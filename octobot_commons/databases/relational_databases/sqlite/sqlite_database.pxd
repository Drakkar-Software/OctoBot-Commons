# cython: language_level=3
#  Drakkar-Software OctoBot-Backtesting
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
#  Lesser General License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.

cdef class SQLiteDatabase:
    cdef str file_name

    cdef object logger
    cdef object connection
    cdef object _cursor_pool

    cdef list tables

    cdef dict cache

    cdef str __insert_values(self, double timestamp, str inserting_values)
    cdef str __select_order_by(self, str order_by, str sort)
    cdef str __select_group_by(self, str group_by)
    cdef str __max(self, list columns)
    cdef str __min(self, list columns)
    cdef str __quote_value(self, str value)
    cdef str __selected_columns(self, list columns=*)
    cdef str __where_clauses_from_operations(self, list keys, list values, list operations, bint should_quote_value=*)
    cdef str __where_clauses_from_operation(self, str key, str value, str operation=*, bint should_quote_value=*)
