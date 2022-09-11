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


def import_profile(
    import_path: str,
    name: str = None,
    bot_install_path: str = ".",
    replace_if_exists: bool = False,
) -> Profile:
    """
    Imports the given profile export archive into the user's profile directory with the "imported_" prefix
    :param import_path: path to the profile zipped archive
    :param name: name of the profile folder
    :param bot_install_path: path to the octobot installation
    :param replace_if_exists: when True erase the profile with the same name if it exists
    :return: None
    """
    logger = bot_logging.get_logger("ProfileSharing")
    profile_name = name or (
        f"{constants.IMPORTED_PROFILE_PREFIX}_{os.path.split(import_path)[-1]}"
    )
    profile_name = profile_name.split(f".{constants.PROFILE_EXPORT_FORMAT}")[0]
    target_import_path, replaced = _get_target_import_path(
        bot_install_path, profile_name, replace_if_exists
    )
    action = "Creat"
    if replaced:
        action = "Updat"
    logger.info(f"{action}ing {profile_name} profile.")
    _import_profile_files(import_path, target_import_path)
    profile = Profile(target_import_path).read_config()
    profile.imported = True
    _ensure_unique_profile_id(profile)
    logger.info(f"{action}ed {profile.name} ({profile_name}) profile.")
    return profile


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
