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


def split_symbol(symbol):
    """
    Split the specified symbol
    :param symbol: the symbol to split
    :return: currency, market
    """
    try:
        separated_symbol = symbol.split(octobot_commons.MARKET_SEPARATOR)
        return separated_symbol[0], separated_symbol[1]
    except IndexError:
        return symbol


def merge_symbol(symbol):
    """
    Return merged currency and market without /
    :param symbol: the specified symbol
    :return: merged currency and market without /
    """
    return symbol.replace(octobot_commons.MARKET_SEPARATOR, "")


def merge_currencies(currency, market, separator=octobot_commons.MARKET_SEPARATOR):
    """
    Merge currency and market
    :param currency: the currency
    :param market: the currency
    :param separator: the separator
    :return: currency and market merged
    """
    return f"{currency}{separator}{market}"


def convert_symbol(
    symbol,
    symbol_separator,
    new_symbol_separator=octobot_commons.MARKET_SEPARATOR,
    should_uppercase=False,
    should_lowercase=False,
):
    """
    Convert symbol according to parameter
    :param symbol: the symbol to convert
    :param symbol_separator: the symbol separator
    :param new_symbol_separator: the new symbol separator
    :param should_uppercase: if it should be concerted to uppercase
    :param should_lowercase: if it should be concerted to lowercase
    :return:
    """
    if should_uppercase:
        return symbol.replace(symbol_separator, new_symbol_separator).upper()
    if should_lowercase:
        return symbol.replace(symbol_separator, new_symbol_separator).lower()
    return symbol.replace(symbol_separator, new_symbol_separator)
