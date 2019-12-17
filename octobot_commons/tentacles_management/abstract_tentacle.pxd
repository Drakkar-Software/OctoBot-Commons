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


cdef class AbstractTentacle:
    cdef public object logger

    cpdef str get_name(cls)

    cpdef str get_config_tentacle_type(cls)

    cpdef str get_tentacle_folder(cls)

    cpdef list get_all_subclasses(cls)

#     cpdef str get_config_folder(cls, str config_tentacle_type=*)
#
#     cpdef str get_config_file_name(cls, str config_tentacle_type=*)
#
#     cpdef str get_config_file_schema_name(cls, str config_tentacle_type=*)
#
#     cpdef str get_config_file_error_message(cls, str error)
#
#     cpdef dict get_specific_config(cls, bint raise_exception=*)
#
#     cpdef str get_specific_raw_config(cls, bint raise_exception=*)
#
#     cpdef str get_specific_config_schema(cls, bint raise_exception=*)

    cpdef str get_description(cls)
