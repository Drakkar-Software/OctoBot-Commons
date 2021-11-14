# pylint: disable=W0613
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


class AbstractDatabaseAdaptor:
    """
    AbstractDatabaseAdaptor is an interface listing document databases public methods
    """

    def __init__(self, db_path: str, **kwargs):
        """
        TinyDBAdaptor constructor
        :param db_path: database path
        :param kwargs: kwargs to pass to the underlying db driver constructor
        """
        self.db_path = db_path

    async def select(self, table_name: str, query) -> list:
        """
        Select data from the table_name table
        :param table_name: name of the table
        :param query: select query
        """
        raise NotImplementedError("select is not implemented")

    async def insert(self, table_name: str, row: dict) -> int:
        """
        Insert dict data into the table_name table
        :param table_name: name of the table
        :param row: data to insert
        """
        raise NotImplementedError("insert is not implemented")

    async def tables(self) -> list:
        """
        Select tables
        """
        raise NotImplementedError("tables is not implemented")

    async def insert_many(self, table_name: str, rows: list) -> list:
        """
        Insert multiple dict data into the table_name table
        :param table_name: name of the table
        :param rows: data to insert
        """
        raise NotImplementedError("insert_many is not implemented")

    async def update(self, table_name: str, row: dict, query) -> list:
        """
        Select data from the table_name table
        :param table_name: name of the table
        :param row: data to update
        :param query: select query
        """
        raise NotImplementedError("update is not implemented")

    async def delete(self, table_name: str, query) -> list:
        """
        Delete data from the table_name table
        :param table_name: name of the table
        :param query: select query
        """
        raise NotImplementedError("delete is not implemented")

    async def count(self, table_name: str, query) -> int:
        """
        Counts documents in the table_name table
        :param table_name: name of the table
        :param query: select query
        """
        raise NotImplementedError("count is not implemented")

    async def query_factory(self):
        """
        Creates a new empty select query
        """
        raise NotImplementedError("query_factory is not implemented")

    async def close(self):
        """
        Closes the database
        """
        raise NotImplementedError("close is not implemented")
