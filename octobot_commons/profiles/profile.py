# pylint: disable=R0902
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
import json
import copy
import os
import shutil
import uuid
import octobot_commons.constants as constants
import octobot_commons.json_util as json_util


class Profile:
    """
    A profile is managing an OctoBot local configuration: activated tentacles, exchanges, currencies and
    trading settings.
    """

    FULLY_MANAGED_ELEMENTS = [
        constants.CONFIG_CRYPTO_CURRENCIES,
        constants.CONFIG_TRADING,
        constants.CONFIG_TRADER,
        constants.CONFIG_SIMULATOR,
    ]
    PARTIALLY_MANAGED_ELEMENTS = {
        constants.CONFIG_EXCHANGES: {
            constants.CONFIG_EXCHANGE_KEY: constants.DEFAULT_API_KEY,
            constants.CONFIG_EXCHANGE_SECRET: constants.DEFAULT_API_SECRET,
            constants.CONFIG_EXCHANGE_PASSWORD: constants.DEFAULT_API_PASSWORD,
            constants.CONFIG_ENABLED_OPTION: False,
        }
    }
    PARTIALLY_MANAGED_ELEMENTS_ALLOWED_KEYS = {
        constants.CONFIG_EXCHANGES: [constants.CONFIG_ENABLED_OPTION]
    }

    def __init__(self, profile_path: str, schema_path: str = None):
        self.profile_id: str = None
        self.path: str = profile_path
        self.schema_path: str = schema_path or constants.PROFILE_FILE_SCHEMA
        self.name: str = None
        self.description: str = None
        self.avatar: str = None
        self.avatar_path: str = None
        self.read_only: bool = False

        self.config: dict = {}

    def read_config(self) -> None:
        """
        Reads a profile from self.path
        :return: None
        """
        with open(self.config_file()) as profile_file:
            parsed_profile = json.load(profile_file)
            profile_config = parsed_profile.get(constants.CONFIG_PROFILE, {})
            self.profile_id = profile_config.get(constants.CONFIG_ID, str(uuid.uuid4()))
            self.name = profile_config.get(constants.CONFIG_NAME, "")
            self.description = profile_config.get(constants.CONFIG_DESCRIPTION, "")
            self.avatar = profile_config.get(constants.CONFIG_AVATAR, "")
            self.read_only = profile_config.get(constants.CONFIG_READ_ONLY, False)
            self.config = parsed_profile[constants.PROFILE_CONFIG]

        if self.avatar:
            avatar_path = os.path.join(self.path, self.avatar)
            if os.path.isfile(avatar_path):
                self.avatar_path = avatar_path

    def save_config(self, global_config: dict):
        """
        Save ths profile config
        :param global_config: the bot config containing profile data
        :return: None
        """
        for element in self.FULLY_MANAGED_ELEMENTS:
            if element in global_config:
                self.config[element] = global_config[element]
        for element in self.PARTIALLY_MANAGED_ELEMENTS:
            if element in global_config:
                allowed_keys = self.PARTIALLY_MANAGED_ELEMENTS_ALLOWED_KEYS.get(
                    element, None
                )
                if allowed_keys is not None:
                    self._filter_fill_elements(
                        global_config, self.config, element, allowed_keys
                    )
        self.validate_and_save_config()

    def validate(self):
        """
        Validate this profile configuration against self.schema_path
        :return:
        """
        json_util.validate(self.as_dict(), self.schema_path)

    def validate_and_save_config(self) -> None:
        """
        JSON validates this profile and then saves its configuration file
        :return: None
        """
        self.validate()
        self.save()

    def save(self) -> None:
        """
        Saves the current profile configuration file
        :return: None
        """
        with open(self.config_file(), "w") as profile_file:
            json.dump(self.as_dict(), profile_file, indent=4, sort_keys=True)

    def duplicate(self, name: str = None, description: str = None):
        """
        Duplicates the current profile and associates it with a new profile_id
        :param name: name of the profile to create, uses the original's one by default
        :param description: description of the profile to create, uses the original's one by default
        :return: the created profile
        """
        clone = copy.deepcopy(self)
        clone.name = name or clone.name
        clone.description = description or clone.description
        clone.profile_id = str(uuid.uuid4())
        clone.read_only = False
        try:
            clone.path = os.path.join(
                os.path.split(self.path)[0], f"{clone.name}_{clone.profile_id}"
            )
            shutil.copytree(self.path, clone.path)
        except OSError:
            # invalid profile name for a filename
            clone.path = os.path.join(os.path.split(self.path)[0], clone.profile_id)
            shutil.copytree(self.path, clone.path)
        clone.save()
        return clone

    def get_tentacles_config_path(self) -> str:
        """
        :return: The tentacles configurations path
        """
        return os.path.join(self.path, constants.CONFIG_TENTACLES_FILE)

    def as_dict(self) -> dict:
        """
        :return: A dict representation of this profile configuration
        """
        return {
            constants.CONFIG_PROFILE: {
                constants.CONFIG_ID: self.profile_id,
                constants.CONFIG_NAME: self.name,
                constants.CONFIG_DESCRIPTION: self.description,
                constants.CONFIG_AVATAR: self.avatar,
                constants.CONFIG_READ_ONLY: self.read_only,
            },
            constants.PROFILE_CONFIG: self.config,
        }

    def config_file(self):
        """
        :return: the path to this profile config file
        """
        return os.path.join(self.path, constants.PROFILE_CONFIG_FILE)

    def merge_partially_managed_element_into_config(self, config: dict, element: str):
        """
        Merge this profile configuration's partially managed element into the given config
        :param config: dict to merge this profile configuration's partially managed element into
        :param element: the partially managed element to merge
        :return: None
        """
        Profile._merge_partially_managed_element(
            config, self.config, element, Profile.PARTIALLY_MANAGED_ELEMENTS[element]
        )

    @staticmethod
    def _merge_partially_managed_element(
        config: dict, profile_config: dict, element: str, template: dict
    ):
        if element in config:
            for key, val in profile_config[element].items():
                if key in config[element]:
                    if isinstance(config[element][key], dict):
                        # merge profile values for element[key]
                        Profile._merge_partially_managed_element(
                            config[element], profile_config[element], key, template
                        )
                    else:
                        # overwrite element[key] by profile value
                        config[element][key] = copy.deepcopy(
                            profile_config[element][key]
                        )
                else:
                    # use profile value for element[key]
                    if isinstance(val, dict):
                        config[element][key] = Profile._get_element_from_template(
                            template, val
                        )
                    else:
                        config[element][key] = val
        else:
            # use profile value for element
            config[element] = {
                key: Profile._get_element_from_template(template, val)
                for key, val in profile_config[element].items()
            }

    @staticmethod
    def _get_element_from_template(template: dict, profile_values: dict) -> dict:
        merged_values = copy.deepcopy(template)
        merged_values.update(profile_values)
        return merged_values

    @staticmethod
    def _filter_fill_elements(
        config: dict, profile_config: dict, element: str, allowed_keys: list
    ):
        if element in config:
            # reset profile element to avoid saving outdated data
            profile_config[element] = {}
            for key, value in config[element].items():
                if isinstance(value, dict):
                    # handle nested elements
                    Profile._filter_fill_elements(
                        config[element], profile_config[element], key, allowed_keys
                    )
                else:
                    # save allowed keys
                    if key in allowed_keys:
                        profile_config[element][key] = value
