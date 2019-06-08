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
import logging

from octobot_commons import OCTOBOT_KEY
from octobot_commons.constants import DEFAULT_CONFIG_VALUES
from cryptography.fernet import Fernet, InvalidToken


def has_invalid_default_config_value(*config_values):
    return any(value in DEFAULT_CONFIG_VALUES for value in config_values)


def encrypt(data):
    try:
        return Fernet(OCTOBOT_KEY).encrypt(data.encode())
    except Exception as e:
        logging.getLogger().error(f"Failed to encrypt : {data}")
        raise e


def decrypt(data, silent_on_invalid_token=False):
    try:
        return Fernet(OCTOBOT_KEY).decrypt(data.encode()).decode()
    except InvalidToken as e:
        if not silent_on_invalid_token:
            logging.getLogger().error(f"Failed to decrypt : {data} ({e})")
        raise e
    except Exception as e:
        logging.getLogger().error(f"Failed to decrypt : {data} ({e})")
        raise e
