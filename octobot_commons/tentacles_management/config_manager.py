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
from octobot_commons.config import load_config


def reload_tentacle_config(config: dict,
                           config_key: str,
                           tentacle_config_path: str,
                           raised_exception: Exception = None):
    config[config_key] = load_config(tentacle_config_path, False)
    if config[config_key] is None:
        raise raised_exception if raised_exception is not None else Exception

    return config
