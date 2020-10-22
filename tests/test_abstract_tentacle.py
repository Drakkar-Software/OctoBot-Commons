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
from octobot_commons.tentacles_management.abstract_tentacle import AbstractTentacle


class TentacleTest(AbstractTentacle):
    pass


class TentacleTestChild(TentacleTest):
    pass


def test_get_name():
    assert TentacleTest().get_name() == "TentacleTest"
    assert TentacleTestChild().get_name() == "TentacleTestChild"


def test_get_all_subclasses():
    assert TentacleTest().get_all_subclasses() == [TentacleTestChild]
