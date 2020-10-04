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
import enum


class TimeFrames(enum.Enum):
    """
    OctoBot supported time frames values
    """

    ONE_MINUTE = "1m"
    THREE_MINUTES = "3m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"
    ONE_HOUR = "1h"
    TWO_HOURS = "2h"
    THREE_HOURS = "3h"
    FOUR_HOURS = "4h"
    SIX_HOURS = "6h"
    HEIGHT_HOURS = "8h"
    TWELVE_HOURS = "12h"
    ONE_DAY = "1d"
    THREE_DAYS = "3d"
    ONE_WEEK = "1w"
    ONE_MONTH = "1M"


TimeFramesMinutes = {
    TimeFrames.ONE_MINUTE: 1,
    TimeFrames.THREE_MINUTES: 3,
    TimeFrames.FIVE_MINUTES: 5,
    TimeFrames.FIFTEEN_MINUTES: 15,
    TimeFrames.THIRTY_MINUTES: 30,
    TimeFrames.ONE_HOUR: 60,
    TimeFrames.TWO_HOURS: 120,
    TimeFrames.THREE_HOURS: 180,
    TimeFrames.FOUR_HOURS: 240,
    TimeFrames.SIX_HOURS: 360,
    TimeFrames.HEIGHT_HOURS: 480,
    TimeFrames.TWELVE_HOURS: 720,
    TimeFrames.ONE_DAY: 1440,
    TimeFrames.THREE_DAYS: 4320,
    TimeFrames.ONE_WEEK: 10080,
    TimeFrames.ONE_MONTH: 43200,
}


class PriceIndexes(enum.Enum):
    """
    Default candle price index correspondence
    """

    IND_PRICE_TIME = 0
    IND_PRICE_OPEN = 1
    IND_PRICE_HIGH = 2
    IND_PRICE_LOW = 3
    IND_PRICE_CLOSE = 4
    IND_PRICE_VOL = 5


class PlatformsName(enum.Enum):
    """
    OctoBot supported platforms name
    """

    WINDOWS = "nt"
    LINUX = "posix"
    MAC = "mac"


class OctoBotTypes(enum.Enum):
    """
    OctoBot running types
    """

    BINARY = "binary"
    PYTHON = "python"
    DOCKER = "docker"


class MarkdownFormat(enum.Enum):
    """
    Markdown formating
    """

    ITALIC = "_"
    BOLD = "*"
    CODE = "`"
    IGNORE = 1
    NONE = 0


class OctoBotChannelSubjects(enum.Enum):
    """
    OctoBot Channel subjects
    """

    NOTIFICATION = "notification"
    CREATION = "creation"
    UPDATE = "update"
    DELETION = "deletion"
    ERROR = "error"
