# pylint: disable=W0603
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

from octobot_commons.logging import (
    add_log,
    reset_errors_count,
    get_errors_count,
    BACKTESTING_NEW_ERRORS_COUNT,
    STORED_LOG_MIN_LEVEL,
)

ERROR_PUBLICATION_ENABLED = True
SHOULD_PUBLISH_LOGS_WHEN_RE_ENABLED = False


def set_global_logger_level(level) -> None:
    """
    Set the global logger level
    :param level: the level to set
    """
    logger = logging.getLogger()
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)


def get_global_logger_level() -> object:
    """
    Return the global logger level
    :return: the global logger level
    """
    return logging.getLogger().getEffectiveLevel()


def get_logger(logger_name="Anonymous") -> object:
    """
    Return the logger from the logger_name
    :param logger_name: the logger name
    :return: the logger from the logger name
    """
    return BotLogger(logger_name)


def set_logging_level(logger_names, level) -> None:
    """
    Set the logging level for the logger names
    :param logger_names: the logger names
    :param level: the level to set
    """
    for name in logger_names:
        logging.getLogger(name).setLevel(level)


class BotLogger:
    """
    The bot logger that manage all OctoBot's logs
    """

    def __init__(self, logger_name):
        self.logger_name = logger_name
        self.logger = logging.getLogger(logger_name)

    def debug(self, message) -> None:
        """
        Called for a debug log
        :param message: the log message
        """
        self.logger.debug(message)
        self._publish_log_if_necessary(message, logging.DEBUG)

    def info(self, message) -> None:
        """
        Called for an info log
        :param message: the log message
        """
        self.logger.info(message)
        self._publish_log_if_necessary(message, logging.INFO)

    def warning(self, message) -> None:
        """
        Called for a warning log
        :param message: the log message
        """
        self.logger.warning(message)
        self._publish_log_if_necessary(message, logging.WARNING)

    def error(self, message) -> None:
        """
        Called for an error log
        :param message: the log message
        """
        self.logger.error(message)
        self._publish_log_if_necessary(message, logging.ERROR)

    def exception(
        self, exception, publish_error_if_necessary=False, error_message=None
    ) -> None:
        """
        Called for an exception log
        :param exception: the log exception
        :param publish_error_if_necessary: if the error should be published
        :param error_message: the log message
        """
        self.logger.exception(exception)
        if publish_error_if_necessary:
            self.error(exception if error_message is None else error_message)

    def critical(self, message) -> None:
        """
        Called for a critical log
        :param message: the log message
        """
        self.logger.critical(message)
        self._publish_log_if_necessary(message, logging.CRITICAL)

    def fatal(self, message) -> None:
        """
        Called for a fatal log
        :param message: the log message
        """
        self.logger.fatal(message)
        self._publish_log_if_necessary(message, logging.FATAL)

    def _publish_log_if_necessary(self, message, level) -> None:
        """
        Publish the log message if necessary
        :param message: the log message
        :param level: the log level
        """
        if STORED_LOG_MIN_LEVEL <= level and get_global_logger_level() <= level:
            self._web_interface_publish_log(message, level)
            if not ERROR_PUBLICATION_ENABLED and logging.ERROR <= level:
                global SHOULD_PUBLISH_LOGS_WHEN_RE_ENABLED
                SHOULD_PUBLISH_LOGS_WHEN_RE_ENABLED = True

    def _web_interface_publish_log(self, message, level) -> None:
        """
        Publish log to web interface
        :param message: the log message
        :param level: the log level
        """
        add_log(
            level, self.logger_name, message, call_notifiers=ERROR_PUBLICATION_ENABLED,
        )


def get_backtesting_errors_count() -> int:
    """
    Get backtesting errors count
    :return: the backtesting errors count
    """
    return get_errors_count(BACKTESTING_NEW_ERRORS_COUNT)


def reset_backtesting_errors() -> None:
    """
    Reset the backtesting errors count
    """
    reset_errors_count(BACKTESTING_NEW_ERRORS_COUNT)


def set_error_publication_enabled(enabled) -> None:
    """
    Set the error publication enabling
    :param enabled: if the error publication is enabled
    """
    global ERROR_PUBLICATION_ENABLED
    global SHOULD_PUBLISH_LOGS_WHEN_RE_ENABLED
    ERROR_PUBLICATION_ENABLED = enabled
    if enabled and SHOULD_PUBLISH_LOGS_WHEN_RE_ENABLED:
        add_log(logging.ERROR, None, None, keep_log=False, call_notifiers=True)
    else:
        SHOULD_PUBLISH_LOGS_WHEN_RE_ENABLED = False
