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

from logging import ERROR, getLevelName, WARNING

from octobot_commons.timestamp_util import get_now_time

LOG_DATABASE = "log_db"
LOG_NEW_ERRORS_COUNT = "log_new_errors_count"

STORED_LOG_MIN_LEVEL = WARNING
BACKTESTING_NEW_ERRORS_COUNT: str = "log_backtesting_errors_count"

logs_database = {
    LOG_DATABASE: [],
    LOG_NEW_ERRORS_COUNT: 0,
    BACKTESTING_NEW_ERRORS_COUNT: 0
}

error_notifier_callbacks = []

LOGS_MAX_COUNT = 1000


def add_log(level, source, message, keep_log=True, call_notifiers=True):
    if keep_log:
        logs_database[LOG_DATABASE].append({
            "Time": get_now_time(),
            "Level": getLevelName(level),
            "Source": str(source),
            "Message": message
        })
        if len(logs_database[LOG_DATABASE]) > LOGS_MAX_COUNT:
            logs_database[LOG_DATABASE].pop(0)
    if level >= ERROR:
        logs_database[LOG_NEW_ERRORS_COUNT] += 1
        logs_database[BACKTESTING_NEW_ERRORS_COUNT] += 1
    if call_notifiers:
        for callback in error_notifier_callbacks:
            callback()


def get_errors_count(counter=LOG_NEW_ERRORS_COUNT):
    return logs_database[counter]


def reset_errors_count(counter=LOG_NEW_ERRORS_COUNT):
    logs_database[counter] = 0


def register_error_notifier(callback):
    error_notifier_callbacks.append(callback)
