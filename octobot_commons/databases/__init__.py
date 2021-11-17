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


from octobot_commons.databases import adaptors
from octobot_commons.databases import bases

from octobot_commons.databases import reader
from octobot_commons.databases import writer
from octobot_commons.databases import writer_reader
from octobot_commons.databases import cache_timestamp_database

from octobot_commons.databases.adaptors import (
    AbstractDatabaseAdaptor,
    TinyDBAdaptor,
)

from octobot_commons.databases.bases import (
    DocumentDatabase,
    DatabaseCache,
    BaseDatabase,
)

from octobot_commons.databases.reader import (
    DBReader,
)

from octobot_commons.databases.writer import (
    DBWriter,
)

from octobot_commons.databases.writer_reader import (
    DBWriterReader,
)

from octobot_commons.databases.cache_timestamp_database import (
    CacheTimestampDatabase,
)


__all__ = [
    "AbstractDatabaseAdaptor",
    "TinyDBAdaptor",
    "DocumentDatabase",
    "DatabaseCache",
    "BaseDatabase",
    "DBReader",
    "DBWriter",
    "DBWriterReader",
    "CacheTimestampDatabase",
]
