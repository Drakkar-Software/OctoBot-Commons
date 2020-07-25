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

cpdef bint default_parent_inspection(object element, object parent)
cpdef bint default_parents_inspection(object element, object parent)
cpdef bint evaluator_parent_inspection(object element, object parent)
cpdef bint trading_mode_parent_inspection(object element, object parent)

cpdef object get_class_from_parent_subclasses(str class_string, object parent)
cpdef object get_deep_class_from_parent_subclasses(str class_string, object parent)

cpdef bint is_abstract_using_inspection_and_class_naming(object clazz)

cpdef list get_all_classes_from_parent(object parent_class)
cpdef object get_single_deepest_child_class(object clazz)
