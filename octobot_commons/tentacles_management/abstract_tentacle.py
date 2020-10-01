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
import abc
import copy


class AbstractTentacle:
    """
    The parent class of any OctoBot tentacle
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.logger = None

    @classmethod
    def get_name(cls) -> str:
        """
        Tentacle name based on class name
        :return: the tentacle name
        """
        return cls.__name__

    @classmethod
    def get_all_subclasses(cls) -> list:
        """
        Return all subclasses of this tentacle
        :return: the subclasses
        """
        subclasses_list = cls.__subclasses__()
        if cls.__subclasses__():
            for subclass in copy.deepcopy(subclasses_list):
                subclasses_list += subclass.get_all_subclasses()
        return subclasses_list
