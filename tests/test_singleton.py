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
from octobot_commons.singleton.singleton_class import Singleton


class TestSingleton(Singleton):
    def __init__(self):
        self.test_attr = ""


instance = TestSingleton().instance()


def test_create_instance():
    assert TestSingleton.instance() is instance


def test_instance_attribute():
    instance.test_attr = "test"
    assert TestSingleton.instance().test_attr == "test"
