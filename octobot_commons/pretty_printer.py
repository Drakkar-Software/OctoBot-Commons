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

from octobot_commons import DICT_BULLET_TOKEN_STR
from octobot_commons.constants import PORTFOLIO_TOTAL, PORTFOLIO_AVAILABLE
from octobot_commons.dict_util import get_value_or_default
from octobot_commons.enums import MarkdownFormat
from octobot_commons.logging.logging_util import get_logger
from octobot_commons.symbol_util import split_symbol
from octobot_commons.timestamp_util import convert_timestamp_to_datetime
from octobot_commons.number_util import round_into_str_with_max_digits


class PrettyPrinter:

    ORDER_TIME_FORMAT = '%m-%d %H:%M'
    LOGGER = get_logger("PrettyPrinter")

    @staticmethod
    def open_order_pretty_printer(exchange_name, dict_order, markdown=False):
        try:
            from octobot_trading.enums import ExchangeConstantsOrderColumns, TraderOrderType, TradeOrderSide
            from octobot_trading.api.orders import parse_order_type
            _, _, c = PrettyPrinter.get_markers(markdown)
            currency, market = \
                split_symbol(str(get_value_or_default(dict_order, ExchangeConstantsOrderColumns.SYMBOL.value, "")))
            order_type = parse_order_type(dict_order)
            if order_type == TraderOrderType.UNKNOWN:
                order_type = TradeOrderSide(get_value_or_default(dict_order, ExchangeConstantsOrderColumns.SIDE.value))
            quantity = get_value_or_default(dict_order, ExchangeConstantsOrderColumns.AMOUNT.value, 0.0)
            price = get_value_or_default(dict_order, ExchangeConstantsOrderColumns.PRICE.value, 0.0)
            creation_time = get_value_or_default(dict_order, ExchangeConstantsOrderColumns.TIMESTAMP.value, 0)

            return f"{c}{order_type.name.replace('_', ' ')}{c}: {c}" \
                   f"{PrettyPrinter.get_min_string_from_number(quantity)} {currency}{c} at {c}" \
                   f"{PrettyPrinter.get_min_string_from_number(price)} {market}{c} {exchange_name.capitalize()} " \
                   f"{convert_timestamp_to_datetime(creation_time, time_format=PrettyPrinter.ORDER_TIME_FORMAT)}"
        except ImportError:
            PrettyPrinter.LOGGER.error("open_order_pretty_printer requires OctoBot-Trading package installed")

    @staticmethod
    def trade_pretty_printer(exchange_name, trade, markdown=False):
        try:
            from octobot_trading.enums import ExchangeConstantsOrderColumns, TraderOrderType
            _, _, c = PrettyPrinter.get_markers(markdown)
            trade_type = trade.trade_type
            if trade_type == TraderOrderType.UNKNOWN:
                trade_type = trade.side

            return f"{c}{trade_type.name.replace('_', ' ')}{c}: {c}" \
                   f"{PrettyPrinter.get_min_string_from_number(trade.executed_quantity)} {trade.currency}{c} at {c}" \
                   f"{PrettyPrinter.get_min_string_from_number(trade.executed_price)} {trade.market}{c} " \
                   f"{exchange_name.capitalize()} " \
                   f"{convert_timestamp_to_datetime(trade.executed_time, time_format=PrettyPrinter.ORDER_TIME_FORMAT)}"
        except ImportError:
            PrettyPrinter.LOGGER.error("open_order_pretty_printer requires OctoBot-Trading package installed")

    @staticmethod
    def cryptocurrency_alert(result, final_eval):
        try:
            from telegram.utils.helpers import escape_markdown
            _, _, c = PrettyPrinter.get_markers(True)
            display_result = str(result).split('.')[1].replace('_', ' ')
            alert = f"Result : {display_result}\n" \
                    f"Evaluation : {final_eval}"
            alert_markdown = f"Result : {c}{display_result}{c}\n" \
                             f"Evaluation : {c}{escape_markdown(str(final_eval))}{c}"
            return alert, alert_markdown
        except ImportError:
            PrettyPrinter.LOGGER.error("cryptocurrency_alert requires Telegram package installed")

    @staticmethod
    def global_portfolio_pretty_print(global_portfolio, separator="\n", markdown=False):
        result = []
        for currency, amounts in global_portfolio.items():
            if amounts[PORTFOLIO_TOTAL] > 0:
                # fill lines with empty spaces if necessary
                total = PrettyPrinter.get_min_string_from_number(amounts[PORTFOLIO_TOTAL])
                if markdown:
                    total = "{:<10}".format(total)
                available = f"({PrettyPrinter.get_min_string_from_number(amounts[PORTFOLIO_AVAILABLE])})"
                if markdown:
                    available = "{:<12}".format(available)

                holding_str = f"{total} {available} {currency}"
                result.append(holding_str)

        return separator.join(result)

    @staticmethod
    def portfolio_profitability_pretty_print(profitability, profitability_percent, reference):
        difference = f"({PrettyPrinter.get_min_string_from_number(profitability_percent, 5)}%)" \
            if profitability_percent is not None else ""
        return f"{PrettyPrinter.get_min_string_from_number(profitability, 5)} {reference} {difference}"

    @staticmethod
    def pretty_print_dict(dict_content, default="0", markdown=False):
        _, _, c = PrettyPrinter.get_markers(markdown)
        if dict_content:
            result_str = DICT_BULLET_TOKEN_STR
            return f"{result_str}{c}" \
                f"{DICT_BULLET_TOKEN_STR.join(f'{value} {key}' for key, value in dict_content.items())}{c}"
        return default

    @staticmethod
    def round_with_decimal_count(number, max_digits=8):
        if number is None:
            return 0
        return float(PrettyPrinter.get_min_string_from_number(number, max_digits))

    @staticmethod
    def get_min_string_from_number(number, max_digits=8):
        if number is None or round(number, max_digits) == 0.0:
            return "0"
        else:
            if number % 1 != 0:
                number_str = round_into_str_with_max_digits(number, max_digits)
                if "." in number_str:
                    number_str = number_str.rstrip("0.")
                return number_str
            return "{:f}".format(number).split(".")[0]

    # return markers for italic, bold and code
    @staticmethod
    def get_markers(markdown=False):
        if markdown:
            return MarkdownFormat.ITALIC.value, MarkdownFormat.BOLD.value, MarkdownFormat.CODE.value
        return "", "", ""
