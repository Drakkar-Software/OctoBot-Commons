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


cdef class EventTreeNode:
    cdef public object node_value
    cdef public object node_event
    cdef public object node_type
    cdef public object node_task
    cdef public list node_path
    cdef public dict children

cdef class EventTree:
    cdef public EventTreeNode root

    cpdef void set_node(self, object value, object node_type, EventTreeNode node)
    cpdef void set_node_at_path(self, object value, object node_type, list path)
    cpdef EventTreeNode get_node(self, list path)

    cdef EventTreeNode __get_node(self, list path)
    cdef EventTreeNode __create_node_path(self, list path)
    cdef void __set_node(self, EventTreeNode node, object value=*, object node_type=*)
