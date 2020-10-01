# pylint: disable=C0415, R0913, W0703
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
import hashlib
import json
import os
import shutil
import copy
import functools

import jsonschema

import octobot_commons.config as commons_config
import octobot_commons.config_util as config_util
import octobot_commons.constants as constants
import octobot_commons.logging as logging_util

DELETE_ELEMENT_VALUE = ""


def save_config(
    config_file, config, temp_restore_config_file, schema_file=None, json_data=None
) -> None:
    """
    Save a json config
    :param config_file: the config file path
    :param config: the json config
    :param temp_restore_config_file: the temporary config file
    :param schema_file: path to the json schema to validate the updated config
    :param json_data: json data if the data is already json
    """
    try:

        # prepare a restoration config file
        prepare_restore_file(temp_restore_config_file, config_file)

        new_content = jsonify_config(config) if json_data is None else json_data

        # edit the config file
        with open(config_file, "w") as cg_file:
            cg_file.write(new_content)

        if schema_file is not None:
            # check if the new config file is correct
            check_config(config_file, schema_file)

        # remove temp file
        remove_restore_file(temp_restore_config_file)

    # when fail restore the old config
    except Exception as global_exception:
        logging_util.get_logger().error(f"Save config failed : {global_exception}")
        restore_config(temp_restore_config_file, config_file)
        raise global_exception


def validate_config_file(
    config=None, schema_file=constants.CONFIG_FILE_SCHEMA
) -> (bool, object):
    """
    Validate a config file
    :param config: the config
    :param schema_file: the config schema
    :return: True if valid, the exception if caught
    """
    try:
        with open(schema_file) as json_schema:
            loaded_schema = json.load(json_schema)
        jsonschema.validate(instance=config, schema=loaded_schema)
    except Exception as global_exception:
        return False, global_exception
    return True, None


def restore_config(restore_file, target_file) -> None:
    """
    Restore a config file from a saved file
    :param restore_file: the restore file path
    :param target_file: the target file path
    """
    shutil.copy(restore_file, target_file)


def prepare_restore_file(restore_file, current_config_file) -> None:
    """
    Prepare a config restoration file
    :param restore_file: the restoration file
    :param current_config_file: the file to be restored
    """
    shutil.copy(current_config_file, restore_file)


def remove_restore_file(restore_file) -> None:
    """
    Remove a restore file
    :param restore_file: the restore file path
    """
    os.remove(restore_file)


def jsonify_config(config) -> str:
    """
    Jsonify a config
    :param config: the config
    :return: the jsonified config
    """
    try:
        from octobot_trading.constants import (
            CONFIG_EXCHANGES,
            CONFIG_EXCHANGE_ENCRYPTED_VALUES,
        )

        # check exchange keys encryption
        for exchange, exchange_config in config[CONFIG_EXCHANGES].items():
            try:
                for key in CONFIG_EXCHANGE_ENCRYPTED_VALUES:
                    _handle_encrypted_value(key, exchange_config)
            except Exception:
                config[CONFIG_EXCHANGES][exchange] = {
                    key: "" for key in CONFIG_EXCHANGE_ENCRYPTED_VALUES
                }

        return dump_json(config)
    except ImportError:
        logging_util.get_logger().error(
            "OctoBot_Commons/config_manager.py/jsonify_config requires "
            "OctoBot-Trading package installed"
        )


def _handle_encrypted_value(value_key, config_element, verbose=False):
    """
    Handle encrypted value
    :param value_key: the value key
    :param config_element: the config element
    :param verbose: if verbosity is enabled
    :return: True if the value can be decrypted
    """
    if value_key in config_element:
        key = config_element[value_key]
        if not config_util.has_invalid_default_config_value(key):
            try:
                config_util.decrypt(key, silent_on_invalid_token=True)
                return True
            except Exception:
                config_element[value_key] = config_util.encrypt(key).decode()
                if verbose:
                    logging_util.get_logger().warning(
                        f"Non encrypted secret info found in config ({value_key}): replaced "
                        f"value with encrypted equivalent."
                    )
                return False
    return True


def get_password_hash(password):
    """
    Returns the password's hex digest
    :param password: the password to hash
    :return: the hash digest
    """
    return hashlib.sha256(password.encode()).hexdigest()


def dump_json(json_data) -> str:
    """
    The dumped json data
    :param json_data: the json data to be dumped
    :return: the dumped json data
    """
    return json.dumps(json_data, indent=4, sort_keys=True)


def check_config(config_file, schema_file) -> None:
    """
    Check a config file
    :param config_file: the config file path
    :param schema_file: path to the json schema to validate the updated config
    """
    try:
        valid, global_exception = validate_config_file(
            commons_config.load_config(config_file=config_file), schema_file=schema_file
        )
        if not valid:
            raise global_exception  # pylint: disable=E0702
    except Exception as global_exception:
        raise global_exception


def is_in_dev_mode(config) -> None:
    """
    Check if dev mode is enabled
    :param config: the config
    :return: if dev mode is enabled
    """
    # return True if "DEV-MODE": true in config.json
    return (
        constants.CONFIG_DEBUG_OPTION in config
        and config[constants.CONFIG_DEBUG_OPTION]
    )


def filter_to_update_data(to_update_data, in_backtesting):
    """
    Filter data to update
    :param to_update_data: the data to be updated
    :param in_backtesting: if backtesting is enabled
    :return: the updated data
    """
    if in_backtesting:
        for key in set(to_update_data.keys()):
            # remove changes to currency config when in backtesting
            if constants.CONFIG_CRYPTO_CURRENCIES in key:
                to_update_data.pop(key)


def update_global_config(
    to_update_data,
    current_config,
    schema_file,
    in_backtesting,
    config_separator,
    update_input=False,
    delete=False,
) -> None:
    """
    Update the global config
    :param to_update_data: the data to update
    :param current_config: the current config
    :param schema_file: path to the json schema to validate the updated config
    :param in_backtesting: if backtesting is enabled
    :param config_separator: the config separator
    :param update_input: if input should be updated
    :param delete: if the data should be removed
    """
    new_current_config = copy.copy(current_config)

    filter_to_update_data(to_update_data, in_backtesting)

    # now can make a deep copy
    new_current_config = copy.deepcopy(new_current_config)

    if delete:
        removed_configs = [
            parse_and_update(data_key, DELETE_ELEMENT_VALUE, config_separator)
            for data_key in to_update_data
        ]
        functools.reduce(
            clear_dictionaries_by_keys, [new_current_config] + removed_configs
        )
        if update_input:
            functools.reduce(
                clear_dictionaries_by_keys, [current_config] + removed_configs
            )
    else:
        updated_configs = [
            parse_and_update(data_key, data_value, config_separator)
            for data_key, data_value in to_update_data.items()
        ]
        # merge configs
        functools.reduce(
            merge_dictionaries_by_appending_keys, [new_current_config] + updated_configs
        )
        if update_input:
            functools.reduce(
                merge_dictionaries_by_appending_keys, [current_config] + updated_configs
            )

    # save config
    save_config(
        commons_config.get_user_config(),
        new_current_config,
        constants.TEMP_RESTORE_CONFIG_FILE,
        schema_file,
    )


def simple_save_config_update(updated_config, schema_file=None) -> bool:
    """
    Simple config update saving
    :param updated_config: the updated config
    :param schema_file: path to the json schema to validate the updated config
    :return: True if successfully updated
    """
    to_save_config = copy.copy(updated_config)
    save_config(
        commons_config.get_user_config(),
        to_save_config,
        constants.TEMP_RESTORE_CONFIG_FILE,
        schema_file,
    )
    return True


def parse_and_update(key, new_data, config_separator):
    """
    Parse and update key
    :param key: the key to update
    :param new_data: the new data
    :param config_separator: the config separator
    :return: the key updated
    """
    parsed_data_array = key.split(config_separator)
    new_config = {}
    current_dict = new_config

    for i, _ in enumerate(parsed_data_array):
        if i > 0:
            if i == len(parsed_data_array) - 1:
                current_dict[parsed_data_array[i]] = new_data
            else:
                current_dict[parsed_data_array[i]] = {}
        else:
            new_config[parsed_data_array[i]] = {}

        current_dict = current_dict[parsed_data_array[i]]

    return new_config


def are_of_compatible_type(val1, val2) -> bool:
    """
    Check if types are compatibles
    :param val1: the first value
    :param val2: the second value
    :return: True if types are compatible
    """
    return (
        isinstance(val1, val2.__class__)
        or (isinstance(val1, (float, int)) and isinstance(val2, (float, int)))
    ) and isinstance(val1, (bool, str, float, int))


def merge_dictionaries_by_appending_keys(dict_dest, dict_src) -> dict:
    """
    Merge dictionnaries by appending keys
    :param dict_dest: the destination dictionnary
    :param dict_src: the source dictionnary
    :return: the merged dictionnary
    """
    for key in dict_src:
        src_val = dict_src[key]
        if key in dict_dest:
            dest_val = dict_dest[key]
            if isinstance(dest_val, dict) and isinstance(src_val, dict):
                dict_dest[key] = merge_dictionaries_by_appending_keys(dest_val, src_val)
            elif dest_val == src_val:
                pass  # same leaf value
            elif are_of_compatible_type(dest_val, src_val):
                # simple type: update value
                dict_dest[key] = src_val
            elif isinstance(dest_val, list) and isinstance(src_val, list):
                dict_dest[key] = src_val
            else:
                logging_util.get_logger().error(
                    f"Conflict when merging dict with key : {key}"
                )
        else:
            dict_dest[key] = src_val

    return dict_dest


def clear_dictionaries_by_keys(dict_dest, dict_src):
    """
    Clear dictionnaries by keys
    :param dict_dest: the destination dictionnary
    :param dict_src: the source dictionnary
    :return: the cleaned dictionnary
    """
    for key in dict_src:
        src_val = dict_src[key]
        if key in dict_dest:
            dest_val = dict_dest[key]
            if src_val == DELETE_ELEMENT_VALUE:
                dict_dest.pop(key)
            elif isinstance(dest_val, dict) and isinstance(src_val, dict):
                dict_dest[key] = clear_dictionaries_by_keys(dest_val, src_val)
            else:
                logging_util.get_logger().error(
                    f"Conflict when deleting dict element with key : {key}"
                )

    return dict_dest


def get_metrics_enabled(config) -> bool:
    """
    Check if metrics are enabled
    :param config: the config
    :return: the check result
    """
    if (
        constants.CONFIG_METRICS in config
        and config[constants.CONFIG_METRICS]
        and constants.CONFIG_ENABLED_OPTION in config[constants.CONFIG_METRICS]
    ):
        return bool(config[constants.CONFIG_METRICS][constants.CONFIG_ENABLED_OPTION])
    return True


def accepted_terms(config) -> bool:
    """
    Check if terms has been accepted
    :param config: the config
    :return: the check result
    """
    if constants.CONFIG_ACCEPTED_TERMS in config:
        return config[constants.CONFIG_ACCEPTED_TERMS]
    return False


def accept_terms(config, accepted) -> None:
    """
    Perform terms acceptation
    :param config: the config
    :param accepted: accepted or not
    """
    config[constants.CONFIG_ACCEPTED_TERMS] = accepted
    simple_save_config_update(config)
