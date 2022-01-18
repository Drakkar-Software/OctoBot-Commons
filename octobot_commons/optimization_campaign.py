#  This file is part of OctoBot (https://github.com/Drakkar-Software/OctoBot)
#  Copyright (c) 2021 Drakkar-Software, All rights reserved.
#
#  OctoBot is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  OctoBot is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public
#  License along with OctoBot. If not, see <https://www.gnu.org/licenses/>.


class OptimizationCampaign:
    def __init__(self, name=None):
        self.name = name or self.get_campaign_name()

    @classmethod
    def get_campaign_name(cls, *args):
        return _optimization_name_proxy(*args)


DEFAULT_CAMPAIGN = "default_campaign"


def _default_optimization_name_proxy(*_):
    return DEFAULT_CAMPAIGN


_name_proxy = _default_optimization_name_proxy


def _optimization_name_proxy(*args):
    return _name_proxy(*args)


def register_optimization_campaign_name_proxy(new_proxy):
    global _name_proxy
    _name_proxy = new_proxy
