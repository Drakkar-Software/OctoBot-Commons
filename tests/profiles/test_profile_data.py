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
#  License along with this library.*
import json
import pytest

import octobot_commons.profiles as profiles
import octobot_commons.constants as constants

from tests.profiles import get_profile_path, profile


@pytest.fixture
def profile_data_dict():
    return {
        'profile_details': {
            'name': 'default',
            'description': 'OctoBot default profile.',
            'id': 'default',
            'origin_url': 'https://default.url',
            'avatar': 'default_profile.png',
            'complexity': 2,
            'risk': 2,
            'type': 'live',
            'bot_id': 'bot_1',
            'imported': False,
            'read_only': False
        },
        'crypto_currencies': [
            {
                'trading_pairs': ['BTC/USDT'],
                'name': 'Bitcoin',
                'enabled': True
            }
        ], 'exchanges': [
            {
                'name': 'binance',
                'type': 'spot',
                'enabled': True,
                'config_name': 'binance_1'
            }
        ], 'trader': {
            'enabled': False,
            'load_trade_history': True
        }, 'trader_simulator': {
            'enabled': True,
            'starting_portfolio': {
                'BTC': 10,
                'USDT': 1000
            },
            'maker_fees': 0.1,
            'taker_fees': 0.1
        }, 'trading': {
            'reference_market': 'BTC',
            'risk': 0.5
        }, 'tentacles': [
            {
                'name': 'plopEvaluator',
                'config': {},
                'enabled': False,
            },
            {
                'name': 'plopEvaluator',
                'enabled': True,
                'config': {
                    'a': True,
                    'other': {
                        'l': [1, 2],
                        'n': None,
                    }
                },
            },
        ]
    }


def test_from_profile(profile):
    profile_data = profiles.ProfileData.from_profile(profile.read_config())
    # check one element per attribute to be sure it's all parsed
    assert profile_data.profile_details.origin_url == "https://default.url"
    assert profile_data.crypto_currencies[0].trading_pairs == ['BTC/USDT']
    assert profile_data.exchanges[0].name == "binance"
    assert profile_data.trader.enabled is False
    assert profile_data.trader_simulator.enabled is True
    assert profile_data.trader_simulator.starting_portfolio == {'BTC': 10, 'USDT': 1000}
    assert profile_data.trading.risk == 0.5
    assert profile_data.tentacles == []


def test_to_profile(profile):
    profile_data = profiles.ProfileData.from_profile(profile.read_config())
    created_profile = profile_data.to_profile("plop_path")
    # force missing values
    for crypto_data in profile.config[constants.CONFIG_CRYPTO_CURRENCIES].values():
        crypto_data[constants.CONFIG_ENABLED_OPTION] = crypto_data.get(constants.CONFIG_ENABLED_OPTION, True)
    for exchange_data in profile.config[constants.CONFIG_EXCHANGES].values():
        exchange_data[constants.CONFIG_ENABLED_OPTION] = exchange_data.get(constants.CONFIG_ENABLED_OPTION, True)
        exchange_data[constants.CONFIG_EXCHANGE_TYPE] = exchange_data.get(constants.CONFIG_EXCHANGE_TYPE,
                                                                          constants.DEFAULT_EXCHANGE_TYPE)
    # if both parsing and transforming return the same profile as original one, the whole chain works
    assert profile.as_dict() == created_profile.as_dict()


def test_from_dict(profile_data_dict):
    profile_data = profiles.ProfileData.from_dict(profile_data_dict)
    # check one element per attribute to be sure it's all parsed
    assert profile_data.profile_details.origin_url == "https://default.url"
    assert profile_data.crypto_currencies[0].trading_pairs == ['BTC/USDT']
    assert profile_data.exchanges[0].name == "binance"
    assert profile_data.trader.enabled is False
    assert profile_data.trader_simulator.enabled is True
    assert profile_data.trader_simulator.starting_portfolio == {'BTC': 10, 'USDT': 1000}
    assert profile_data.trading.risk == 0.5
    assert profile_data.tentacles[0].name == "plopEvaluator"
    assert profile_data.tentacles[1].config["other"]["l"] == [1, 2]


def test_from_dict_objects(profile_data_dict):
    profile_data_objects = profiles.ProfileData.from_dict(profile_data_dict)
    profile_data = profiles.ProfileData.from_dict({
        "profile_details": profile_data_objects.profile_details,
        "crypto_currencies": profile_data_objects.crypto_currencies,
        "exchanges": profile_data_objects.exchanges,
        "trader": profile_data_objects.trader,
        "trader_simulator": profile_data_objects.trader_simulator,
        "trading": profile_data_objects.trading,
        "tentacles": profile_data_objects.tentacles,
    })
    # check one element per attribute to be sure it's all parsed
    assert profile_data.profile_details.origin_url == "https://default.url"
    assert profile_data.crypto_currencies[0].trading_pairs == ['BTC/USDT']
    assert profile_data.exchanges[0].name == "binance"
    assert profile_data.trader.enabled is False
    assert profile_data.trader_simulator.enabled is True
    assert profile_data.trader_simulator.starting_portfolio == {'BTC': 10, 'USDT': 1000}
    assert profile_data.trading.risk == 0.5
    assert profile_data.tentacles[0].name == "plopEvaluator"
    assert profile_data.tentacles[1].config["other"]["l"] == [1, 2]


def test_to_dict(profile_data_dict):
    profile_data = profiles.ProfileData.from_dict(profile_data_dict)
    # if both parsing and transforming return the same profile as original one, the whole chain works
    assert profile_data_dict == profile_data.to_dict()

    dict_without_default_values = profile_data.to_dict(include_default_values=False)
    assert profile_data_dict != dict_without_default_values

    # ensure no empty elements
    assert len(dict_without_default_values) == len(profile_data_dict)
    for values in dict_without_default_values.values():
        assert len(values)
