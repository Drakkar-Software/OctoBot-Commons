# pylint: disable=W0703, W0613
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
import logging
import os

import octobot_commons.constants as constants


def get_user_config():
    """
    Return user config path
    :return: user config path
    """
    return os.path.join(constants.USER_FOLDER, constants.CONFIG_FILE)


def load_config(
    config_file=get_user_config(), error=True, fill_missing_fields=False
) -> dict:
    """
    Load a config from a config_file
    :param config_file: the config file path
    :param error: if error should be raised
    :param fill_missing_fields: if missing fields should be filled
    :return: the loaded config
    """
    logger = logging.getLogger("CONFIG LOADER")
    basic_error = "Error when load config file {0}".format(config_file)
    try:
        with open(config_file) as json_data_file:
            config = json.load(json_data_file)
            # if fill_missing_fields: TODO
            #     _fill_missing_config_fields(config)
        return config
    except ValueError as value_error:
        error_str = "{0} : json decoding failed ({1})".format(basic_error, value_error)
        if error:
            raise Exception(error_str)
        logger.error(error_str)
    except IOError as io_error:
        error_str = "{0} : file opening failed ({1})".format(basic_error, io_error)
        if error:
            raise Exception(error_str)
        logger.error(error_str)
    except Exception as global_exception:
        error_str = f"{basic_error} : {global_exception}"
        if error:
            raise Exception(error_str)
        logger.error(error_str)
    return None


def is_config_empty_or_missing(config_file=get_user_config()):
    """
    Check if the config file at path is empty or is missing
    :param config_file: the config file path
    :return: the check result
    """
    return (not os.path.isfile(config_file)) or os.stat(config_file).st_size == 0
