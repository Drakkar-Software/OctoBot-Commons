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


class ConfigError(Exception):
    """
    Config related Exception
    """


class NoProfileError(Exception):
    """
    Profile related Exception: raised when the current profile can't be found and default profile can't be loaded
    """


class ProfileRemovalError(Exception):
    """
    Profile related Exception: raised when the current profile can't be can't be removed
    """


class ConfigEvaluatorError(Exception):
    """
    Evaluator config related Exception
    """


class ConfigTradingError(Exception):
    """
    Trading config related Exception
    """


class TentacleNotFound(Exception):
    """
    Tentacle not found related Exception
    """


class NoCacheValue(Exception):
    """
    Raised when a cache value is selected but is not available in database
    """


class DatabaseNotFoundError(Exception):
    """
    Raised when a database can't be found
    """
