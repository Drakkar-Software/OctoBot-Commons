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
from octobot_commons.enums import MarkdownFormat
from octobot_commons.timestamp_util import convert_timestamp_to_datetime
from octobot_commons.number_util import round_into_str_with_max_digits
from telegram.utils.helpers import escape_markdown


class PrettyPrinter:

    ORDER_TIME_FORMAT = '%m-%d %H:%M'

    @staticmethod
    def open_order_pretty_printer(exchange_name, order, markdown=False):
        _, _, c = PrettyPrinter.get_markers(markdown)
        currency, market = order.get_currency_and_market()
        order_type_name = order.order_type.name

        return f"{c}{order_type_name}{c}: {c}{PrettyPrinter.get_min_string_from_number(order.origin_quantity)} " \
            f"{currency}{c} at {c}{PrettyPrinter.get_min_string_from_number(order.origin_price)} {market}{c} " \
            f"{exchange_name} " \
            f"{convert_timestamp_to_datetime(order.creation_time, time_format=PrettyPrinter.ORDER_TIME_FORMAT)}"

    @staticmethod
    def trade_pretty_printer(exchange_name, trade, markdown=False):
        _, _, c = PrettyPrinter.get_markers(markdown)
        currency = trade.currency
        market = trade.market
        order_type_name = trade.order_type.name
        
        return f"{c}{order_type_name}{c}: {c}{PrettyPrinter.get_min_string_from_number(trade.quantity)} {currency}{c}" \
            f" at {c}{PrettyPrinter.get_min_string_from_number(trade.price)} {market}{c} " \
            f"{exchange_name} " \
            f"{convert_timestamp_to_datetime(trade.filled_time, time_format=PrettyPrinter.ORDER_TIME_FORMAT)}"

    @staticmethod
    def cryptocurrency_alert(result, final_eval):
        _, _, c = PrettyPrinter.get_markers(True)
        alert = f"Result : {str(result).split('.')[1]}\n" \
                f"Evaluation : {final_eval}"
        alert_markdown = f"Result : {c}{str(result).split('.')[1]}{c}\n" \
                         f"Evaluation : {c}{escape_markdown(str(final_eval))}{c}"
        return alert, alert_markdown

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
