# cython: language_level=3
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

cpdef str open_order_pretty_printer(str exchange_name, dict dict_order, bint markdown=*)
cpdef str trade_pretty_printer(str exchange_name, object trade, bint markdown=*)
cpdef tuple cryptocurrency_alert(object result, object final_eval)
cpdef str global_portfolio_pretty_print(object global_portfolio, str separator=*, bint markdown=*)
cpdef str portfolio_profitability_pretty_print(double profitability, object profitability_percent, str reference)
# cpdef str pretty_print_dict(dict dict_content, default=*, bint markdown=*)
cpdef double round_with_decimal_count(object number, int max_digits=*)
cpdef str get_min_string_from_number(object number, int max_digits=*)
cpdef tuple get_markers(bint markdown=*)
