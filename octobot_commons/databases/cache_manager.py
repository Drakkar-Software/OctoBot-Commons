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
import os
import json
import inspect
import hashlib

import octobot_commons.logging as logging
import octobot_commons.databases.adaptors as adaptors
import octobot_commons.databases.cache_timestamp_database as cache_timestamp_database
import octobot_commons.constants as common_constants
import octobot_commons.symbol_util as symbol_util
import octobot_commons.errors as common_errors


class CacheManager:
    """
    Manages cache as a global dict since caches can be accessed from live, backtesting and optimizers concurrently
    """

    CACHES = {}

    def __init__(self, database_adaptor=adaptors.TinyDBAdaptor):
        self.database_adaptor = database_adaptor
        self.logger = logging.get_logger(self.__class__.__name__)

    def get_cache(self, tentacle, tentacle_name, exchange_name, symbol, time_frame, tentacles_setup_config,
                  cache_type=cache_timestamp_database.CacheTimestampDatabase, open_if_missing=True):
        try:
            return self.__class__.CACHES[tentacle_name][exchange_name][symbol][time_frame].get_database()
        except KeyError:
            if open_if_missing:
                if tentacle_name not in self.__class__.CACHES:
                    self.__class__.CACHES[tentacle_name] = {}
                if exchange_name not in self.__class__.CACHES[tentacle_name]:
                    self.__class__.CACHES[tentacle_name][exchange_name] = {}
                if symbol not in self.__class__.CACHES[tentacle_name][exchange_name]:
                    self.__class__.CACHES[tentacle_name][exchange_name][symbol] = {}
                if tentacle is None:
                    raise RuntimeError("tentacle parameter must be set to get the associated cache path database")
                cache = self._open_or_create_cache_database(tentacle, exchange_name, symbol, time_frame,
                                                            tentacle_name, tentacles_setup_config, cache_type)
                self.__class__.CACHES[tentacle_name][exchange_name][symbol][time_frame] = cache
                return cache.get_database()
            raise common_errors.NoCacheValue(f"Cache is initialized for {tentacle_name} on {exchange_name} "
                                             f"{symbol} {time_frame}")

    def has_cache(self, tentacle_name, exchange_name, symbol, time_frame):
        try:
            return bool(self.__class__.CACHES[tentacle_name][exchange_name][symbol][time_frame])
        except KeyError:
            return False

    async def clear_cache(self, tentacle_name, exchange_name=None, symbol=None, time_frame=None):
        try:
            for cache in self._caches(tentacle_name, exchange_name, symbol, time_frame):
                await cache.clear()
            return True
        except KeyError:
            return False

    async def close_cache(self, tentacle_name, exchange_name=None, symbol=None, time_frame=None):
        try:
            for cache in self._caches(tentacle_name, exchange_name, symbol, time_frame):
                await cache.close()
            return True
        except KeyError:
            return False

    async def reset(self):
        for cache in self._caches(None, None, None, None):
            if cache.is_open():
                await cache.close()
        self.__class__.CACHES = {}

    def _caches(self, tentacle_name, exchange_name, symbol, time_frame):
        for _tentacle_name in [tentacle_name] if tentacle_name else list(self.__class__.CACHES):
            for _exchange_name in [exchange_name] if exchange_name else list(self.__class__.CACHES[_tentacle_name]):
                for _symbol in [symbol] if symbol else list(self.__class__.CACHES[_tentacle_name][_exchange_name]):
                    for _time_frame in [time_frame] if time_frame else list(
                            self.__class__.CACHES[_tentacle_name][_exchange_name][_symbol]):
                        yield self.__class__.CACHES[_tentacle_name][_exchange_name][_symbol][_time_frame]

    def _open_or_create_cache_database(self, tentacle, exchange, symbol, time_frame,
                                       tentacle_name, tentacles_setup_config, cache_type):
        cache_full_path = self.get_cache_path(tentacle, exchange, symbol, time_frame,
                                              tentacle_name, tentacles_setup_config)
        cache_dir = os.path.split(cache_full_path)[0]
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        return self._open_cache_database(cache_full_path, cache_type)

    def _open_cache_database(self, file_path, cache_type):
        """
        Override to use another cache database or adaptor
        :return: the cache database class
        """
        return _CacheWrapper(file_path, cache_type, self.database_adaptor)

    def get_cache_path(self, tentacle, exchange, symbol, time_frame, tentacle_name, tentacles_setup_config):
        try:
            return self.__class__.CACHES[tentacle_name][exchange][symbol][time_frame].get_path()
        except KeyError:
            sanitized_pair = symbol_util.merge_symbol(symbol) if symbol else symbol
            # warning: very slow, should be called as rarely as possible
            return os.path.join(common_constants.USER_FOLDER, common_constants.CACHE_FOLDER, tentacle_name,
                                exchange, sanitized_pair, time_frame,
                                self._code_hash(tentacle), self._config_hash(tentacle, tentacles_setup_config),
                                common_constants.CACHE_FILE)

    @staticmethod
    def _code_hash(tentacle) -> str:
        code_location = tentacle.get_script() if hasattr(tentacle, "get_script") else tentacle.__class__
        return hashlib.sha256(
            inspect.getsource(code_location).replace(" ", "").replace("\n", "").encode()
        ).hexdigest()[:common_constants.CACHE_HASH_SIZE]

    def _config_hash(self, tentacle, tentacles_setup_config) -> str:
        try:
            import octobot_tentacles_manager.api as tentacles_manager_api
            config = tentacle.specific_config if hasattr(tentacle, "specific_config") else \
                tentacles_manager_api.get_tentacle_config(tentacles_setup_config, tentacle.__class__)
            return hashlib.sha256(
                json.dumps(config).encode()
            ).hexdigest()[:common_constants.CACHE_HASH_SIZE]
        except ImportError:
            self.logger.error("octobot_tentacles_manager is required to use cache")


class _CacheWrapper:
    def __init__(self, file_path, cache_type, database_adaptor, **kwargs):
        self.file_path = file_path
        self.cache_type = cache_type
        self.database_adaptor = database_adaptor
        self.db_kwargs = kwargs
        self._cache_database = None
        self._db_path = None

    def get_database(self):
        if self._cache_database is None:
            self._cache_database = self.cache_type(self.file_path,
                                                   database_adaptor=self.database_adaptor,
                                                   **self.db_kwargs)
            self._db_path = self._cache_database.get_db_path()
        return self._cache_database

    def is_open(self):
        return self._cache_database is not None

    async def close(self):
        await self._cache_database.close()
        self._cache_database = None
        return True

    async def clear(self):
        await self._cache_database.clear()

    def get_path(self):
        return self._db_path
