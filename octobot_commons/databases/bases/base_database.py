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
import contextlib
import numpy

import octobot_commons.databases.document_database_adaptors as adaptors
import octobot_commons.databases.bases.document_database as document_database
import octobot_commons.databases.database_caches as database_cache


class BaseDatabase:
    def __init__(self, file_path: str, database_adaptor=adaptors.TinyDBAdaptor, cache_size=None, **kwargs):
        if database_adaptor is not None:
            self._database = document_database.DocumentDatabase(database_adaptor(file_path, cache_size=cache_size,
                                                                                 **kwargs))
            self._database.initialize()
        self.are_data_initialized = False
        self.are_data_initialized_by_key = {}
        self.cache = database_cache.GenericDatabaseCache()

    def set_initialized_flags(self, value, keys=None):
        self.are_data_initialized = value
        for key in keys or self.are_data_initialized_by_key.keys():
            self.are_data_initialized_by_key[key] = value

    def get_db_path(self):
        return self._database.get_db_path()

    async def search(self, dict_query: dict = None):
        if dict_query is None:
            return await self._database.query_factory()
        return (await self._database.query_factory()).fragment(dict_query)

    async def count(self, table_name: str, query) -> int:
        return await self._database.count(table_name, query)

    async def flush(self):
        await self._database.flush()

    async def hard_reset(self):
        return await self._database.hard_reset()

    async def close(self):
        await self.flush()
        await self._database.close()

    async def clear(self):
        self.cache.clear()

    async def contains_row(self, table: str, row: dict):
        if self.cache.contains_row(table, row):
            return True
        return await self.count(table, await self.search(row)) > 0

    def __str__(self):
        return f"{self.__class__.__name__}, database: {self._database}"

    @classmethod
    def _create_database(cls, *args, required_adaptor=False, cache_size=None, database_adaptor=None, **kwargs):
        if required_adaptor:
            adaptor = kwargs.pop("database_adaptor", adaptors.TinyDBAdaptor)
            if adaptor is None:
                raise RuntimeError("database_adaptor parameter required")
            adaptor_instance = adaptor(*args, cache_size=cache_size, **kwargs)
            return cls(*args, database_adaptor=database_adaptor, cache_size=cache_size, **kwargs), adaptor_instance
        return cls(*args, cache_size=cache_size, **kwargs), None

    @classmethod
    @contextlib.asynccontextmanager
    async def database(cls, *args, with_lock=False, cache_size=None, database_adaptor=None, **kwargs):
        database, adaptor_instance = cls._create_database(*args, required_adaptor=with_lock, cache_size=cache_size,
                                                          database_adaptor=database_adaptor, **kwargs)
        if with_lock:
            async with document_database.DocumentDatabase.locked_database(adaptor_instance) as db:
                database._database = db
                yield database
                # context manager is taking care of closing the database
            return
        try:
            yield database
        finally:
            await database.close()

    @staticmethod
    def get_serializable_value(value):
        return value.item() if isinstance(value, numpy.generic) else value
