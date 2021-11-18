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
import octobot_commons.databases.bases as bases
import octobot_commons.enums as commons_enums
import octobot_commons.errors as errors


class CacheTimestampDatabase(bases.CacheDatabase):
    async def get(self, timestamp: float, name: str = commons_enums.CacheDatabaseColumns.VALUE.value) -> dict:
        try:
            return await self._get_from_local_cache(commons_enums.CacheDatabaseColumns.TIMESTAMP.value, timestamp, name)
        except KeyError:
            try:
                value = (await self._database.select(self.CACHE_TABLE, await self._timestamp_query(timestamp)))[0][name]
                await self._ensure_local_cache(commons_enums.CacheDatabaseColumns.TIMESTAMP.value, update=True)
                return value
            except IndexError:
                raise errors.NoCacheValue(f"No cache value associated to {timestamp}")
            except KeyError:
                raise errors.NoCacheValue(f"No {name} value associated to {timestamp} cache.")

    async def set(self, timestamp: float, value, name: str = commons_enums.CacheDatabaseColumns.VALUE.value) -> None:
        await self._ensure_metadata()
        if await self._needs_update(commons_enums.CacheDatabaseColumns.TIMESTAMP.value, timestamp, name, value):
            set_value = {
                commons_enums.CacheDatabaseColumns.TIMESTAMP.value: timestamp,
                name: value,
            }
            await self._database.upsert(self.CACHE_TABLE, set_value, await self._timestamp_query(timestamp))
            if timestamp in self._local_cache:
                self._local_cache[timestamp][name] = value
            else:
                self._local_cache[timestamp] = {
                    name: value
                }

    async def contains(self, timestamp: float) -> bool:
        return await self._database.count(self.CACHE_TABLE, await self._timestamp_query(timestamp)) > 0

    async def _timestamp_query(self, timestamp):
        return (await self._database.query_factory()).t == timestamp
