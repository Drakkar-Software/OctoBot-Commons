# pylint: disable=R0913, R0902, W0703
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
import os
import functools
import copy
import octobot_commons.logging as logging
import octobot_commons.errors as errors
import octobot_commons.constants as commons_constants
import octobot_commons.profiles as profiles
import octobot_commons.json_util as json_util
import octobot_commons.configuration.config_file_manager as config_file_manager
import octobot_commons.configuration.config_operations as config_operations


class Configuration:
    """
    Configuration is managing an OctoBot configuration regarding reading, writing and updating
    """

    def __init__(
        self,
        config_path: str,
        profiles_path: str,
        schema_path: str = None,
        profile_schema_path: str = None,
    ):
        self.logger = logging.get_logger(self.__class__.__name__)
        self.config_path: str = config_path
        self.profiles_path: str = profiles_path
        self.config: dict = None
        self.config_schema_path: str = (
            schema_path or commons_constants.CONFIG_FILE_SCHEMA
        )
        self.profile_schema_path: str = (
            profile_schema_path or commons_constants.PROFILE_FILE_SCHEMA
        )

        self._read_config: dict = None
        self._profile: profiles.Profile = None
        self._profile_by_id: dict = {}

    def validate(self) -> None:
        """
        Validated self._read_config and self._profile against their json schema
        :return: None
        """
        json_util.validate(self._read_config, self.config_schema_path)
        self._profile.validate()

    def read(self, should_raise=True, fill_missing_fields=False) -> None:
        """
        Reads the configuration from self.config_path and load the current profile
        Overall config is stored into self.config and consists of a merger from the user
        config and activated profile
        :param should_raise: will raise upon exception when True
        :param fill_missing_fields: will try to fill in missing fields when true
        :return: None
        """
        self._read_config = config_file_manager.load(
            self.config_path,
            should_raise=should_raise,
            fill_missing_fields=fill_missing_fields,
        )
        self._load_profiles()
        self._profile = self._get_selected_profile()
        self.logger.info(f"Using {self._profile.name} profile.")
        self._generate_config_from_user_config_and_profile()

    def _generate_config_from_user_config_and_profile(self):
        self.config = copy.deepcopy(self._read_config)
        for profile_managed_element in self._profile.FULLY_MANAGED_ELEMENTS:
            self.config[profile_managed_element] = copy.deepcopy(
                self._profile.config[profile_managed_element]
            )
        for partially_managed_element in self._profile.PARTIALLY_MANAGED_ELEMENTS:
            self._profile.merge_partially_managed_element_into_config(
                self.config, partially_managed_element
            )

    def save(
        self,
        temp_restore_config_file=commons_constants.TEMP_RESTORE_CONFIG_FILE,
        schema_file=None,
    ) -> None:
        """
        Save the current self.config and self.profile
        :param temp_restore_config_file:
        :param schema_file:
        :return: None
        """
        config_to_save = self._get_config_without_profile_elements()
        config_file_manager.dump(
            self.config_path,
            config_to_save,
            temp_restore_config_file=temp_restore_config_file,
            schema_file=schema_file,
        )
        self._profile.save_config(self.config)

    def is_loaded(self):
        """
        Checks if self has been loaded
        :return: True when self has been loaded (read)
        """
        return self.config is not None

    def is_config_file_empty_or_missing(self):
        """
        Checks if self.config_path existing and not empty
        :return: True when self.config_path is existing and non empty
        """
        return (not os.path.isfile(self.config_path)) or os.stat(
            self.config_path
        ).st_size == 0

    def get_tentacles_config_path(self):
        """
        :return: The tentacles configurations associated to the activated profile
        """
        return os.path.join(self._profile.path, commons_constants.CONFIG_TENTACLES_FILE)

    def get_metrics_enabled(self) -> bool:
        """
        Check if metrics are enabled
        :return: True if metrics are enabled
        """
        try:
            return bool(
                self.config[commons_constants.CONFIG_METRICS].get(
                    commons_constants.CONFIG_ENABLED_OPTION, True
                )
            )
        except KeyError:
            return True

    def accepted_terms(self) -> bool:
        """
        Check if terms has been accepted
        :return: the check result
        """
        if commons_constants.CONFIG_ACCEPTED_TERMS in self.config:
            return self.config[commons_constants.CONFIG_ACCEPTED_TERMS]
        return False

    def accept_terms(self, accepted) -> None:
        """
        Perform terms acceptation
        :param accepted: accepted or not
        """
        self.config[commons_constants.CONFIG_ACCEPTED_TERMS] = accepted
        self.save()

    def update_config_fields(
        self,
        to_update_fields,
        in_backtesting,
        config_separator,
        delete=False,
    ) -> None:
        """
        Partially update self.config using the fields found in to_update_fields
        :param to_update_fields: the fields to update
        :param in_backtesting: if backtesting is enabled
        :param config_separator: the config separator
        :param delete: if the data should be removed
        """
        config_operations.filter_to_update_data(to_update_fields, in_backtesting)

        if delete:
            removed_configs = [
                config_operations.parse_and_update(
                    data_key, config_operations.DELETE_ELEMENT_VALUE, config_separator
                )
                for data_key in to_update_fields
            ]
            functools.reduce(
                config_operations.clear_dictionaries_by_keys,
                [self.config] + removed_configs,
            )
        else:
            updated_configs = [
                config_operations.parse_and_update(
                    data_key, data_value, config_separator
                )
                for data_key, data_value in to_update_fields.items()
            ]
            # merge configs
            functools.reduce(
                config_operations.merge_dictionaries_by_appending_keys,
                [self.config] + updated_configs,
            )

        # save config
        self.save(schema_file=self.config_schema_path)

    def _get_selected_profile(self):
        selected_profile_id = self._read_config.get(
            commons_constants.CONFIG_PROFILE, commons_constants.DEFAULT_PROFILE
        )
        try:
            return self._profile_by_id[selected_profile_id]
        except KeyError as err:
            if (
                selected_profile_id != commons_constants.DEFAULT_PROFILE
                and commons_constants.DEFAULT_PROFILE in self._profile_by_id
            ):
                return self._profile_by_id[commons_constants.DEFAULT_PROFILE]
            raise errors.NoProfileError from err

    def _load_profiles(self):
        for profile_entry in os.scandir(self.profiles_path):
            self.load_profile(profile_entry.path)

    def _get_config_without_profile_elements(self) -> dict:
        filtered_config = copy.deepcopy(self.config)
        # do not include profile fully managed elements into filtered config
        for profile_managed_element in self._profile.FULLY_MANAGED_ELEMENTS:
            filtered_config.pop(profile_managed_element, None)
        return filtered_config

    def load_profile(self, profile_path):
        """
        Loads a profile identified by its path if profile_path is actually a profile
        :param profile_path: path to the profile to load
        :return: None
        """
        profile = profiles.Profile(profile_path, self.profile_schema_path)
        try:
            if os.path.isfile(profile.config_file()):
                profile.read_config()
                self._profile_by_id[profile.profile_id] = profile
            else:
                self.logger.debug(
                    f"Ignored {profile_path} as it does not contain a profile configuration"
                )
        except Exception as err:
            self.logger.exception(
                err, True, f"Error when reading profile at '{profile_path}': {err}"
            )
