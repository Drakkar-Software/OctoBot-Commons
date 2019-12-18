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
from shutil import copyfile

from octobot_commons.constants import USER_FOLDER, CONFIG_FILE, DEFAULT_CONFIG_FILE_PATH


def get_user_config():
    return os.path.join(USER_FOLDER, CONFIG_FILE)


def load_config(config_file=get_user_config(), error=True, fill_missing_fields=False) -> dict:
    logger = logging.getLogger("CONFIG LOADER")
    basic_error = "Error when load config file {0}".format(config_file)
    try:
        with open(config_file) as json_data_file:
            config = json.load(json_data_file)
            # if fill_missing_fields: TODO
            #     _fill_missing_config_fields(config)
        return config
    except ValueError as e:
        error_str = "{0} : json decoding failed ({1})".format(basic_error, e)
        if error:
            raise Exception(error_str)
        else:
            logger.error(error_str)
    except IOError as e:
        error_str = "{0} : file opening failed ({1})".format(basic_error, e)
        if error:
            raise Exception(error_str)
        else:
            logger.error(error_str)
    except Exception as e:
        error_str = f"{basic_error} : {e}"
        if error:
            raise Exception(error_str)
        else:
            logger.error(error_str)
    return None


def init_config(config_file=get_user_config(), from_config_file=DEFAULT_CONFIG_FILE_PATH):
    try:
        if not os.path.exists(USER_FOLDER):
            os.makedirs(USER_FOLDER)

        copyfile(from_config_file, config_file)
    except Exception as e:
        raise Exception(f"Can't init config file {e}")


def is_config_empty_or_missing(config_file=get_user_config()):
    return (not os.path.isfile(config_file)) or os.stat(config_file).st_size == 0
