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

cdef class BotLogger:
    cdef str logger_name
    cdef object logger

    cpdef void disable(self, bint disabled)

    cdef void _publish_log_if_necessary(self, str message, object level)
    cdef void _web_interface_publish_log(self, str message, object level)

cpdef void set_global_logger_level(level)
cpdef object get_global_logger_level()
cpdef object get_logger(str logger_name=*)
cpdef void set_logging_level(list logger_names, object level)
cpdef int get_backtesting_errors_count()
cpdef void reset_backtesting_errors()
cpdef void set_error_publication_enabled(bint enabled)
