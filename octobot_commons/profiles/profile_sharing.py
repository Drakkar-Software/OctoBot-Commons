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
import octobot_commons.constants as constants


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
    import_path: str, name: str = None, bot_install_path: str = "."
) -> None:
    """
    Imports the given profile export archive into the user's profile directory with the "imported_" prefix
    :param import_path: path to the profile zipped archive
    :param name: name of the profile folder
    :param bot_install_path: path to the octobot installation
    :return: None
    """
    profile_name = name or (
        f"{constants.IMPORTED_PROFILE_PREFIX}_{os.path.split(import_path)[-1]}"
    )
    profile_name = profile_name.split(f".{constants.PROFILE_EXPORT_FORMAT}")[0]
    target_import_path = os.path.join(
        bot_install_path, constants.USER_PROFILES_FOLDER, profile_name
    )
    target_import_path = _get_unique_profile_folder(target_import_path)
    if zipfile.is_zipfile(import_path):
        with zipfile.ZipFile(import_path) as zipped:
            zipped.extractall(target_import_path)
    else:
        shutil.copytree(import_path, target_import_path)


def _get_unique_profile_folder(target_import_path):
    i = 1
    candidate = target_import_path
    while os.path.isfile(candidate):
        i += 1
        candidate = f"{target_import_path}_{i}"
    return candidate
