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

from octobot_commons.enums import TimeFrames

# Strings
CONFIG_WILDCARD = "*"
PORTFOLIO_AVAILABLE = "available"
PORTFOLIO_TOTAL = "total"

# config
CONFIG_ENABLED_OPTION = "enabled"
CONFIG_TIME_FRAME = "time_frame"
USER_FOLDER = "user"
CONFIG_FILE = "config.json"
DEFAULT_CONFIG_FILE = "config/default_config.json"
SCHEMA = "schema"
CONFIG_FOLDER = "config"
CONFIG_FILE_EXT = ".json"
CONFIG_FILE_SCHEMA = f"{CONFIG_FOLDER}/config_{SCHEMA}.json"

# Evaluators
MIN_EVAL_TIME_FRAME = TimeFrames.FIVE_MINUTES

# tentacles
TENTACLE_CONFIG_FOLDER = "config"
TENTACLES_PATH = "tentacles"

# Advanced
CONFIG_ADVANCED_CLASSES = "advanced_classes"
CONFIG_ADVANCED_INSTANCES = "advanced_instances"

# default values in config files and interfaces
DEFAULT_CONFIG_VALUES = {"your-api-key-here", "your-api-secret-here", "your-api-password-here", "NOKEY", "Empty"}
