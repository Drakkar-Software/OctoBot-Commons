# pylint: disable=R0913,W0703
#  Drakkar-Software OctoBot-Commons
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import json
import os
import zipfile
import shutil
import pathlib
import uuid
import time
import requests
import octobot_commons.constants as constants
import octobot_commons.logging as bot_logging

# avoid cyclic import
from octobot_commons.profiles.profile import Profile


def export_profile(profile, export_path: str) -> str:
    """
    Exports the given profile into export_path, appends ".zip" as a file extension
    :param profile: profile to export
    :param export_path: export path ending with filename
    :return: the exported profile path including file extension
    """
    temp_path = f"{export_path}{int(time.time() * 1000)}"
    # remove any existing file to prevent any side effect
    if os.path.exists(temp_path):
        raise OSError(f"Can't export profile, the {temp_path} folder exists")
    export_path_with_ext = f"{export_path}.{constants.PROFILE_EXPORT_FORMAT}"
    if os.path.isfile(export_path_with_ext):
        os.remove(export_path_with_ext)
    # copy profile into a temp dir to edit it
    shutil.copytree(profile.path, temp_path)
    try:
        _filter_profile_export(temp_path)
        # export the edited profile
        shutil.make_archive(export_path, constants.PROFILE_EXPORT_FORMAT, temp_path)
    finally:
        shutil.rmtree(temp_path)
    return export_path_with_ext


def install_profile(
    import_path: str,
    profile_name: str,
    bot_install_path: str,
    replace_if_exists: bool,
    is_imported: bool,
    origin_url: str = None,
    quite: bool = False,
) -> Profile:
    """
    Installs the given profile export archive into the user's profile directory
    :param import_path: path to the profile zipped archive
    :param profile_name: name of the profile folder
    :param bot_install_path: path to the octobot installation
    :param replace_if_exists: when True erase the profile with the same name if it exists
    :param is_imported: when True erase the profile is set as imported
    :param origin_url: url the profile is coming from (if relevant)
    :param quite: when True, only log errors
    :return: The created profile
    """
    logger = bot_logging.get_logger("ProfileSharing")
    target_import_path, replaced = _get_target_import_path(
        bot_install_path, profile_name, replace_if_exists
    )
    action = "Creat"
    if replaced:
        action = "Updat"
    if not quite:
        logger.info(f"{action}ing {profile_name} profile.")
    _import_profile_files(import_path, target_import_path)
    profile = Profile(target_import_path).read_config()
    profile.imported = is_imported
    profile.origin_url = origin_url
    _ensure_unique_profile_id(profile)
    if not quite:
        logger.info(f"{action}ed {profile.name} ({profile_name}) profile.")
    return profile


def import_profile(
    import_path: str,
    name: str = None,
    bot_install_path: str = ".",
    origin_url: str = None,
) -> Profile:
    """
    Imports the given profile export archive into the user's profile directory with the "imported_" prefix
    :param import_path: path to the profile zipped archive
    :param name: name of the profile folder
    :param bot_install_path: path to the octobot installation
    :param origin_url: url the profile is coming from
    :return: The created profile
    """
    temp_profile_name = _get_profile_name(name, import_path)
    profile = install_profile(
        import_path,
        temp_profile_name,
        bot_install_path,
        False,
        True,
        origin_url=origin_url,
    )
    if profile.name != temp_profile_name:
        profile.rename_folder(_get_unique_profile_folder_from_name(profile), False)
    return profile


def download_profile(url, target_file, timeout=60):
    """
    Downloads a profile from the given url
    :param url: profile url
    :param target_file: path to save the file
    :param timeout: time given to the request before timeout
    :return: saved file path
    """
    # unauthenticated download
    with requests.get(url, stream=True, timeout=timeout) as req:
        req.raise_for_status()
        with open(target_file, "wb") as write_file:
            for chunk in req.iter_content(chunk_size=8192):
                write_file.write(chunk)
    return target_file


def download_and_install_profile(download_url):
    """
    :param download_url: profile url
    :return: the installed profile, None if an error occurred
    """
    logger = bot_logging.get_logger("ProfileSharing")
    name = download_url.split("/")[-1]
    file_path = None
    try:
        file_path = download_profile(download_url, name)
        profile = import_profile(file_path, name=name, origin_url=download_url)
        logger.info(
            f"Downloaded and installed {profile.name} from {profile.origin_url}"
        )
        return profile
    except Exception as err:
        logger.exception(err, True, f"Error when installing profile: {err}")
        return None
    finally:
        if file_path is not None and os.path.isfile(file_path):
            os.remove(file_path)


def _get_profile_name(name, import_path):
    profile_name = name or (
        f"{constants.IMPORTED_PROFILE_PREFIX}_{os.path.split(import_path)[-1]}"
    )
    return profile_name.split(f".{constants.PROFILE_EXPORT_FORMAT}")[0]


def _filter_profile_export(profile_path: str):
    profile_file = os.path.join(profile_path, constants.PROFILE_CONFIG_FILE)
    if os.path.isfile(profile_file):
        with open(profile_file) as open_file:
            parsed_profile = json.load(open_file)
        _filter_disabled(parsed_profile, constants.CONFIG_EXCHANGES)
        with open(profile_file, "w") as open_file:
            json.dump(parsed_profile, open_file, indent=4, sort_keys=True)


def _filter_disabled(profile_config: dict, element):
    filtered_exchanges = {
        exchange: details
        for exchange, details in profile_config[constants.PROFILE_CONFIG][
            element
        ].items()
        if details.get(constants.CONFIG_ENABLED_OPTION, True)
    }
    profile_config[constants.PROFILE_CONFIG][element] = filtered_exchanges


def _get_target_import_path(
    bot_install_path: str, profile_name: str, replace_if_exists: bool
) -> (str, bool):
    """
    Get the target profile folder path
    :param bot_install_path: path to the octobot installation
    :param profile_name: name of the profile folder
    :param replace_if_exists: when True erase the profile with the same name if it exists
    :return: (the final target import path, True if the profile is replaced)
    """
    target_import_path = os.path.join(
        bot_install_path, constants.USER_PROFILES_FOLDER, profile_name
    )
    if replace_if_exists:
        try:
            replaced = True
            shutil.rmtree(target_import_path)
        except FileNotFoundError:
            replaced = False
        return target_import_path, replaced
    return _get_unique_profile_folder(target_import_path), False


def _import_profile_files(profile_path: str, target_profile_path: str) -> None:
    """
    Copy or extract profile files to destination
    :param profile_path: the current profile path
    :param target_profile_path: the target profile path
    :return: None
    """
    if zipfile.is_zipfile(profile_path):
        with zipfile.ZipFile(profile_path) as zipped:
            zipped.extractall(target_profile_path)
    else:
        shutil.copytree(profile_path, target_profile_path)


def _get_unique_profile_folder_from_name(profile) -> str:
    folder = _get_unique_profile_folder(
        os.path.join(os.path.split(profile.path)[0], profile.name)
    )
    return os.path.split(folder)[1]


def _get_unique_profile_folder(target_import_path: str) -> str:
    """
    Creates an unique profile folder name
    :param target_import_path: the expected target profile folder name
    :return: the unique profile folder name
    """
    iteration = 1
    candidate = target_import_path
    while os.path.exists(candidate) and iteration < 100:
        iteration += 1
        candidate = f"{target_import_path}_{iteration}"
    return candidate


def _ensure_unique_profile_id(profile) -> None:
    """
    Ensure that no other installed profile has the same id
    :param profile: the installed profile
    :return: None
    """
    ids = Profile.get_all_profiles_ids(
        pathlib.Path(profile.path).parent, ignore=profile.path
    )
    iteration = 1
    while profile.profile_id in ids and iteration < 100:
        profile.profile_id = str(uuid.uuid4())
        iteration += 1
    profile.save()
