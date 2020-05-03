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

cdef list _sort_time_frames(list time_frames, bint reverse=*)

cpdef list get_config_time_frame(dict config)
cpdef list sort_time_frames(list time_frames, bint reverse=*)
cpdef void sort_config_time_frames(dict config)
cpdef object get_display_time_frame(dict config, object default_display_time_frame)
cpdef object get_previous_time_frame(list config_time_frames, object time_frame, object origin_time_frame)
cpdef object find_min_time_frame(list time_frames, object min_time_frame=*)
cpdef list parse_time_frames(list time_frames_string_list)
