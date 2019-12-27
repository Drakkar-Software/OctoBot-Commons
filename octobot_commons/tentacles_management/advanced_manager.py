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

from copy import copy

from octobot_commons.constants import CONFIG_ADVANCED_INSTANCES, CONFIG_ADVANCED_CLASSES
from octobot_commons.logging.logging_util import get_logger


def is_abstract(class_type) -> bool:
    """
    is_abstract will test if the class in an abstract one or not
    by checking if __metaclass__ attribute is inherited or not we will know if the class is an abstract one
    :param class_type: class_type to inspect
    :return: True if it is an abstract one else False
    """

    # Get class parental description
    mro = class_type.mro()

    # if class has parent get its metaclass
    try:
        parent_metaclass = mro[1].__metaclass__
    except KeyError:
        parent_metaclass = None

    # If the metaclass attribute has been inherited
    try:
        if class_type.__metaclass__ == parent_metaclass:
            return False
        return True
    except AttributeError:
        return False


def __get_advanced(config, class_type, abstract_class=None) -> None:
    """
    get_advanced will get each subclasses of the parameter class_type
    For each abstract subclasses it will call itself with the reference abstract_class not set
    If the current child is not abstract it will be set as the reference only if abstract_class is None
    If there is not subclasses to class_type it will add class_type into the config advanced list
    with its name as a key or the reference class name --> abstract_class
    :param config: global config dict
    :param class_type: class type to append
    :param abstract_class: abstract class to get advanced
    :return: None
    """

    if class_type.__subclasses__():
        for child in class_type.__subclasses__():
            if is_abstract(child):
                __get_advanced(config, child)
            else:
                # If abstract class is not defined --> current non abstract_class is the reference
                # else keep the first non abstract class as the reference
                if abstract_class is None:
                    __get_advanced(config, child, child.get_name())
                else:
                    __get_advanced(config, child, abstract_class)
    else:
        if abstract_class is not None:
            __append_to_class(config, abstract_class, class_type)
        else:
            __append_to_class(config, class_type.get_name(), class_type)


def create_classes_list(config, abstract_class) -> None:
    """
    create_class_list will create a list with the best class available
    Advanced class are declared into advanced folders of each packages
    This will call the get_advanced method to initialize the config list
    :param config: global config dict
    :param abstract_class: abstract class to get advanced child
    :return: None
    """
    __init_class_list_config(config)
    __get_advanced(config, abstract_class)


def __init_class_list_config(config) -> None:
    """
    Init advanced dicts in config if not exists
    :param config: global config dict
    :return: None
    """

    if CONFIG_ADVANCED_CLASSES not in config:
        config[CONFIG_ADVANCED_CLASSES] = {}

    if CONFIG_ADVANCED_INSTANCES not in config:
        config[CONFIG_ADVANCED_INSTANCES] = {}


def __get_advanced_classes(config) -> dict:
    return config[CONFIG_ADVANCED_CLASSES]


def __get_advanced_instances(config) -> dict:
    return config[CONFIG_ADVANCED_INSTANCES]


def __append_to_class(config, class_name, class_type) -> None:
    """
    Append class type to advanced class list
    :param config: global config dict
    :param class_name: class name to add
    :param class_type: class type to add
    :return: None
    """
    try:
        __get_advanced_classes(config)[class_name].append(class_type)
    except KeyError:
        __get_advanced_classes(config)[class_name] = [class_type]


def get_classes(config, class_type, should_get_all_classes=False) -> list:
    classes = []
    if class_type.get_name() in __get_advanced_classes(config):
        classes = copy(__get_advanced_classes(config)[class_type.get_name()])
    if not classes or (should_get_all_classes and class_type not in classes):
        classes.append(class_type)
    return classes


def get_class(config, class_type) -> object:
    classes = get_classes(config, class_type)
    if classes and len(classes) > 1:
        get_logger(__name__).warning(f"More than one instance of {class_type} available, "
                                     f"using {classes[0]}.")
    return classes[0]


def get_instance(config, class_type, *args) -> object:
    advanced_class_type = get_class(config, class_type)
    if class_type in __get_advanced_instances(config):
        return __get_advanced_instances(config)[class_type]
    elif advanced_class_type:
        instance = advanced_class_type(*args)
        __get_advanced_instances(config)[class_type] = instance
        return instance
    return None


def create_default_types_list(clazz) -> list:
    default_class_list = []
    for current_subclass in clazz.__subclasses__():
        subclasses = current_subclass.__subclasses__()
        if subclasses:
            for current_class in subclasses:
                default_class_list.append(current_class)
        else:
            if not is_abstract(current_subclass):
                default_class_list.append(current_subclass)
    return default_class_list


def create_advanced_types_list(clazz, config) -> list:
    advanced_class_list = [
        class_type
        for subclass in clazz.__subclasses__()
        for class_type in get_classes(config, subclass)
    ]

    if not __check_duplicate(advanced_class_list):
        get_logger(__name__).warning("Duplicate class name.")

    return advanced_class_list


def get_all_classes(clazz, config) -> list:
    return [
        class_type
        for subclass in clazz.__subclasses__()
        for type_class in subclass.__subclasses__()
        for class_type in get_classes(config, type_class, True)
    ]


def get_all_classes_from_parent(parent_class) -> list:
    classes = []
    for subclass in parent_class.__subclasses__():
        if subclass.__subclasses__():
            classes += get_all_classes_from_parent(subclass)
        else:
            classes.append(subclass)
    return classes


def search_class_name_in_class_list(class_name, parent_class_list) -> object:
    for subclass in parent_class_list:
        if isinstance(subclass, list):
            return search_class_name_in_class_list(class_name, subclass)
        elif subclass.get_name() == class_name:
            return subclass
    return None


def __check_duplicate(list_to_check) -> bool:
    return len(set(list_to_check)) == len(list_to_check)


def get_single_deepest_child_class(clazz) -> object:
    children_classes = clazz.__subclasses__()
    if len(children_classes) == 0:
        return clazz
    if len(children_classes) > 1:
        get_logger(__name__).error(f"More than one child class of {clazz}, expecting one, "
                                   f"using {children_classes[0]}")
    return get_single_deepest_child_class(children_classes[0])
