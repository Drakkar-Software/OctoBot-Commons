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
from octobot_commons.configuration import configuration
from octobot_commons.configuration import config_file_manager
from octobot_commons.configuration import config_operations
from octobot_commons.configuration import fields_utils


from octobot_commons.configuration.configuration import (
    Configuration,
)
from octobot_commons.configuration.config_file_manager import (
    get_user_config,
    load,
    dump,
    check_config,
    jsonify_config,
    handle_encrypted_value,
    prepare_restore_file,
    remove_restore_file,
    restore,
    dump_formatted_json,
)
from octobot_commons.configuration.config_operations import (
    filter_to_update_data,
    parse_and_update,
    merge_dictionaries_by_appending_keys,
    clear_dictionaries_by_keys,
)
from octobot_commons.configuration.fields_utils import (
    has_invalid_default_config_value,
    encrypt,
    decrypt,
    decrypt_element_if_possible,
    get_password_hash,
)


__all__ = [
    "Configuration",
    "get_user_config",
    "load",
    "dump",
    "check_config",
    "jsonify_config",
    "handle_encrypted_value",
    "prepare_restore_file",
    "remove_restore_file",
    "restore",
    "dump_formatted_json",
    "filter_to_update_data",
    "parse_and_update",
    "merge_dictionaries_by_appending_keys",
    "clear_dictionaries_by_keys",
    "has_invalid_default_config_value",
    "encrypt",
    "decrypt",
    "decrypt_element_if_possible",
    "get_password_hash",
]
