# pylint: disable=R0913
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
import octobot_commons.constants as commons_constants
import octobot_commons.configuration.config_file_manager as config_file_manager
import octobot_commons.configuration.config_operations as config_operations


class Configuration:
    """
    Configuration is managing an OctoBot configuration regarding reading, writing and updating
    """

    def __init__(self, config_path: str, schema_path: str = None):
        self.logger = logging.get_logger(self.__class__.__name__)
        self.config_path = config_path
        self.config = None
        self.config_schema_path = schema_path or commons_constants.CONFIG_FILE_SCHEMA
        self.profile = None
        self.profile_by_id = {}

    def validate(self) -> (bool, object):
        """
        Validated self.config configuration against self.config_schema_path json schema
        :return: a boolean result and the exception if any
        """
        return config_file_manager.validate(
            self.config if self.config else config_file_manager.load(self.config_path),
            self.config_schema_path,
        )

    def read(self, should_raise=True, fill_missing_fields=False) -> None:
        """
        Reads the configuration from self.config_path and load the current profile
        :param should_raise: will raise upon exception when True
        :param fill_missing_fields: will try to fill in missing fields when true
        :return: None
        """
        self.config = config_file_manager.load(
            self.config_path,
            should_raise=should_raise,
            fill_missing_fields=fill_missing_fields,
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
        :return:
        """
        config_file_manager.dump(
            self.config_path,
            self.config,
            temp_restore_config_file=temp_restore_config_file,
            schema_file=schema_file,
        )

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
        update_current_config=False,
        delete=False,
    ) -> None:
        """
        Partially update self.config using the fields found in to_update_fields
        :param to_update_fields: the fields to update
        :param in_backtesting: if backtesting is enabled
        :param config_separator: the config separator
        :param update_current_config: if the current config should be updated
        :param delete: if the data should be removed
        """
        new_current_config = copy.copy(self.config)

        config_operations.filter_to_update_data(to_update_fields, in_backtesting)

        # now can make a deep copy
        new_current_config = copy.deepcopy(new_current_config)

        if delete:
            removed_configs = [
                config_operations.parse_and_update(
                    data_key, config_operations.DELETE_ELEMENT_VALUE, config_separator
                )
                for data_key in to_update_fields
            ]
            functools.reduce(
                config_operations.clear_dictionaries_by_keys,
                [new_current_config] + removed_configs,
            )
            if update_current_config:
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
                [new_current_config] + updated_configs,
            )
            if update_current_config:
                functools.reduce(
                    config_operations.merge_dictionaries_by_appending_keys,
                    [self.config] + updated_configs,
                )

        # save config
        config_file_manager.dump(
            self.config_path,
            new_current_config,
            temp_restore_config_file=commons_constants.TEMP_RESTORE_CONFIG_FILE,
            schema_file=self.config_schema_path,
        )
