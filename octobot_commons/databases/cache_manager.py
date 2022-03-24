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

import octobot_commons.logging as logging
import octobot_commons.databases.document_database_adaptors as adaptors
import octobot_commons.databases.implementations.cache_timestamp_database as cache_timestamp_database
import octobot_commons.databases.databases_util as databases_util
import octobot_commons.constants as common_constants
import octobot_commons.symbol_util as symbol_util
import octobot_commons.errors as common_errors
import octobot_commons.event_tree as event_tree


class CacheManager:
    """
    Manages cache as a global dict since caches can be accessed from live, backtesting and optimizers concurrently
    """

    CACHES = event_tree.EventTree()
    DEFAULT_CONFIG_IDENTIFIER = "default"
    UNPROVIDED_CACHE_IDENTIFIER = "_unprovided"

    def __init__(self, database_adaptor=adaptors.TinyDBAdaptor):
        self.database_adaptor = database_adaptor
        self.logger = logging.get_logger(self.__class__.__name__)

    def get_cache(self, tentacle, tentacle_name, exchange_name, symbol, time_frame, config_name,
                  tentacles_setup_config, tentacles_requirements,
                  cache_type=cache_timestamp_database.CacheTimestampDatabase, open_if_missing=True) -> tuple:
        identifier = config_name or self.DEFAULT_CONFIG_IDENTIFIER
        cache_path = [tentacle_name, exchange_name, symbol, time_frame, identifier]
        try:
            return self.__class__.CACHES.get_node(cache_path).node_value.get_database()
        except event_tree.NodeExistsError:
            if open_if_missing:
                if tentacle is None:
                    config_names = self.__class__.CACHES.get_children_keys(cache_path[:-1])
                    available_config_names = \
                        f"Available configuration names: {config_names}. " if config_names else ""
                    raise common_errors.UninitializedCache(
                        f"No initialized cache for {tentacle_name} tentacle with config name: {config_name}. "
                        f"{available_config_names}"
                        f"The tentacle parameter must be set to get the associated cache database path")
                cache = self._open_or_create_cache_database(tentacle, exchange_name, symbol, time_frame,
                                                            tentacle_name, identifier,
                                                            tentacles_setup_config, cache_type, tentacles_requirements)
                self.__class__.CACHES.set_node_at_path(cache, None, cache_path)
                return cache.get_database()
            raise common_errors.NoCacheValue(f"Cache is initialized for {tentacle_name} on {exchange_name} "
                                             f"{symbol} {time_frame}")

    def has_cache(self, tentacle_name, exchange_name, symbol, time_frame, config_name=None):
        identifier = config_name or self.DEFAULT_CONFIG_IDENTIFIER
        try:
            return bool(self.__class__.CACHES.get_node([tentacle_name, exchange_name, symbol, time_frame, identifier]))
        except event_tree.NodeExistsError:
            return False

    def get_cache_registered_requirements(self, tentacle_name, exchange_name, symbol, time_frame, config_name=None):
        identifier = config_name or self.DEFAULT_CONFIG_IDENTIFIER
        return self.__class__.CACHES.get_node([tentacle_name, exchange_name, symbol, time_frame, identifier]).\
            node_value.tentacles_requirements

    def get_cache_previous_db_metadata(self, tentacle_name, exchange_name, symbol, time_frame, config_name=None):
        identifier = config_name or self.DEFAULT_CONFIG_IDENTIFIER
        return self.__class__.CACHES.get_node([tentacle_name, exchange_name, symbol, time_frame, identifier]).\
            node_value.previous_db_metadata

    async def clear_cache(self,
                          tentacle_name,
                          exchange_name=UNPROVIDED_CACHE_IDENTIFIER,
                          symbol=UNPROVIDED_CACHE_IDENTIFIER,
                          time_frame=UNPROVIDED_CACHE_IDENTIFIER,
                          config_name=UNPROVIDED_CACHE_IDENTIFIER):
        try:
            for cache, _ in self._caches(tentacle_name, exchange_name, symbol, time_frame, config_name):
                await cache.node_value.clear()
            return True
        except event_tree.NodeExistsError:
            return False

    async def reset_cache(self, tentacle_name, exchange_name, symbol, time_frame, config_name):
        identifier = config_name or self.DEFAULT_CONFIG_IDENTIFIER
        cache = self.__class__.CACHES.delete_node([tentacle_name, exchange_name, symbol, time_frame, identifier])
        await cache.node_value.close()

    async def close_cache(self,
                          tentacle_name,
                          exchange_name=UNPROVIDED_CACHE_IDENTIFIER,
                          symbol=UNPROVIDED_CACHE_IDENTIFIER,
                          time_frame=UNPROVIDED_CACHE_IDENTIFIER,
                          config_name=UNPROVIDED_CACHE_IDENTIFIER,
                          reset_cache_db_ids=False):
        try:
            to_remove_caches = []
            for cache, identifiers in self._caches(tentacle_name, exchange_name, symbol, time_frame, config_name):
                await cache.node_value.close()
                to_remove_caches.append(identifiers)
            if reset_cache_db_ids:
                # remove cache from caches to force complete reopen of the cache db
                # (might be at a different place)
                for identifier in to_remove_caches:
                    self.__class__.CACHES.delete_node(identifier)
            return True
        except event_tree.NodeExistsError:
            return False

    async def reset(self):
        for cache, _ in self._caches():
            if cache.node_value.is_open():
                await cache.node_value.close()
        self.__class__.CACHES = event_tree.EventTree()

    def _caches(self,
                tentacle_name=UNPROVIDED_CACHE_IDENTIFIER,
                exchange_name=UNPROVIDED_CACHE_IDENTIFIER,
                symbol=UNPROVIDED_CACHE_IDENTIFIER,
                time_frame=UNPROVIDED_CACHE_IDENTIFIER,
                config_name=UNPROVIDED_CACHE_IDENTIFIER):
        path = []
        for element in (tentacle_name, exchange_name, symbol, time_frame, config_name):
            if element == self.UNPROVIDED_CACHE_IDENTIFIER:
                break
            else:
                path.append(element)
        if self.__class__.CACHES.get_children_keys(path):
            return self.__class__.CACHES.get_nested_children_with_path(path)
        # no cache value
        return []

    def _open_or_create_cache_database(self, tentacle, exchange, symbol, time_frame,
                                       tentacle_name, identifier, tentacles_setup_config,
                                       cache_type, tentacles_requirements):
        cache_full_path = self.get_cache_or_build_path(
            tentacle, exchange, symbol, time_frame,
            tentacle_name, identifier, tentacles_setup_config, tentacles_requirements)
        cache_dir = os.path.split(cache_full_path)[0]
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        return self._open_cache_database(cache_full_path, cache_type, tentacles_requirements)

    def _open_cache_database(self, file_path, cache_type, tentacles_requirements):
        """
        Override to use another cache database or adaptor
        :return: the cache database class
        """
        return databases_util.CacheWrapper(file_path, cache_type, self.database_adaptor, tentacles_requirements)

    def get_cache_or_build_path(self, tentacle, exchange, symbol, time_frame, tentacle_name, config_name,
                                tentacles_setup_config, tentacles_requirements):
        identifier = config_name or self.DEFAULT_CONFIG_IDENTIFIER
        try:
            return self.__class__.CACHES.get_node([tentacle_name, exchange, symbol, time_frame, identifier]).\
                node_value.get_path()
        except event_tree.NodeExistsError:
            sanitized_pair = symbol_util.merge_symbol(symbol) if symbol else symbol
            required_tentacles = tentacles_requirements.get_all_required_tentacles(False)
            # ensure tentacles requirements are snapshotting the configuration that was used to build the
            # cache identifier
            tentacles_requirements.synchronize_tentacles_config()
            identifying_tentacles = [tentacle] + required_tentacles
            # warning: very slow, should be called as rarely as possible
            code_hash, config_hash = self._tentacles_hashes(identifying_tentacles, tentacles_setup_config)
            return os.path.join(common_constants.USER_FOLDER, common_constants.CACHE_FOLDER, tentacle_name,
                                exchange, sanitized_pair, time_frame,
                                code_hash, config_hash,
                                common_constants.CACHE_FILE)

    @staticmethod
    def _tentacles_hashes(identifying_tentacles, tentacles_setup_config) -> (str, str):
        try:
            import octobot_tentacles_manager.api
            return \
                octobot_tentacles_manager.api.get_code_hash(identifying_tentacles)[:common_constants.CACHE_HASH_SIZE], \
                octobot_tentacles_manager.api.get_config_hash(
                    identifying_tentacles,
                    tentacles_setup_config
                )[:common_constants.CACHE_HASH_SIZE]
        except ImportError as e:
            raise ImportError("octobot_tentacles_manager is required to use cache") from e
