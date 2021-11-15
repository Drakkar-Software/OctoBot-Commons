#  Drakkar-Software OctoBot-Trading
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


class DocumentDatabase:
    """
    DocumentDatabase is used to communicate with an underlying database
    """

    def __init__(self, database_adaptor):
        """
        DocumentDatabase constructor
        :param database_adaptor: database adaptor
        """
        self.adaptor = database_adaptor

    def initialize(self):
        """
        Initialize the database adaptor.
        """
        self.adaptor.initialize()

    def get_db_path(self):
        """
        Select database path
        """
        return self.adaptor.db_path

    async def select(self, table_name: str, query) -> list:
        """
        Select data from the table_name table
        :param table_name: name of the table
        :param query: select query
        """
        return await self.adaptor.select(table_name, query)

    async def tables(self) -> list:
        """
        Select tables
        """
        return await self.adaptor.tables()

    async def insert(self, table_name: str, row: dict) -> int:
        """
        Insert dict data into the table_name table
        :param table_name: name of the table
        :param row: data to insert
        """
        return await self.adaptor.insert(table_name, row)

    async def insert_many(self, table_name: str, rows: list) -> list:
        """
        Insert multiple dict data into the table_name table
        :param table_name: name of the table
        :param rows: data to insert
        """
        return await self.adaptor.insert_many(table_name, rows)

    async def update(self, table_name: str, row: dict, query: dict) -> list:
        """
        Insert dict data into the table_name table
        :param table_name: name of the table
        :param row: data to update
        :param query: select statement
        """
        return await self.adaptor.update(table_name, row, query)

    async def delete(self, table_name: str, query) -> list:
        """
        Delete data from the table_name table
        :param table_name: name of the table
        :param query: select query
        """
        return await self.adaptor.delete(table_name, query)

    async def count(self, table_name: str, query) -> int:
        """
        Counts documents in the table_name table
        :param table_name: name of the table
        :param query: select query
        """
        return await self.adaptor.count(table_name, query)

    async def query_factory(self):
        """
        Creates a new empty select query
        """
        return await self.adaptor.query_factory()

    async def flush(self):
        """
        Flushes the database cache
        """
        return await self.adaptor.flush()

    async def close(self):
        """
        Closes the database
        """
        return await self.adaptor.close()

    @classmethod
    @contextlib.asynccontextmanager
    async def locked_database(cls, *args, **kwargs):
        """
        Instantiate and then ensure lock is acquired before initializing the database.
        Closes the database and then releases the lock when exiting
        :param args: args to pass to the database constructor
        :param kwargs: kwargs to pass to the database constructor
        """
        instance = None
        try:
            instance = cls(*args, **kwargs)
            if instance.adaptor.is_multiprocessing():
                await instance.adaptor.acquire()
            instance.initialize()
            yield instance
        finally:
            if instance is not None:
                try:
                    await instance.close()
                finally:
                    if instance.adaptor.is_multiprocessing():
                        await instance.adaptor.release()
