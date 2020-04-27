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

import inspect


def default_parent_inspection(element, parent):
    """
    Check if the element bases has the specified parent
    :param element: the element to check
    :param parent: the expected parent
    :return: the check result
    """
    return parent in element.__bases__


def default_parents_inspection(element, parent):
    """
    Check if the element has the specified parent
    :param element: the element to check
    :param parent: the expected parent
    :return: the check result
    """
    return parent in element.mro()


def evaluator_parent_inspection(element, parent):
    """
    Recursively check if the evaluator class has the specified parent
    :param element: the element to check
    :param parent: the expected parent
    :return: the check result
    """
    return hasattr(
        element, "get_parent_evaluator_classes"
    ) and element.get_parent_evaluator_classes(parent)


def trading_mode_parent_inspection(element, parent):
    """
    Check if the trading class has the specified parent
    :param element: the element to check
    :param parent: the expected parent
    :return: the check result
    """
    return hasattr(
        element, "get_parent_trading_mode_classes"
    ) and element.get_parent_trading_mode_classes(parent)


def get_class_from_parent_subclasses(class_string, parent):
    """
    Search the class string in parent subclasses
    :param class_string: the class name to search
    :param parent: the parent
    :return: the class if found else None
    """
    for found in parent.__subclasses__():
        if found.__name__ == class_string:
            return found
    return None


def get_deep_class_from_parent_subclasses(class_string, parent):
    """
    Search for a class in parent subclasses "deeply"
    :param class_string: the class name to search
    :param parent: the expected parent
    :return: the class if found else None
    """
    found = get_class_from_parent_subclasses(class_string, parent)
    if found is not None:
        return found

    for parent_class in parent.__subclasses__():
        found = get_deep_class_from_parent_subclasses(class_string, parent_class)
        if found is not None:
            return found
    return None


def get_class_from_string(
    class_string: str,
    parent,
    module,
    parent_inspection=default_parent_inspection,
    error_when_not_found: bool = False,
):
    """
    Search a class from a class string in a specified module for a specified parent
    :param class_string: the class name to search
    :param parent: the class expected parent
    :param module: the class expected module
    :param parent_inspection: the parent inspection
    :param error_when_not_found: if errors should be raised
    :return: the class if found else None
    """
    if any(
        m[0] == class_string
        and hasattr(m[1], "__bases__")
        and parent_inspection(m[1], parent)
        for m in inspect.getmembers(module)
    ):
        return getattr(module, class_string)
    if error_when_not_found:
        raise ModuleNotFoundError(f"Cant find {class_string} module")
    return None


def get_deep_class_from_string(class_string, module):
    """
    Search for a class string in module
    :param class_string: the class name to search
    :param module: the module
    :return: the class if found else None
    """
    for member in inspect.getmembers(module):
        if member[0] == class_string:
            return getattr(module, class_string)
    return None


def is_abstract_using_inspection_and_class_naming(clazz):
    """
    Check if a class is abstract
    :param clazz: the class to check
    :return: the check result
    """
    return inspect.isabstract(clazz) or "abstract" in clazz.__name__.lower()
