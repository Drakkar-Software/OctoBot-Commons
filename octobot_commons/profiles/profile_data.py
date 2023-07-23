# pylint: disable=C0103,R0902
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
import dataclasses

import octobot_commons.profiles.profile as profile_import
import octobot_commons.minimizable_dataclass as minimizable_dataclass
import octobot_commons.enums as enums
import octobot_commons.constants as constants


@dataclasses.dataclass
class ProfileDetailsData:
    name: str
    description: str
    id: str = None
    origin_url: str = None
    avatar: str = None
    complexity: int = enums.ProfileComplexity.MEDIUM.value
    risk: int = enums.ProfileRisk.MODERATE.value
    type: str = enums.ProfileType.LIVE.value
    imported: bool = False
    read_only: bool = False
    bot_id: str = None


@dataclasses.dataclass
class CryptoCurrencyData:
    trading_pairs: list[str]
    name: str = None
    enabled: bool = True


@dataclasses.dataclass
class ExchangeData:
    name: str
    type: str = constants.DEFAULT_EXCHANGE_TYPE
    enabled: bool = True
    config_name: str = None


@dataclasses.dataclass
class TraderData:
    enabled: bool
    load_trade_history: bool = True


@dataclasses.dataclass
class TraderSimulatorData:
    enabled: bool
    starting_portfolio: dict[str, float]
    maker_fees: float = 0.0
    taker_fees: float = 0.0


@dataclasses.dataclass
class TradingData:
    reference_market: str
    risk: float = 1.0


@dataclasses.dataclass
class TentaclesData:
    name: str
    config: dict = None
    enabled: bool = True


@dataclasses.dataclass
class ProfileData(minimizable_dataclass.MinimizableDataclass):
    profile_details: ProfileDetailsData
    crypto_currencies: list[CryptoCurrencyData]
    exchanges: list[ExchangeData]
    trader: TraderData
    trader_simulator: TraderSimulatorData
    trading: TradingData
    tentacles: list[TentaclesData] = None

    # pylint: disable=E1134
    def __post_init__(self):
        if isinstance(self.profile_details, dict):
            self.profile_details = ProfileDetailsData(**self.profile_details)
        if self.crypto_currencies and isinstance(self.crypto_currencies[0], dict):
            self.crypto_currencies = [
                CryptoCurrencyData(**crypto_currency)
                for crypto_currency in self.crypto_currencies
            ]
        if self.exchanges and isinstance(self.exchanges[0], dict):
            self.exchanges = [ExchangeData(**exchange) for exchange in self.exchanges]
        if isinstance(self.trader, dict):
            self.trader = TraderData(**self.trader)
        if isinstance(self.trader_simulator, dict):
            self.trader_simulator = TraderSimulatorData(**self.trader_simulator)
        if isinstance(self.trading, dict):
            self.trading = TradingData(**self.trading)
        if self.tentacles and isinstance(self.tentacles[0], dict):
            self.tentacles = (
                [TentaclesData(**tentacle) for tentacle in self.tentacles]
                if self.tentacles
                else []
            )

    @classmethod
    def from_profile(cls, profile: profile_import.Profile):
        """
        Creates a cls instance from the given profile
        """
        profile_dict = profile.as_dict()
        content = profile_dict[constants.PROFILE_CONFIG]
        return cls.from_dict(
            {
                "profile_details": profile_dict[constants.CONFIG_PROFILE],
                "crypto_currencies": [
                    {
                        "trading_pairs": details.get(constants.CONFIG_CRYPTO_PAIRS, []),
                        "name": currency,
                        "enabled": details.get(constants.CONFIG_ENABLED_OPTION, True),
                    }
                    for currency, details in content[
                        constants.CONFIG_CRYPTO_CURRENCIES
                    ].items()
                ],
                "exchanges": [
                    {
                        "name": exchange,
                        "type": details.get(
                            constants.CONFIG_EXCHANGE_TYPE,
                            constants.DEFAULT_EXCHANGE_TYPE,
                        ),
                        "enabled": details.get(constants.CONFIG_ENABLED_OPTION, True),
                    }
                    for exchange, details in content[constants.CONFIG_EXCHANGES].items()
                ],
                "trader": {
                    "enabled": content[constants.CONFIG_TRADER][
                        constants.CONFIG_ENABLED_OPTION
                    ],
                    "load_trade_history": content[constants.CONFIG_TRADER].get(
                        constants.CONFIG_LOAD_TRADE_HISTORY, True
                    ),
                },
                "trader_simulator": {
                    "enabled": content[constants.CONFIG_SIMULATOR][
                        constants.CONFIG_ENABLED_OPTION
                    ],
                    "starting_portfolio": content[constants.CONFIG_SIMULATOR][
                        constants.CONFIG_STARTING_PORTFOLIO
                    ],
                    "maker_fees": content[constants.CONFIG_SIMULATOR][
                        constants.CONFIG_SIMULATOR_FEES
                    ].get(constants.CONFIG_SIMULATOR_FEES_MAKER, 0.0),
                    "taker_fees": content[constants.CONFIG_SIMULATOR][
                        constants.CONFIG_SIMULATOR_FEES
                    ].get(constants.CONFIG_SIMULATOR_FEES_TAKER, 0.0),
                },
                "trading": {
                    "reference_market": content[constants.CONFIG_TRADING][
                        constants.CONFIG_TRADER_REFERENCE_MARKET
                    ],
                    "risk": content[constants.CONFIG_TRADING][
                        constants.CONFIG_TRADER_RISK
                    ],
                },
                "tentacles": [],
            }
        )

    def to_profile(self, to_create_profile_path: str) -> profile_import.Profile:
        """
        Returns a new Profile from self
        """
        profile = profile_import.Profile(to_create_profile_path)
        profile.from_dict(self._to_profile_dict())
        return profile

    def set_tentacles_config(self, config_by_tentacle: dict):
        """
        Update self.tentacles from the given config_by_tentacle
        """
        self.tentacles = [
            TentaclesData(name=tentacle, config=config)
            for tentacle, config in config_by_tentacle.items()
        ]

    def _to_profile_dict(self) -> dict:
        return {
            constants.PROFILE_CONFIG: {
                constants.CONFIG_CRYPTO_CURRENCIES: {
                    crypto_currency.name: {
                        constants.CONFIG_CRYPTO_PAIRS: crypto_currency.trading_pairs,
                        constants.CONFIG_ENABLED_OPTION: crypto_currency.enabled,
                    }
                    for crypto_currency in self.crypto_currencies
                },
                constants.CONFIG_EXCHANGES: {
                    exchange.name: {
                        constants.CONFIG_EXCHANGE_TYPE: exchange.type,
                        constants.CONFIG_ENABLED_OPTION: exchange.enabled,
                    }
                    for exchange in self.exchanges
                },
                constants.CONFIG_TRADER: {
                    constants.CONFIG_ENABLED_OPTION: self.trader.enabled,
                    constants.CONFIG_LOAD_TRADE_HISTORY: self.trader.load_trade_history,
                },
                constants.CONFIG_SIMULATOR: {
                    constants.CONFIG_ENABLED_OPTION: self.trader_simulator.enabled,
                    constants.CONFIG_STARTING_PORTFOLIO: self.trader_simulator.starting_portfolio,
                    constants.CONFIG_SIMULATOR_FEES: {
                        constants.CONFIG_SIMULATOR_FEES_MAKER: self.trader_simulator.maker_fees,
                        constants.CONFIG_SIMULATOR_FEES_TAKER: self.trader_simulator.taker_fees,
                    },
                },
                constants.CONFIG_TRADING: {
                    constants.CONFIG_TRADER_REFERENCE_MARKET: self.trading.reference_market,
                    constants.CONFIG_TRADER_RISK: self.trading.risk,
                },
            },
            constants.CONFIG_PROFILE: dataclasses.asdict(self.profile_details),
        }
