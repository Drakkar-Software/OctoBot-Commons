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
from abc import ABCMeta
from copy import deepcopy

from octobot_commons.config import load_config

from octobot_commons.constants import SCHEMA, CONFIG_FILE_EXT, TENTACLE_CONFIG_FOLDER, TENTACLES_PATH


class AbstractTentacle:
    __metaclass__ = ABCMeta

    DESCRIPTION = "No description set."

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
    def get_config_tentacle_type(cls) -> str:
        """
        :return: The tentacle config type
        """
        raise NotImplementedError("get_config_tentacle_type")

    @classmethod
    def get_tentacle_folder(cls) -> str:
        """
        :return: The tentacle folder
        """
        raise NotImplementedError("get_tentacle_folder")

    @classmethod
    def get_all_subclasses(cls) -> list:
        subclasses_list = cls.__subclasses__()
        if cls.__subclasses__():
            for subclass in deepcopy(subclasses_list):
                subclasses_list += subclass.get_all_subclasses()
        return subclasses_list

    @classmethod
    def get_config_folder(cls, config_tentacle_type=None) -> str:
        return f"{TENTACLES_PATH}" \
               f"/{cls.get_tentacle_folder()}" \
               f"/{config_tentacle_type or cls.get_config_tentacle_type()}" \
               f"/{TENTACLE_CONFIG_FOLDER}"

    @classmethod
    def get_config_file_name(cls, config_tentacle_type=None) -> str:
        return f"{cls.get_config_folder(config_tentacle_type)}/{cls.get_name()}{CONFIG_FILE_EXT}"

    @classmethod
    def get_config_file_schema_name(cls, config_tentacle_type=None) -> str:
        return f"{cls.get_config_folder(config_tentacle_type)}/{cls.get_name()}_{SCHEMA}{CONFIG_FILE_EXT}"

    @classmethod
    def get_config_file_error_message(cls, error) -> str:
        return f"Key Error when computing {cls.get_name()} this probably means an error in " \
               f"{cls.get_config_file_name()} config file" \
               f". (error: {error})"

    @classmethod
    def get_specific_config(cls, raise_exception=True, raw_file=False) -> str:
        try:
            if raw_file:
                with open(cls.get_config_file_name()) as file:
                    return file.read()
            return load_config(cls.get_config_file_name())
        except Exception as e:
            if raise_exception:
                raise e
        return ""

    @classmethod
    def get_specific_config_schema(cls, raise_exception=True) -> str:
        try:
            with open(cls.get_config_file_schema_name()) as f:
                return f.read()
        except Exception as e:
            if raise_exception:
                raise e
        return ""

    @classmethod
    # returns DESCRIPTION class attribute, used as documentation
    def get_description(cls) -> str:
        return cls.DESCRIPTION
