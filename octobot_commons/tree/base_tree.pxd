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


cdef class BaseTreeNode:
    cdef public object node_value
    cdef public object node_value_time
    cdef public object node_type
    cdef public dict children

    cpdef void set_child(self, object key, object child)
    cpdef object pop_child(self, object key, object default)

cdef class NodeExistsError(Exception):
    pass

cdef class BaseTree:
    cdef public BaseTreeNode root

    cpdef void set_node(self, object value, object node_type, BaseTreeNode node, double timestamp=*)
    cpdef void set_node_at_path(self, object value, object node_type, list path, double timestamp=*)
    cpdef BaseTreeNode get_node(self, list path, BaseTreeNode starting_node=*)
    cpdef BaseTreeNode delete_node(self, list path, BaseTreeNode starting_node=*)
    cpdef list get_children_keys(self, list path)

    cdef BaseTreeNode _get_node(self, list path, BaseTreeNode starting_node=*)
    cdef BaseTreeNode _delete_node(self, list path, BaseTreeNode starting_node=*)
    cdef void _set_node(self, BaseTreeNode node, object value=*, object node_type=*, double timestamp=*)
