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
import os
import zipfile
import shutil
import pathlib
import uuid
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
    export_path_with_ext = f"{export_path}.{constants.PROFILE_EXPORT_FORMAT}"
    # remove any existing file to prevent any side effect
    if os.path.isfile(export_path_with_ext):
        os.remove(export_path_with_ext)
    shutil.make_archive(export_path, constants.PROFILE_EXPORT_FORMAT, profile.path)
    return export_path_with_ext


def import_profile(
    import_path: str,
    name: str = None,
    bot_install_path: str = ".",
    replace_if_exists: bool = False,
) -> None:
    """
    Imports the given profile export archive into the user's profile directory with the "imported_" prefix
    :param import_path: path to the profile zipped archive
    :param name: name of the profile folder
    :param bot_install_path: path to the octobot installation
    :param replace_if_exists: when True erase the profile with the same name if it exists
    :return: None
    """
    profile_name = name or (
        f"{constants.IMPORTED_PROFILE_PREFIX}_{os.path.split(import_path)[-1]}"
    )
    profile_name = profile_name.split(f".{constants.PROFILE_EXPORT_FORMAT}")[0]
    target_import_path, replaced = _get_target_import_path(
        bot_install_path, profile_name, replace_if_exists
    )
    action = "Creating"
    if replaced:
        action = "Updating"
    bot_logging.get_logger("ProfileSharing").info(f"{action} {profile_name} profile.")
    _import_profile_files(import_path, target_import_path)
    _ensure_unique_profile_id(target_import_path)


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


def _ensure_unique_profile_id(profile_path: str) -> None:
    """
    Ensure that no other installed profile has the same id
    :param profile_path: the installed profile folder
    :return: None
    """
    ids = Profile.get_all_profiles_ids(
        pathlib.Path(profile_path).parent, ignore=profile_path
    )
    profile = Profile(profile_path)
    profile.read_config()
    iteration = 1
    while profile.profile_id in ids and iteration < 100:
        profile.profile_id = str(uuid.uuid4())
        iteration += 1
    profile.save()
