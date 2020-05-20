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
from shutil import copy

from octobot_commons.config import is_config_empty_or_missing
from octobot_commons.constants import CONFIG_FILE, DEFAULT_CONFIG_FILE
from octobot_commons.tests.test_config import load_test_config, TEST_CONFIG_FOLDER


def get_fake_config_path():
    return os.path.join(TEST_CONFIG_FOLDER, f"test_{CONFIG_FILE}")


def test_load_config():
    assert load_test_config()


def test_is_config_empty_or_missing():
    if os.path.isfile(get_fake_config_path()):
        os.remove(get_fake_config_path())

    assert is_config_empty_or_missing(config_file=get_fake_config_path())
    copy(os.path.join(TEST_CONFIG_FOLDER, DEFAULT_CONFIG_FILE), get_fake_config_path())
    assert not is_config_empty_or_missing(config_file=get_fake_config_path())

    if os.path.isfile(get_fake_config_path()):
        os.remove(get_fake_config_path())
