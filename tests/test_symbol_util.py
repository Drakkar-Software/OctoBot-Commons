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
from octobot_commons.symbol_util import merge_symbol, split_symbol, merge_currencies, convert_symbol


def test_split_symbol():
    assert split_symbol("BTC/USDT") == ("BTC", "USDT")


def test_merge_symbol():
    assert merge_symbol("BTC/USDT") == "BTCUSDT"


def test_merge_currencies():
    assert merge_currencies("BTC", "USDT") == "BTC/USDT"


def test_convert_symbol():
    assert convert_symbol("BTC-USDT", symbol_separator="-") == "BTC/USDT"
