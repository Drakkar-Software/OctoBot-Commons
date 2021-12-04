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
import octobot_commons.databases.bases.base_database as base_database


class DBWriter(base_database.BaseDatabase):

    async def log(self, table_name: str, row: dict):
        self.cache.register(table_name, row)
        return await self._database.insert(table_name, row)

    async def update(self, table_name: str, row: dict, query):
        return await self._database.update(table_name, row, query)

    async def upsert(self, table_name: str, row: dict, query, uuid=None):
        return await self._database.upsert(table_name, row, query, uuid=uuid)

    async def update_many(self, table_name: str, update_values: list):
        return await self._database.update_many(table_name, update_values)

    async def delete(self, table_name: str, query):
        return await self._database.delete(table_name, query)

    async def delete_all(self, table_name: str):
        return await self._database.delete(table_name, None)

    async def log_many(self, table_name: str, rows: list):
        for row in rows:
            self.cache.register(table_name, row)
        return await self._database.insert_many(table_name, rows)

    @staticmethod
    def get_value_from_array(array, index, multiplier=1):
        if array is None:
            return None
        return array[index] * multiplier
