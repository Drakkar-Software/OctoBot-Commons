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
cimport octobot_commons.tree.base_tree as base_tree


cdef class EventTreeNode(base_tree.BaseTreeNode):
    cdef base_tree.BaseTreeNode _parent
    cdef object _logger

    cpdef void bind_parent(self, object parent)
    cpdef bint is_triggered(self)
    cpdef void trigger(self)
    cpdef void clear(self)
    cpdef void on_child_change(self)
    cpdef object get_parent(self)
    cpdef list get_path_to_root(self)
    cpdef object get_child_key(self, object child_to_find)

    cdef void _propagate(self)
    cdef void _trigger(self)
    cdef void _trigger_and_log(self)
    cdef void _clear(self)
    cdef list _untriggered_children(self)


cdef class EventTree(base_tree.BaseTree):
    cpdef create_node_at_path(self, list path, bint triggered)
