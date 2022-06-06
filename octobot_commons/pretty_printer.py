# pylint: disable=C0415
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

import octobot_commons
import octobot_commons.enums as enums
import octobot_commons.constants as constants
import octobot_commons.logging as logging_util
import octobot_commons.symbols.symbol_util as symbol_util
import octobot_commons.timestamp_util as timestamp_util
import octobot_commons.number_util as number_util

ORDER_TIME_FORMAT = "%m-%d %H:%M"
LOGGER = logging_util.get_logger("PrettyPrinter")


def open_order_pretty_printer(exchange_name, dict_order, markdown=False) -> str:
    """
    Open Order pretty printer
    :param exchange_name: the exchange name
    :param dict_order: the order dict
    :param markdown: if printer use markdown
    :return: the order pretty printed
    """
    try:
        from octobot_trading.enums import (
            ExchangeConstantsOrderColumns,
            TraderOrderType,
            TradeOrderSide,
        )
        from octobot_trading.api.orders import parse_order_type

        _, _, code = get_markers(markdown)
        market = symbol_util.parse_symbol(
            str(dict_order.get(ExchangeConstantsOrderColumns.SYMBOL.value, ""))
        ).quote
        quantity_currency = dict_order.get(
            ExchangeConstantsOrderColumns.QUANTITY_CURRENCY.value, ""
        )
        order_type = parse_order_type(dict_order)
        if order_type == TraderOrderType.UNKNOWN:
            order_type = TradeOrderSide(
                dict_order.get(ExchangeConstantsOrderColumns.SIDE.value)
            )
        quantity = dict_order.get(ExchangeConstantsOrderColumns.AMOUNT.value, 0.0)
        price = dict_order.get(ExchangeConstantsOrderColumns.PRICE.value, 0.0)

        return (
            f"{code}{order_type.name.replace('_', ' ')}{code}: {code}"
            f"{get_min_string_from_number(quantity)} {quantity_currency}{code} at {code}"
            f"{get_min_string_from_number(price)} {market}{code} on {exchange_name.capitalize()}"
        )
    except ImportError:
        LOGGER.error(
            "open_order_pretty_printer requires OctoBot-Trading package installed"
        )
    return ""


def trade_pretty_printer(exchange_name, trade, markdown=False) -> str:
    """
    Trade pretty printer
    :param exchange_name: the exchange name
    :param trade: the trade object
    :param markdown: if printer use markdown
    :return: the trade pretty printed
    """
    try:
        from octobot_trading.enums import TraderOrderType

        _, _, code = get_markers(markdown)
        trade_type = trade.trade_type
        if trade_type == TraderOrderType.UNKNOWN:
            trade_type = trade.side

        trade_executed_time_str = (
            timestamp_util.convert_timestamp_to_datetime(
                trade.executed_time, time_format=ORDER_TIME_FORMAT
            )
            if trade.executed_time
            else ""
        )
        return (
            f"{code}{trade_type.name.replace('_', ' ')}{code}: {code}"
            f"{get_min_string_from_number(trade.executed_quantity)} {trade.quantity_currency}{code} at {code}"
            f"{get_min_string_from_number(trade.executed_price)} {trade.market}{code} "
            f"{exchange_name.capitalize()} "
            f"{trade_executed_time_str} "
        )
    except ImportError:
        LOGGER.error(
            "open_order_pretty_printer requires OctoBot-Trading package installed"
        )
    return ""


def cryptocurrency_alert(result, final_eval) -> (str, str):
    """
    Cryptocurrency alert
    :param result: the result
    :param final_eval: the final eval
    :return: alert and the markdown alert
    """
    try:
        from telegram.utils.helpers import escape_markdown

        _, _, code = get_markers(True)
        display_result = str(result).split(".")[1].replace("_", " ")
        alert = f"Result : {display_result}\n" f"Evaluation : {final_eval}"
        alert_markdown = (
            f"Result : {code}{display_result}{code}\n"
            f"Evaluation : {code}{escape_markdown(str(final_eval))}{code}"
        )
        return alert, alert_markdown
    except ImportError:
        LOGGER.error("cryptocurrency_alert requires Telegram package installed")
    return "", ""


def global_portfolio_pretty_print(
    global_portfolio, separator="\n", markdown=False
) -> str:
    """
    Global portfolio pretty printer
    :param global_portfolio: the global portfolio
    :param separator: the printer separator
    :param markdown: if printer use markdown
    :return: the global portfolio pretty printed
    """
    result = []
    for currency, asset_dict in global_portfolio.items():
        if asset_dict[constants.PORTFOLIO_TOTAL] > 0:
            # fill lines with empty spaces if necessary
            total = get_min_string_from_number(asset_dict[constants.PORTFOLIO_TOTAL])
            if markdown:
                total = "{:<10}".format(total)
            available = f"({get_min_string_from_number(asset_dict[constants.PORTFOLIO_AVAILABLE])})"
            if markdown:
                available = "{:<12}".format(available)

            holding_str = f"{total} {available} {currency}"
            result.append(holding_str)

    return separator.join(result)


def portfolio_profitability_pretty_print(
    profitability, profitability_percent, reference
) -> str:
    """
    Profitability pretty printer
    :param profitability: the profitability
    :param profitability_percent: the profitability percent
    :param reference: the reference
    :return: the profitability pretty printed
    """
    difference = (
        f"({get_min_string_from_number(profitability_percent, 5)}%)"
        if profitability_percent is not None
        else ""
    )
    return f"{get_min_string_from_number(profitability, 5)} {reference} {difference}"


def pretty_print_dict(dict_content, default="0", markdown=False) -> str:
    """
    Dict pretty printer
    :param dict_content: the dict to be printed
    :param default: the default printed
    :param markdown: if printer use markdown
    :return: the dict pretty printed
    """
    _, _, code = get_markers(markdown)
    if dict_content:
        result_str = octobot_commons.DICT_BULLET_TOKEN_STR
        return (
            f"{result_str}{code}"
            f"{octobot_commons.DICT_BULLET_TOKEN_STR.join(f'{value} {key}' for key, value in dict_content.items())}"
            f"{code}"
        )
    return default


def round_with_decimal_count(number, max_digits=8) -> float:
    """
    Round a decimal count
    :param number: the number to round
    :param max_digits: the digits
    :return: the rounded number
    """
    if number is None:
        return 0
    return float(get_min_string_from_number(number, max_digits))


def get_min_string_from_number(number, max_digits=8) -> str:
    """
    Get a min string from number
    :param number: the number
    :param max_digits: the mex digits
    :return: the string from number
    """
    if number is None or round(number, max_digits) == 0.0:
        return "0"
    if number % 1 != 0:
        number_str = number_util.round_into_str_with_max_digits(number, max_digits)
        # remove post comma trailing 0
        if "." in number_str:
            # remove "0" first and only the "." to avoid removing 2x"0" in 10.0 and returning 1 for example.
            number_str = number_str.rstrip("0").rstrip(".")
        return number_str
    return "{:f}".format(number).split(".")[0]


# return markers for italic, bold and code
def get_markers(markdown=False) -> (str, str, str):
    """
    Get the markdown markers
    :param markdown: if printer use markdown
    :return: the italic marker, the bold marker, the code marker
    """
    if markdown:
        return (
            enums.MarkdownFormat.ITALIC.value,
            enums.MarkdownFormat.BOLD.value,
            enums.MarkdownFormat.CODE.value,
        )
    return "", "", ""
