#  Drakkar-Software OctoBot
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
import abc
import functools
import asyncio

import octobot_commons.logging as bot_logging


class Authenticator:
    """
    Abstract class to be implemented when using authenticated requests
    """

    def __init__(self):
        self.logger: bot_logging.BotLogger = bot_logging.get_logger(
            self.__class__.__name__
        )
        self.initialized_event: asyncio.Event = None
        self.supports: None

    @abc.abstractmethod
    def login(self, username, password):
        """
        Used to trigger a login
        :param username: authentication username
        :param password: authentication password
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def logout(self):
        """
        Used to clear a logged in session
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_aiohttp_session(self):
        """
        Get the aiohttp authenticated session
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def is_logged_in(self):
        """
        :return: True when authenticated
        """
        raise NotImplementedError

    @abc.abstractmethod
    def ensure_token_validity(self):
        """
        Called before @authenticated methods to ensure authentication
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def is_initialized(self) -> bool:
        """
        Returns True when initialized
        :return:
        """
        raise NotImplementedError

    async def await_initialization(self, timeout):
        """
        Returns when initialized
        :return:
        """
        await asyncio.wait_for(self.initialized_event.wait(), timeout)


class FailedAuthentication(Exception):
    """
    Raised upon authentication failure
    """


class UnavailableError(Exception):
    """
    Raised upon website availability issues failure
    """


class AuthenticationError(Exception):
    """
    Raised upon authentication technical error, not on login/password issues
    """


class AuthenticationRequired(Exception):
    """
    Raised when an authentication is required
    """


def authenticated(func):
    """
    Annotation to required authentication for a method call
    :param func:
    :return:
    """

    @functools.wraps(func)
    def wrapped(self, *args, **kwargs):
        self.ensure_token_validity()
        return func(self, *args, **kwargs)

    return wrapped
