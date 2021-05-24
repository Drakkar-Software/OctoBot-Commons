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


class Authenticator:

    @abc.abstractmethod
    def login(self, username, password):
        raise NotImplementedError

    @abc.abstractmethod
    def logout(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_aiohttp_session(self):
        raise NotImplementedError


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
    @functools.wraps(func)
    def wrapped(self, *args, **kwargs):
        self.ensure_token_validity()
        return func(self, *args, **kwargs)
    return wrapped
