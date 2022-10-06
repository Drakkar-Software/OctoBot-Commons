# pylint: disable=C0103,W0703,C0415
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


import octobot_commons.enums as commons_enums
import octobot_commons.configuration as configuration
import octobot_commons.databases as databases


class AbstractTentacle:
    """
    The parent class of any OctoBot tentacle
    """

    __metaclass__ = abc.ABCMeta
    ALLOW_SUPER_CLASS_CONFIG = False
    USER_INPUT_TENTACLE_TYPE = commons_enums.UserInputTentacleTypes.UNDEFINED

    def __init__(self):
        self.logger = None
        self.UI: configuration.UserInputFactory = configuration.UserInputFactory(
            self.USER_INPUT_TENTACLE_TYPE
        )
        self.UI.set_tentacle_class(self.__class__).set_tentacle_config_proxy(
            self.get_local_config
        )

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
        """
        :return: the config of the tentacle
        """
        raise NotImplementedError

    @classmethod
    def create_local_instance(cls, config, tentacles_setup_config, tentacle_config):
        """
        :param config: the global configuration to give to the tentacle
        :param tentacles_setup_config: the global tentacles setup configuration to give to the tentacle
        :param tentacle_config: the tentacle configuration to give to the tentacle
        :return: a local, aimed to be short-lived, tentacle instance
        """
        raise NotImplementedError

    def init_user_inputs(self, inputs: dict) -> None:
        """
        Called right before starting the tentacle, should define all the tentacle's user inputs unless
        those are defined somewhere else.
        """

    async def load_and_save_user_inputs(self, bot_id: str):
        """
        Initialize and save the user inputs of the tentacle
        """
        try:
            inputs = {}
            self.init_user_inputs(inputs)
            if databases.RunDatabasesProvider.instance().is_storage_enabled(bot_id):
                run_db = databases.RunDatabasesProvider.instance().get_run_db(bot_id)
                await configuration.clear_user_inputs(run_db, self.get_name())
                for user_input in inputs.values():
                    await configuration.save_user_input(user_input, run_db)
                await run_db.flush()
        except Exception as err:
            self.logger.exception(
                err, True, f"Error when initializing user inputs: {err}"
            )

    @classmethod
    async def get_raw_config_and_user_inputs(
        cls, config, tentacles_setup_config, bot_id
    ):
        """
        :return: the tentacle configuration and its list of user inputs
        """
        try:
            import octobot_tentacles_manager.api as api

            specific_config = api.get_tentacle_config(tentacles_setup_config, cls)
        except ImportError as err:
            raise ImportError("octobot_tentacles_manager is required") from err
        if saved_user_inputs := await configuration.get_user_inputs(
            databases.RunDatabasesProvider.instance().get_run_db(bot_id),
            cls.get_name(),
        ):
            # user inputs have been saved in run database, use those as they might contain additional
            # (nested) user inputs
            return specific_config, saved_user_inputs
        # use user inputs from init_user_inputs
        tentacle_instance = cls.create_local_instance(
            config, tentacles_setup_config, specific_config
        )
        user_inputs = {}
        tentacle_instance.init_user_inputs(user_inputs)
        return specific_config, list(
            user_input.to_dict() for user_input in user_inputs.values()
        )
