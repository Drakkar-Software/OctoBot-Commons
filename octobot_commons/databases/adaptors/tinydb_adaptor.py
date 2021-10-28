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
except ImportError:
    pass

import octobot_commons.databases.adaptors.abstract_database_adaptor as abstract_database_adaptor


class TinyDBAdaptor(abstract_database_adaptor.AbstractDatabaseAdaptor):
    """
    TinyDBAdaptor is an AbstractDatabaseAdaptor implemented using tinydb: a minimal python only
    local document database
    """

    def __init__(self, file_path: str):
        """
        TinyDBAdaptor constructor
        :param file_path: path to the database file
        """
        super().__init__()
        self.database = tinydb.TinyDB(file_path)

    def insert(self, table_name: str, row: dict):
        """
        Insert dict data into the table_name table
        :param table_name: name of the table
        :param row: data to insert
        """
        self.database.table(table_name).insert(row)

    def insert_many(self, table_name: str, rows: list):
        """
        Insert multiple dict data into the table_name table
        :param table_name: name of the table
        :param rows: data to insert
        """
        self.database.table(table_name).insert_multiple(rows)

    def select(self, table_name: str, query) -> list:
        """
        Select data from the table_name table
        :param table_name: name of the table
        :param query: select query
        """
        return self.database.table(table_name).search(query)

    def count(self, table_name: str, query) -> int:
        """
        Counts documents in the table_name table
        :param table_name: name of the table
        :param query: select query
        """
        return self.database.table(table_name).count(query)

    def query_factory(self):
        """
        Creates a new empty select query
        """
        return tinydb.Query()
