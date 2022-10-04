# pylint: disable=C0103
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
    ONE_YEAR = "1y"


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
    TimeFrames.ONE_YEAR: 524160,
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


class PriceStrings(enum.Enum):
    """
    Default candle price str
    """

    STR_PRICE_TIME = "time"
    STR_PRICE_CLOSE = "close"
    STR_PRICE_OPEN = "open"
    STR_PRICE_HIGH = "high"
    STR_PRICE_LOW = "low"
    STR_PRICE_VOL = "vol"


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


class UserCommands(enum.Enum):
    """
    Allowed user commands
    """

    RELOAD_CONFIG = "reload_config"
    RELOAD_SCRIPT = "reload_script"
    CLEAR_PLOTTING_CACHE = "clear_plotting_cache"
    CLEAR_SIMULATED_ORDERS_CACHE = "clear_simulated_orders_cache"
    CLEAR_SIMULATED_TRADES_CACHE = "clear_simulated_trades_cache"
    CLEAR_SIMULATED_TRANSACTIONS_CACHE = "clear_simulated_transactions_cache"


class MultiprocessingLocks(enum.Enum):
    """
    Keys to multiprocessing lock
    """

    DBLock = "db_lock"


class CacheDatabaseTables(enum.Enum):
    """
    Tables in cache databases
    """

    CACHE = "cache"
    METADATA = "metadata"


class CacheDatabaseColumns(enum.Enum):
    """
    Keys/columns in cache databases tables
    """

    TIMESTAMP = "t"
    VALUE = "v"
    TYPE = "ty"
    TRIGGERED_AFTER_CANDLES_CLOSE = "triggered_after_candles_close"


class PlotAttributes(enum.Enum):
    KIND = "kind"
    X = "x"
    Y = "y"
    OPEN = "open"
    HIGH = "high"
    LOW = "low"
    CLOSE = "close"
    VOLUME = "volume"
    TITLE = "title"
    TEXT = "text"
    SUB_ELEMENTS = "sub_elements"
    ELEMENTS = "elements"
    NAME = "name"
    DATA = "data"
    X_TYPE = "x_type"
    Y_TYPE = "y_type"
    MODE = "mode"
    LINE_SHAPE = "line_shape"
    OWN_XAXIS = "own_xaxis"
    OWN_YAXIS = "own_yaxis"
    SIDE = "side"
    VALUE = "value"
    CONFIG = "config"
    SCHEMA = "schema"
    TENTACLE = "tentacle"
    TENTACLE_TYPE = "tentacle_type"
    COLUMNS = "columns"
    ROWS = "rows"
    SEARCHES = "searches"
    IS_HIDDEN = "is_hidden"
    TYPE = "type"
    COLOR = "color"
    HTML = "html"
    SIZE = "size"
    SYMBOL = "symbol"


class BacktestingMetadata(enum.Enum):
    ID = "id"
    GAINS = "gains"
    PERCENT_GAINS = "% gains"
    END_PORTFOLIO = "end portfolio"
    START_PORTFOLIO = "start portfolio"
    WIN_RATE = "% win rate"
    DRAW_DOWN = "% draw down"
    COEFFICIENT_OF_DETERMINATION_MAX_BALANCE = "R² max balance"
    COEFFICIENT_OF_DETERMINATION_END_BALANCE = "R² end balance"
    SYMBOLS = "symbols"
    TIME_FRAMES = "time frames"
    START_TIME = "start time"
    END_TIME = "end time"
    DURATION = "duration"
    ENTRIES = "entries"
    WINS = "wins"
    LOSES = "loses"
    TRADES = "trades"
    TIMESTAMP = "timestamp"
    NAME = "name"
    LEVERAGE = "leverage"
    OPTIMIZATION_CAMPAIGN = "optimization campaign"
    USER_INPUTS = "user inputs"
    BACKTESTING_FILES = "backtesting files"
    CHILDREN = "children"
    OPTIMIZER_ID = "optimizer id"
    EXCHANGE = "exchange"


class DBRows(enum.Enum):
    REFERENCE_MARKET = "ref_market"
    EXCHANGE = "exchange"
    EXCHANGES = "exchanges"
    FUTURE_CONTRACTS = "future_contracts"
    PAIR = "pair"
    TIME_FRAME = "time_frame"
    VALUE = "value"
    START_TIME = "start_time"
    END_TIME = "end_time"
    TRADING_TYPE = "trading_type"
    SYMBOLS = "symbols"


class PlotCharts(enum.Enum):
    MAIN_CHART = "main-chart"
    SUB_CHART = "sub-chart"


class DisplayedElementTypes(enum.Enum):
    CHART = "chart"
    INPUT = "input"
    TABLE = "table"
    VALUE = "value"


class DBTables(enum.Enum):
    METADATA = "metadata"
    INPUTS = "inputs"
    PORTFOLIO = "portfolio"
    ORDERS = "all_orders"
    TRADES = "all_trades"
    TRANSACTIONS = "all_transactions"
    CANDLES = "candles"
    CANDLES_SOURCE = "candles_source"
    CACHE_SOURCE = "cache_source"
    SYMBOL = "symbol"
    FEES_AMOUNT = "fees_amount"
    FEES_CURRENCY = "fees_currency"


class ActivationTopics(enum.Enum):
    """
    Events that can trigger actions
    """

    FULL_CANDLES = "once per bar close"
    IN_CONSTRUCTION_CANDLES = "once per second (Live Price)"
    RECENT_TRADES = "recent trades"
    EVALUATION_CYCLE = "after evaluators"


class DataBaseOrderBy(enum.Enum):
    """
    Database orders
    """

    ASC = "ASC"
    DESC = "DESC"


class DataBaseOperations(enum.Enum):
    """
    Database operators
    """

    SUP = ">"
    INF = "<"
    EQUALS = "="
    INF_EQUALS = f"{INF}{EQUALS}"
    SUP_EQUALS = f"{SUP}{EQUALS}"


class RunDatabases(enum.Enum):
    """
    Database identifiers
    """

    HISTORY = "history"
    LIVE = "live"
    BACKTESTING = "backtesting"
    OPTIMIZER = "optimizer"
    OPTIMIZER_RUNS_SCHEDULE_DB = "runs_schedule"
    RUN_DATA_DB = "run_data"
    PORTFOLIO_VALUE_DB = "portfolio_value"
    HISTORICAL_PORTFOLIO_VALUE = "historical_portfolio_value"
    ORDERS_DB = "orders"
    TRADES_DB = "trades"
    TRANSACTIONS_DB = "transactions"
    EXCHANGES = "exchanges"
    METADATA = "metadata"


class LogicalOperators(enum.Enum):
    """
    Logical operators
    """

    LOWER_THAN = "lower_than"
    HIGHER_THAN = "higher_than"
    LOWER_OR_EQUAL_TO = "lower_or_equal_to"
    HIGHER_OR_EQUAL_TO = "higher_or_equal_to"
    EQUAL_TO = "equal_to"
    DIFFERENT_FROM = "different_from"


class CommunityFeedAttrs(enum.Enum):
    ID = "u"
    STREAM_ID = "i"
    VALUE = "s"
    VERSION = "v"
    TIMESTAMP = "d"
    CHANNEL_TYPE = "t"


class CommunityChannelTypes(enum.Enum):
    SIGNAL = "t"  # to check
    ALERT = "alert"


class SignalBundlesAttrs(enum.Enum):
    IDENTIFIER = "identifier"
    SIGNALS = "signals"
    VERSION = "version"


class SignalsAttrs(enum.Enum):
    TOPIC = "topic"
    CONTENT = "content"


class InitializationEventExchangeTopics(enum.Enum):
    POSITIONS = "positions"
    BALANCE = "balance"
    ORDERS = "orders"
    TRADES = "trades"
    CONTRACTS = "contracts"
    CANDLES = "candles"
    PRICE = "price"
    ORDER_BOOK = "order_book"
    FUNDING = "funding"


class UserInputTentacleTypes(enum.Enum):
    TRADING_MODE = "trading_mode"
    EVALUATOR = "evaluator"
    EXCHANGE = "exchange"
    UNDEFINED = "undefined"


class UserInputTypes(enum.Enum):
    INT = "int"
    FLOAT = "float"
    BOOLEAN = "boolean"
    OPTIONS = "options"
    MULTIPLE_OPTIONS = "multiple-options"
    TEXT = "text"
    OBJECT = "object"
    OBJECT_ARRAY = "object_array"
    STRING_ARRAY = "string_array"
