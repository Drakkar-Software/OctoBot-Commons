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


cdef class Symbol:
    cdef public str symbol_str
    cdef public str base
    cdef public str quote
    cdef public str settlement_asset
    cdef public str identifier
    cdef public str strike_price
    cdef public str option_type
    cdef public str full_symbol_regex

    cpdef object parse_symbol(self, str symbol_str)
    cpdef tuple base_and_quote(self)
    cpdef bint is_linear(self)
    cpdef bint is_inverse(self)
