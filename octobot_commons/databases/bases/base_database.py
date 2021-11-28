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

import octobot_commons.databases.adaptors as adaptors
import octobot_commons.databases.bases.document_database as document_database
import octobot_commons.databases.bases.database_cache as database_cache


class BaseDatabase:
    def __init__(self, file_path: str, database_adaptor=adaptors.TinyDBAdaptor, cache_size=None, **kwargs):
        if database_adaptor is not None:
            self._database = document_database.DocumentDatabase(database_adaptor(file_path, cache_size=cache_size,
                                                                                 **kwargs))
            self._database.initialize()
        self.are_data_initialized = False
        self.cache = database_cache.DatabaseCache()

    def get_db_path(self):
        return self._database.get_db_path()

    async def search(self):
        return await self._database.query_factory()

    async def count(self, table_name: str, query) -> int:
        return await self._database.count(table_name, query)

    async def flush(self):
        await self._database.flush()

    async def close(self):
        await self._database.close()

    def contains_x(self, table: str, x_val):
        return self.cache.contains_x(table, x_val)

    def contains_values(self, table: str, val_by_keys: dict):
        return self.cache.contains_values(table, val_by_keys)

    def __str__(self):
        return f"{self.__class__.__name__}, database: {self._database}"

    @classmethod
    @contextlib.asynccontextmanager
    async def database(cls, *args, with_lock=False, cache_size=None, database_adaptor=None, **kwargs):
        if with_lock:
            adaptor = kwargs.pop("database_adaptor", adaptors.TinyDBAdaptor)
            if adaptor is None:
                raise RuntimeError("database_adaptor parameter required")
            adaptor_instance = adaptor(*args, cache_size=cache_size, **kwargs)
            database = cls(*args, database_adaptor=database_adaptor, cache_size=cache_size, **kwargs)
            async with document_database.DocumentDatabase.locked_database(adaptor_instance) as db:
                database._database = db
                yield database
            return
        database = None
        try:
            database = cls(*args, cache_size=cache_size, **kwargs)
            yield database
        finally:
            if database is not None:
                await database.close()

    @staticmethod
    def get_serializable_value(value):
        return value.item() if isinstance(value, numpy.generic) else value
