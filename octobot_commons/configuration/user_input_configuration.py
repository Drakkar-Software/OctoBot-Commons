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

import octobot_commons.logging as logging
try:
    import octobot_tentacles_manager.api
except ImportError:
    pass


def load_user_inputs_from_class(configured_class, tentacles_setup_config, to_fill_config):
    """
    Apply the given tentacles_setup_config configuration to the given to_fill_config using configured_class user inputs
    Requires octobot_tentacles_manager import, configured_class.UI, configured_class.init_user_inputs
    and configured_class.get_name
    :return: the filled user input configuration
    """
    logger = logging.get_logger(configured_class.get_name())
    inputs = {}
    try:
        to_fill_config.update(
            octobot_tentacles_manager.api.get_tentacle_config(
                tentacles_setup_config,
                configured_class
            )
        )
    except NotImplementedError:
        # get_name not implemented, no tentacle config
        return inputs
    try:
        with configured_class.UI.local_factory(configured_class, lambda: to_fill_config):
            configured_class.init_user_inputs(inputs)
    except Exception as e:
        logger.exception(e, True, f"Error when initializing user inputs: {e}")
    if to_fill_config:
        logger.debug(f"Using config: {to_fill_config}")
    return inputs


def get_raw_config_and_user_inputs_from_class(configured_class, tentacles_setup_config):
    """
    Requires octobot_tentacles_manager import and configured_class.load_user_inputs
    :return: the filled user input configuration of configured_class according to the given tentacles_setup_config
    """
    loaded_config = octobot_tentacles_manager.api.get_tentacle_config(tentacles_setup_config, configured_class)
    user_inputs = configured_class.load_user_inputs(tentacles_setup_config, loaded_config)
    return loaded_config, list(user_input.to_dict() for user_input in user_inputs.values())
