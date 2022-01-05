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
                if self._is_empty_database:
                    raise errors.NoCacheValue(f"No cache value associated to {timestamp}")
                value = (await self._database.select(self.CACHE_TABLE, await self._timestamp_query(timestamp)))[0][name]
                await self._ensure_local_cache(commons_enums.CacheDatabaseColumns.TIMESTAMP.value, update=True)
                return value
            except IndexError:
                raise errors.NoCacheValue(f"No cache value associated to {timestamp}")
            except KeyError:
                raise errors.NoCacheValue(f"No {name} value associated to {timestamp} cache.")

    async def get_values(self, timestamp: float, name: str = commons_enums.CacheDatabaseColumns.VALUE.value, limit=-1) -> list:
        try:
            await self._ensure_local_cache(commons_enums.CacheDatabaseColumns.TIMESTAMP.value)
            values = [
                values[name]
                for value_timestamp, values in self._local_cache.items()
                if value_timestamp <= timestamp and name in values
            ]
            if limit != -1:
                return values[-limit:]
            return values
        except IndexError:
            raise errors.NoCacheValue(f"No cache value associated to {name}")
        except KeyError:
            raise errors.NoCacheValue(f"No {name} value associated to {name} cache.")

    async def set(self, timestamp: float, value, name: str = commons_enums.CacheDatabaseColumns.VALUE.value) -> None:
        await self._ensure_metadata()
        saved_value = self.get_serializable_value(value)
        if await self._needs_update(commons_enums.CacheDatabaseColumns.TIMESTAMP.value, timestamp, name, saved_value):
            uuid = None
            set_value = {
                commons_enums.CacheDatabaseColumns.TIMESTAMP.value: timestamp,
                name: saved_value,
            }
            if timestamp in self._local_cache:
                # set uuid in case this value already exist in db
                uuid = self._local_cache[timestamp].get(self.UUID_KEY)
                self._local_cache[timestamp][commons_enums.CacheDatabaseColumns.TIMESTAMP.value] = timestamp
                self._local_cache[timestamp][name] = saved_value
            else:
                self._local_cache[timestamp] = set_value
            await self.upsert(
                self.CACHE_TABLE,
                set_value,
                None,
                uuid=uuid,
                cache_query={
                    commons_enums.CacheDatabaseColumns.TIMESTAMP.value: timestamp
                }
            )

    async def set_values(self, timestamps, values, name: str = commons_enums.CacheDatabaseColumns.VALUE.value) -> None:
        # 1. update values that exist already (can't be done all at once and is slower)
        handled_timestamps = set()
        for timestamp, value in zip(timestamps, values):
            if timestamp in self._local_cache and name in self._local_cache[timestamp]:
                await self.set(timestamp, value, name=name)
                handled_timestamps.add(timestamp)
        # 2. use optimized multiple insert to speed up the database insert operation
        await self._set_non_existent_values(
            ((timestamp, value) for timestamp, value in zip(timestamps, values) if timestamp not in handled_timestamps),
            name=name
        )

    async def _set_non_existent_values(self, timestamps_and_values, name):
        await self._ensure_metadata()
        rows = []
        for timestamp, value in timestamps_and_values:
            if timestamp in self._local_cache:
                row = self._local_cache[timestamp]
                row[name] = value
            else:
                row = {
                    commons_enums.CacheDatabaseColumns.TIMESTAMP.value: timestamp,
                    name: value
                }
                self._local_cache[timestamp] = row
            rows.append(row)
        await self.log_many(self.CACHE_TABLE, rows)

    async def _timestamp_query(self, timestamp):
        return (await self._database.query_factory()).t == timestamp

    async def get_cache(self):
        # relies on the fact that python dicts keep order
        return sorted(await self._database.select(self.CACHE_TABLE, None),
                      key=lambda x: x[commons_enums.CacheDatabaseColumns.TIMESTAMP.value])
