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
import shutil
from copy import copy, deepcopy
from functools import reduce

import jsonschema

from octobot_commons.config import load_config, get_user_config
from octobot_commons.config_util import decrypt, encrypt, has_invalid_default_config_value
from octobot_commons.constants import CONFIG_FILE_SCHEMA, DEFAULT_CONFIG_VALUES, CONFIG_ACCEPTED_TERMS, \
    CONFIG_ENABLED_OPTION, CONFIG_DEBUG_OPTION, TENTACLE_DEFAULT_FOLDER, CONFIG_METRICS, TEMP_RESTORE_CONFIG_FILE, \
    CONFIG_EVALUATOR_FILE_PATH, CONFIG_EVALUATOR_FILE, CONFIG_TRADING_FILE_PATH, CONFIG_TRADING_FILE, \
    CONFIG_CRYPTO_CURRENCIES
from octobot_commons.logging.logging_util import get_logger

DELETE_ELEMENT_VALUE = ""


def save_config(config_file, config, temp_restore_config_file, json_data=None):
    try:

        # prepare a restoration config file
        prepare_restore_file(temp_restore_config_file, config_file)

        new_content = jsonify_config(config) if json_data is None else json_data

        # edit the config file
        with open(config_file, "w") as cg_file:
            cg_file.write(new_content)

        # check if the new config file is correct
        check_config(config_file)

        # remove temp file
        remove_restore_file(temp_restore_config_file)

    # when fail restore the old config
    except Exception as e:
        get_logger().error(f"Save config failed : {e}")
        restore_config(temp_restore_config_file, config_file)
        raise e


def validate_config_file(config=None, schema_file=CONFIG_FILE_SCHEMA):
    try:
        with open(schema_file) as json_schema:
            loaded_schema = json.load(json_schema)
        jsonschema.validate(instance=config, schema=loaded_schema)
    except Exception as e:
        return False, e
    return True, None


def restore_config(restore_file, target_file):
    shutil.copy(restore_file, target_file)


def prepare_restore_file(restore_file, current_config_file):
    shutil.copy(current_config_file, restore_file)


def remove_restore_file(restore_file):
    os.remove(restore_file)


def jsonify_config(config):
    try:
        from octobot_trading.constants import CONFIG_EXCHANGES, CONFIG_EXCHANGE_ENCRYPTED_VALUES
        # check exchange keys encryption
        for exchange, exchange_config in config[CONFIG_EXCHANGES].items():
            try:
                for key in CONFIG_EXCHANGE_ENCRYPTED_VALUES:
                    _handle_encrypted_value(key, exchange_config)
            except Exception:
                config[CONFIG_EXCHANGES][exchange] = {key: "" for key in CONFIG_EXCHANGE_ENCRYPTED_VALUES}

        return dump_json(config)
    except ImportError:
        get_logger().error(f"OctoBot_Commons/config_manager.py/jsonify_config requires "
                           f"OctoBot-Trading package installed")


def _handle_encrypted_value(value_key, config_element, verbose=False):
    if value_key in config_element:
        key = config_element[value_key]
        if not has_invalid_default_config_value(key):
            try:
                decrypt(key, silent_on_invalid_token=True)
                return True
            except Exception:
                config_element[value_key] = encrypt(key).decode()
                if verbose:
                    get_logger().warning(f"Non encrypted secret info found in config ({value_key}): replaced "
                                         f"value with encrypted equivalent.")
                return False
    return True


def dump_json(json_data):
    return json.dumps(json_data, indent=4, sort_keys=True)


def check_config(config_file):
    try:
        valid, e = validate_config_file(load_config(config_file=config_file))
        if not valid:
            raise e
    except Exception as e:
        raise e


def is_in_dev_mode(config):
    # return True if "DEV-MODE": true in config.json
    return CONFIG_DEBUG_OPTION in config and config[CONFIG_DEBUG_OPTION]


def update_evaluator_config(to_update_data, current_config, deactivate_others):
    _update_activation_config(to_update_data,
                              current_config,
                              CONFIG_EVALUATOR_FILE_PATH,
                              CONFIG_EVALUATOR_FILE,
                              deactivate_others)


def update_trading_config(to_update_data, current_config):
    _update_activation_config(to_update_data,
                              current_config,
                              CONFIG_TRADING_FILE_PATH,
                              CONFIG_TRADING_FILE,
                              False)

def remove_loaded_only_element(config):
    # OctoBot 0.3.X
    # # remove service instances
    # for service in config[CONFIG_CATEGORY_SERVICES]:
    #     config[CONFIG_CATEGORY_SERVICES][service].pop(CONFIG_SERVICE_INSTANCE, None)
    #
    # # remove non config keys
    # config.pop(CONFIG_EVALUATOR, None)
    # config.pop(CONFIG_TRADING_TENTACLES, None)
    # config.pop(CONFIG_INTERFACES, None)
    # config.pop(CONFIG_ADVANCED_CLASSES, None)
    # config.pop(CONFIG_TIME_FRAME, None)
    # config.pop(CONFIG_NOTIFICATION_INSTANCE, None)
    # config.pop(CONFIG_ADVANCED_INSTANCES, None)
    #
    # # remove backtesting specific differences
    # if backtesting_enabled(config):
    #     if CONFIG_BACKTESTING in config:
    #         config[CONFIG_BACKTESTING].pop(CONFIG_ENABLED_OPTION, None)
    #         config[CONFIG_BACKTESTING].pop(CONFIG_ANALYSIS_ENABLED_OPTION, None)

    # OctoBot 0.4.X
    try:
        from octobot_evaluators.constants import CONFIG_EVALUATOR
        from octobot_trading.constants import CONFIG_TRADING_TENTACLES

        config.pop(CONFIG_EVALUATOR, None)
        config.pop(CONFIG_TRADING_TENTACLES, None)
    except ImportError as e:
        get_logger().error(f"Impossible to save config: requires OctoBot-Trading and "
                           f"OctoBot-Evaluators packages installed")
        raise e


def filter_to_update_data(to_update_data, current_config, in_backtesting):
    if in_backtesting:
        for key in set(to_update_data.keys()):
            # remove changes to currency config when in backtesting
            if CONFIG_CRYPTO_CURRENCIES in key:
                to_update_data.pop(key)


def update_global_config(to_update_data, current_config, in_backtesting,
                         config_separator, update_input=False, delete=False):
    new_current_config = copy(current_config)

    filter_to_update_data(to_update_data, current_config, in_backtesting)

    remove_loaded_only_element(new_current_config)

    # now can make a deep copy
    new_current_config = deepcopy(new_current_config)

    if delete:
        removed_configs = [parse_and_update(data_key, DELETE_ELEMENT_VALUE, config_separator)
                           for data_key in to_update_data]
        reduce(clear_dictionaries_by_keys, [new_current_config] + removed_configs)
        if update_input:
            reduce(clear_dictionaries_by_keys, [current_config] + removed_configs)
    else:
        updated_configs = [
            parse_and_update(data_key, data_value, config_separator)
            for data_key, data_value in to_update_data.items()
        ]
        # merge configs
        reduce(merge_dictionaries_by_appending_keys, [new_current_config] + updated_configs)
        if update_input:
            reduce(merge_dictionaries_by_appending_keys, [current_config] + updated_configs)

    # save config
    save_config(get_user_config(), new_current_config, TEMP_RESTORE_CONFIG_FILE)


def simple_save_config_update(updated_config):
    to_save_config = copy(updated_config)
    remove_loaded_only_element(to_save_config)
    save_config(get_user_config(), to_save_config, TEMP_RESTORE_CONFIG_FILE)
    return True


def parse_and_update(key, new_data, config_separator):
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

def are_of_compatible_type(val1, val2):
    return (
            (
                    isinstance(val1, val2.__class__) or
                    (isinstance(val1, (float, int)) and isinstance(val2, (float, int)))
            ) and isinstance(val1, (bool, str, float, int))
    )


def merge_dictionaries_by_appending_keys(dict_dest, dict_src):
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
                get_logger().error(f"Conflict when merging dict with key : {key}")
        else:
            dict_dest[key] = src_val

    return dict_dest


def clear_dictionaries_by_keys(dict_dest, dict_src):
    for key in dict_src:
        src_val = dict_src[key]
        if key in dict_dest:
            dest_val = dict_dest[key]
            if src_val == DELETE_ELEMENT_VALUE:
                dict_dest.pop(key)
            elif isinstance(dest_val, dict) and isinstance(src_val, dict):
                dict_dest[key] = clear_dictionaries_by_keys(dest_val, src_val)
            else:
                get_logger().error(f"Conflict when deleting dict element with key : {key}")

    return dict_dest


def _update_activation_config(to_update_data, current_config, config_file_path, config_file, deactivate_others):
    from octobot_commons.tentacles_management.class_inspector import get_class_from_string, evaluator_parent_inspection
    something_changed = False
    for element_name, activated in to_update_data.items():
        if element_name in current_config:
            active = activated if isinstance(activated, bool) else activated.lower() == "true"
            current_activation = current_config[element_name]
            if current_activation != active:
                get_logger().info(f"{config_file} updated: {element_name} "
                                  f"{'activated' if active else 'deactivated'}")
                current_config[element_name] = active
                something_changed = True
    if deactivate_others:
        import evaluator.Strategies as strategies
        for element_name, activated in current_config.items():
            if element_name not in to_update_data:
                if current_config[element_name]:
                    # do not deactivate strategies
                    config_class = get_class_from_string(element_name, strategies.StrategiesEvaluator,
                                                         strategies, evaluator_parent_inspection)
                    if config_class is None:
                        get_logger().info(f"{config_file} updated: {element_name} "
                                          f"{'deactivated'}")
                        current_config[element_name] = False
                        something_changed = True
    if something_changed:
        with open(config_file_path, "w+") as config_file_w:
            config_file_w.write(dump_json(current_config))


def update_tentacle_config(klass, config_update):
    current_config = klass.get_specific_config()
    # only update values in config update not to erase values in root config (might not be editable)
    for key, val in config_update.items():
        current_config[key] = val
    with open(klass.get_config_file_name(), "w+") as config_file_w:
        config_file_w.write(dump_json(current_config))


def factory_reset_tentacle_config(klass):
    config_file = klass.get_config_file_name()
    config_folder = klass.get_config_folder()
    config_file_name = config_file.split(config_folder)[1]
    factory_config = f"{config_folder}/{TENTACLE_DEFAULT_FOLDER}/{config_file_name}"
    shutil.copy(factory_config, config_file)


def get_metrics_enabled(config):
    if CONFIG_METRICS in config and config[CONFIG_METRICS] and \
            CONFIG_ENABLED_OPTION in config[CONFIG_METRICS]:
        return bool(config[CONFIG_METRICS][CONFIG_ENABLED_OPTION])
    else:
        return True


def accepted_terms(config):
    if CONFIG_ACCEPTED_TERMS in config:
        return config[CONFIG_ACCEPTED_TERMS]
    return False


def accept_terms(config, accepted):
    config[CONFIG_ACCEPTED_TERMS] = accepted
    simple_save_config_update(config)
