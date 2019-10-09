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

cdef void __init_class_list_config(dict config)
cdef dict __get_advanced_classes(dict config)
cdef dict __get_advanced_instances(dict config)
cdef void __append_to_class(dict config, str class_name, object class_type)
cdef bint __check_duplicate(list list_to_check)
cdef void __get_advanced(dict config, object class_type, object abstract_class=*)

cpdef bint is_abstract(object class_type)
cpdef void create_classes_list(dict config, object abstract_class)
cpdef list get_classes(dict config, object class_type, bint should_get_all_classes=*)
cpdef object get_class(dict config, object class_type)
cpdef list create_default_types_list(object clazz)
cpdef list create_advanced_types_list(object clazz, dict config)
cpdef list get_all_classes(object clazz, dict config)
cpdef object search_class_name_in_class_list(str class_name, list parent_class_list)
cpdef list get_all_classes_from_parent(object parent_class)

