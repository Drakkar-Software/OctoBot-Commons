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
from enum import Enum


class OctoBotEvaluatorsChannelsName(Enum):
    MATRIX = "Matrix"


class OctoBotBacktestingChannelsName(Enum):
    TIME_CHANNEL = "Time"


class OctoBotTradingChannelsName(Enum):
    TICKER_CHANNEL = "Ticker"
    MINI_TICKER_CHANNEL = "MiniTicker"
    RECENT_TRADES_CHANNEL = "RecentTrade"
    ORDER_BOOK_CHANNEL = "OrderBook"
    ORDER_BOOK_TICKER_CHANNEL = "OrderBookTicker"
    KLINE_CHANNEL = "Kline"
    OHLCV_CHANNEL = "OHLCV"
    TRADES_CHANNEL = "Trades"
    LIQUIDATIONS_CHANNEL = "Liquidations"
    ORDERS_CHANNEL = "Orders"
    BALANCE_CHANNEL = "Balance"
    BALANCE_PROFITABILITY_CHANNEL = "BalanceProfitability"
    POSITIONS_CHANNEL = "Positions"
    MODE_CHANNEL = "Mode"
    MARK_PRICE_CHANNEL = "MarkPrice"
    FUNDING_CHANNEL = "Funding"
