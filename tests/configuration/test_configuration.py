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
import shutil
import pytest
import octobot_commons.configuration as configuration
import octobot_commons.constants as constants
import octobot_commons.tests.test_config as test_config


def get_fake_config_path():
    return os.path.join(test_config.TEST_CONFIG_FOLDER, f"test_{constants.CONFIG_FILE}")


@pytest.fixture()
def config():
    return configuration.Configuration(get_fake_config_path())


def test_load_config():
    assert test_config.load_test_config()


def test_is_config_empty_or_missing(config):
    if os.path.isfile(get_fake_config_path()):
        os.remove(get_fake_config_path())

    assert config.is_config_file_empty_or_missing()
    shutil.copy(os.path.join(test_config.TEST_CONFIG_FOLDER, constants.DEFAULT_CONFIG_FILE), get_fake_config_path())
    assert not config.is_config_file_empty_or_missing()

    if os.path.isfile(get_fake_config_path()):
        os.remove(get_fake_config_path())
