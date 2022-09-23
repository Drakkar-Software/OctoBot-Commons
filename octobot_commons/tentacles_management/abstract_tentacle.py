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


import octobot_commons.dict_util as dict_util
import octobot_commons.enums as commons_enums
import octobot_commons.configuration as configuration
import octobot_commons.databases as databases


class AbstractTentacle:
    """
    The parent class of any OctoBot tentacle
    """

    __metaclass__ = abc.ABCMeta
    USER_INPUT_TENTACLE_TYPE = commons_enums.UserInputTentacleTypes.UNDEFINED
    ALLOW_SUPER_CLASS_CONFIG = False

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

    @classmethod
    def get_user_commands(cls) -> dict:
        """
        Return the dict of user commands for this tentacle
        :return: the commands dict
        """
        return {}

    def get_local_config(self):
        raise NotImplementedError

    @classmethod
    def create_local_instance(cls, config, tentacles_setup_config, tentacle_config):
        raise NotImplementedError

    def init_user_inputs(self, inputs: dict) -> None:
        """
        Called right before starting the tentacle, should define all the tentacle's user inputs unless
        those are defined somewhere else.
        """
        pass

    async def load_and_save_user_inputs(self, bot_id: str):
        try:
            inputs = {}
            self.init_user_inputs(inputs)
            run_db = databases.RunDatabasesProvider.instance().get_run_db(bot_id)
            for user_input in inputs.values():
                await configuration.save_user_input(user_input, run_db)
        except Exception as e:
            self.logger.exception(e, True, f"Error when initializing user inputs: {e}")

    @classmethod
    async def get_raw_config_and_user_inputs(cls, config, tentacles_setup_config, bot_id):
        try:
            import octobot_tentacles_manager.api as api
            specific_config = api.get_tentacle_config(tentacles_setup_config, cls)
            if saved_user_inputs := await configuration.get_user_inputs(
                databases.RunDatabasesProvider.instance().get_run_db(bot_id),
                cls.get_name()
            ):
                # user inputs have been saved in run database, use those as they might contain additional
                # (nested) user inputs
                return specific_config, saved_user_inputs
            # use user inputs from init_user_inputs
            tentacle_instance = cls.create_local_instance(config, tentacles_setup_config, specific_config)
            user_inputs = {}
            tentacle_instance.init_user_inputs(user_inputs)
            return specific_config, list(user_inputs.values())
        except ImportError as err:
            raise ImportError("octobot_tentacles_manager is required") from err

    def user_input(
            self,
            name: str,
            input_type,
            def_val,
            registered_inputs: dict,
            min_val=None,
            max_val=None,
            options=None,
            title=None,
            item_title=None,
            other_schema_values=None,
            editor_options=None,
            read_only=False,
            is_nested_config=None,
            nested_tentacle=None,
            parent_input_name=None,
            show_in_summary=True,
            show_in_optimizer=True,
            path=None,
            order=None,
    ):
        """
        Set and return a user input value.
        The returned value is set as an attribute named as the "name" param with " " replaced by "_"
        in self.specific_config.
        Types are: int, float, boolean, options, multiple-options, text, object
        :return: the saved_config value if any, def_val otherwise
        """
        value = def_val
        sanitized_name = configuration.sanitize_user_input_name(name)
        parent = self.get_local_config()
        if parent_input_name is not None:
            found, nested_parent = dict_util.find_nested_value(
                self.get_local_config(), configuration.sanitize_user_input_name(parent_input_name)
            )
            if found and isinstance(nested_parent, dict):
                # non dict nested parents are not supported
                parent = nested_parent
            else:
                parent = None
        if parent is not None:
            try:
                value = parent[sanitized_name]
            except KeyError:
                # use default value
                pass
        input_key = f"{parent_input_name}{name}"
        if input_key not in registered_inputs:
            # do not register user input multiple times
            registered_inputs[input_key] = configuration.format_user_input(
                name,
                input_type,
                value,
                def_val,
                self.USER_INPUT_TENTACLE_TYPE.value,
                self.get_name(),
                min_val=min_val,
                max_val=max_val,
                options=options,
                title=title,
                item_title=item_title,
                other_schema_values=other_schema_values,
                editor_options=editor_options,
                read_only=read_only,
                is_nested_config=is_nested_config,
                nested_tentacle=nested_tentacle,
                parent_input_name=parent_input_name,
                show_in_summary=show_in_summary,
                show_in_optimizer=show_in_optimizer,
                path=path,
                order=order,
            )
        if parent is not None:
            parent[sanitized_name] = value
        return value
