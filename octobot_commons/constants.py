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

import octobot_commons.enums as enums

# time
MSECONDS_TO_SECONDS = 1000
MINUTE_TO_SECONDS = 60
MSECONDS_TO_MINUTE = MSECONDS_TO_SECONDS * MINUTE_TO_SECONDS
HOURS_TO_SECONDS = MINUTE_TO_SECONDS * 60
HOURS_TO_MSECONDS = MSECONDS_TO_SECONDS * MINUTE_TO_SECONDS * MINUTE_TO_SECONDS
DAYS_TO_SECONDS = HOURS_TO_SECONDS * 24

# Strings
CONFIG_WILDCARD = "*"
PORTFOLIO_AVAILABLE = "available"
MARGIN_PORTFOLIO = "margin"
PORTFOLIO_TOTAL = "total"

# config
CONFIG_ENABLED_OPTION = "enabled"
CONFIG_DEBUG_OPTION = "DEV-MODE"
CONFIG_TIME_FRAME = "time_frame"
USER_FOLDER = "user"
CONFIG_FOLDER = "config"
CONFIG_FILE = "config.json"
TEMP_RESTORE_CONFIG_FILE = "temp_config.json"
DEFAULT_CONFIG_FILE = "default_config.json"
DEFAULT_CONFIG_FILE_PATH = f"{CONFIG_FOLDER}/{DEFAULT_CONFIG_FILE}"
SCHEMA = "schema"
CONFIG_FILE_EXT = ".json"
CONFIG_FILE_SCHEMA = f"{CONFIG_FOLDER}/config_{SCHEMA}.json"
CONFIG_REFRESH_RATE = "refresh_rate_seconds"

# Config currencies
CONFIG_CRYPTO_CURRENCIES = "crypto-currencies"
CONFIG_CRYPTO_CURRENCY = "crypto-currency"
CONFIG_CRYPTO_PAIRS = "pairs"
CONFIG_CRYPTO_QUOTE = "quote"
CONFIG_CRYPTO_ADD = "add"

# OS
PLATFORM_DATA_SEPARATOR = ":"

# Evaluators
MIN_EVAL_TIME_FRAME = enums.TimeFrames.ONE_MINUTE
INIT_EVAL_NOTE = 0
START_PENDING_EVAL_NOTE = "0"

# tentacles
TENTACLE_DEFAULT_CONFIG = "default_config"

# terms of service
CONFIG_ACCEPTED_TERMS = "accepted_terms"

# metrics
CONFIG_METRICS = "metrics"
CONFIG_METRICS_BOT_ID = "metrics-bot-id"
TIMER_BEFORE_METRICS_REGISTRATION_SECONDS = 600
TIMER_BETWEEN_METRICS_UPTIME_UPDATE = 3600 * 4
METRICS_URL = "https://octobotmetrics.herokuapp.com/"
METRICS_ROUTE_GEN_BOT_ID = "gen-bot-id"
METRICS_ROUTE = "metrics"
METRICS_ROUTE_COMMUNITY = f"{METRICS_ROUTE}/community"
METRICS_ROUTE_UPTIME = f"{METRICS_ROUTE}/uptime"
METRICS_ROUTE_REGISTER = f"{METRICS_ROUTE}/register"
COMMUNITY_TOPS_COUNT = 1000
PLATFORM_DATA_SEPARATOR = ":"

# default values in config files and interfaces
DEFAULT_CONFIG_VALUES = {
    "your-api-key-here",
    "your-api-secret-here",
    "your-api-password-here",
    "NOKEY",
    "NO KEY",
    "Empty",
}

# Async settings
DEFAULT_FUTURE_TIMEOUT = 120

# External resources
EXTERNAL_RESOURCE_URL = "https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/external_resources.json"
