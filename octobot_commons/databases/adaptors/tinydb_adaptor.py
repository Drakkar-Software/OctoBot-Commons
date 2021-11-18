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
try:
    import tinydb
    import tinydb.storages
    import tinydb.middlewares
    import tinydb.table
except ImportError:
    pass

import octobot_commons.databases.adaptors.abstract_database_adaptor as abstract_database_adaptor


class TinyDBAdaptor(abstract_database_adaptor.AbstractDatabaseAdaptor):
    """
    TinyDBAdaptor is an AbstractDatabaseAdaptor implemented using tinydb: a minimal python only
    local document database.
    Warning: loads the whole file in RAM and must be closed to ensure writing
    """

    DEFAULT_WRITE_CACHE_SIZE = 5000

    def __init__(self, file_path: str, cache_size: int = None, **kwargs):
        """
        TinyDBAdaptor constructor.
        :param file_path: path to the database file
        :param cache_size: size of the in memory cache (number of operations before updating the file
        :param kwargs: unused
        """
        super().__init__(file_path)
        self.database = None
        self.cache_size = cache_size

    def initialize(self):
        """
        Initialize the database: opens the database file.
        """
        middleware = tinydb.middlewares.CachingMiddleware(tinydb.storages.JSONStorage)
        middleware.WRITE_CACHE_SIZE = self.cache_size or self.DEFAULT_WRITE_CACHE_SIZE
        self.database = tinydb.TinyDB(self.db_path, storage=middleware)

    async def select(self, table_name: str, query, uuid=None) -> list:
        """
        Select data from the table_name table
        :param table_name: name of the table
        :param query: select query
        :param uuid: id of the document
        """
        if uuid is None:
            return (
                self.database.table(table_name).search(query)
                if query
                else self.database.table(table_name).all()
            )
        return self.database.table(table_name).get(doc_id=uuid)

    async def tables(self) -> list:
        """
        Select tables
        """
        return list(self.database.tables())

    async def insert(self, table_name: str, row: dict) -> int:
        """
        Insert dict data into the table_name table
        :param table_name: name of the table
        :param row: data to insert
        """
        return self.database.table(table_name).insert(row)

    async def upsert(self, table_name: str, row: dict, query, uuid=None) -> int:
        """
        Insert or update dict data into the table_name table
        :param table_name: name of the table
        :param row: data to insert
        :param query: select query
        :param uuid: id of the document
        """
        if uuid is None:
            return self.database.table(table_name).upsert(row, query)
        return self.database.table(table_name).upsert(tinydb.table.Document(row, doc_id=uuid))

    async def insert_many(self, table_name: str, rows: list) -> list:
        """
        Insert multiple dict data into the table_name table
        :param table_name: name of the table
        :param rows: data to insert
        """
        return self.database.table(table_name).insert_multiple(rows)

    async def update(self, table_name: str, row: dict, query, uuid=None) -> list:
        """
        Select data from the table_name table
        :param table_name: name of the table
        :param row: data to update
        :param query: select query
        :param uuid: id of the document
        """
        if uuid is None:
            return self.database.table(table_name).update(row, query)
        return self.database.table(table_name).update(tinydb.table.Document(row, doc_id=uuid))

    async def delete(self, table_name: str, query, uuid=None) -> list:
        """
        Delete data from the table_name table
        :param table_name: name of the table
        :param query: select query
        :param uuid: id of the document
        """
        if uuid is None:
            return self.database.table(table_name).remove(query)
        return self.database.table(table_name).remove(doc_ids=(uuid,))

    async def count(self, table_name: str, query) -> int:
        """
        Counts documents in the table_name table
        :param table_name: name of the table
        :param query: select query
        """
        return self.database.table(table_name).count(query)

    async def query_factory(self):
        """
        Creates a new empty select query
        """
        return tinydb.Query()

    async def flush(self):
        """
        Flushes the database cache
        """
        return self.database.storage.flush()

    async def close(self):
        """
        Closes the database
        """
        return self.database.close()
