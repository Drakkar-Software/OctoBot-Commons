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
import time

from octobot_commons.timestamp_util import is_valid_timestamp, get_now_time, convert_timestamps_to_datetime


def test_is_valid_timestamp():
    assert not is_valid_timestamp(get_now_time())
    assert is_valid_timestamp(time.time())


def test_convert_timestamps_to_datetime():
    # assert convert_timestamps_to_datetime([123456789]) == ['29/11/73 22:33'] TODO fail on travis : https://travis-ci.org/Drakkar-Software/OctoBot-Commons/jobs/626908169
    pass
