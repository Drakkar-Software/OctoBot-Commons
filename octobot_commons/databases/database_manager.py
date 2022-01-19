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

import octobot_commons.databases.adaptors as adaptors
import octobot_commons.constants as constants
import octobot_commons.symbol_util as symbol_util


class DatabaseManager:
    def __init__(self, tentacle_class, optimization_campaign_name=None, database_adaptor=adaptors.TinyDBAdaptor,
                 backtesting_id=None, optimizer_id=None, context=None):
        self.database_adaptor = database_adaptor
        self.optimization_campaign_name = optimization_campaign_name
        self.backtesting_id = backtesting_id
        self.optimizer_id = optimizer_id
        self.tentacle_class = tentacle_class
        self.context = context
        self.base_path = self._merge_parts(constants.USER_FOLDER, tentacle_class.__name__)
        self.suffix = constants.TINYDB_EXT if self.database_adaptor == adaptors.TinyDBAdaptor else ""

    async def initialize(self, exchange=None):
        if self.database_adaptor == adaptors.TinyDBAdaptor:
            deepest_path = self._base_folder() if exchange is None else self._merge_parts(self._base_folder(), exchange)
            if not os.path.exists(deepest_path):
                os.makedirs(deepest_path)

    def get_run_data_db_identifier(self) -> str:
        return self._merge_parts(self._base_folder(), f"{constants.RUN_DATA_DB}{self.suffix}")

    def get_orders_db_identifier(self) -> str:
        return self._merge_parts(self._base_folder(), f"{constants.ORDERS_DB}{self.suffix}")

    def get_trades_db_identifier(self) -> str:
        return self._merge_parts(self._base_folder(), f"{constants.TRADES_DB}{self.suffix}")

    def get_transactions_db_identifier(self) -> str:
        return self._merge_parts(self._base_folder(), f"{constants.TRANSACTIONS_DB}{self.suffix}")

    def get_symbol_db_identifier(self, exchange, symbol) -> str:
        return self._merge_parts(self._base_folder(), exchange, f"{symbol_util.merge_symbol(symbol)}{self.suffix}")

    def get_backtesting_metadata_identifier(self) -> str:
        return self._merge_parts(self._base_folder(ignore_backtesting_id=True), f"{constants.METADATA}{self.suffix}")

    def get_backtesting_run_folder(self) -> str:
        return self._base_folder()

    def get_optimizer_runs_identifier(self) -> str:
        return self._merge_parts(self._base_folder(ignore_backtesting_id=True))

    def get_optimizer_runs_schedule_identifier(self) -> str:
        return self._merge_parts(self.base_path, self.optimization_campaign_name, constants.OPTIMIZER,
                                 f"{constants.OPTIMIZER_RUNS_SCHEDULE_DB}{self.suffix}")

    async def generate_new_backtesting_id(self) -> int:
        return await self._generate_new_id(is_optimizer=False)

    async def generate_new_optimizer_id(self, back_list) -> int:
        return await self._generate_new_id(back_list=back_list, is_optimizer=True)

    async def _generate_new_id(self, back_list=None, is_optimizer=False):
        back_list = back_list or []
        max_runs = constants.MAX_OPTIMIZER_RUNS if is_optimizer else constants.MAX_BACKTESTING_RUNS
        index = 1
        while index < max_runs:
            if index in back_list:
                index += 1
                continue
            name_candidate = self._base_folder(optimizer_id=index) if is_optimizer\
                else self._base_folder(backtesting_id=index)
            if self.database_adaptor == adaptors.TinyDBAdaptor:
                if self._exists(name_candidate):
                    index += 1
                else:
                    return index
            else:
                raise RuntimeError(f"Unsupported database adaptor runs ({self.database_adaptor}).")
        raise RuntimeError(f"Reached maximum number of {'optimizer' if is_optimizer else 'backtesting'} runs "
                           f"({constants.MAX_BACKTESTING_RUNS}). Please remove some.")

    async def get_optimization_campaign_names(self) -> list:
        if self.database_adaptor == adaptors.TinyDBAdaptor:
            optimization_campaign_folder = self._merge_parts(self.base_path)
            if os.path.exists(optimization_campaign_folder):
                return [self._parse_optimizer_id(folder.name)
                        for folder in os.scandir(optimization_campaign_folder)
                        if os.path.isdir(folder)]
        return []

    async def get_optimizer_run_ids(self) -> list:
        if self.database_adaptor == adaptors.TinyDBAdaptor:
            optimizer_runs_path = self._merge_parts(
                self.base_path, self.optimization_campaign_name, constants.OPTIMIZER
            )
            if os.path.exists(optimizer_runs_path):
                return [self._parse_optimizer_id(folder.name)
                        for folder in os.scandir(optimizer_runs_path)
                        if os.path.isdir(folder)]
        return []

    def _parse_optimizer_id(self, identifier) -> str:
        return identifier.split(constants.DB_SEPARATOR)[-1]

    def _base_folder(self, ignore_backtesting_id=False, backtesting_id=None,
                     ignore_optimizer_id=False, optimizer_id=None) -> str:
        path = self.base_path
        backtesting_id = backtesting_id or self.backtesting_id
        optimizer_id = optimizer_id or self.optimizer_id
        # when in optimizer or backtesting: wrap it into the current campaign
        if backtesting_id is not None or optimizer_id is not None:
            if self.optimization_campaign_name is None:
                raise RuntimeError(f"optimization_campaign_name is required in {DatabaseManager} constructor while "
                                   f"in a backtesting or optimizer context")
            path = self._merge_parts(path, self.optimization_campaign_name)
        if optimizer_id is not None:
            if ignore_optimizer_id:
                path = self._merge_parts(path, constants.OPTIMIZER)
            else:
                path = self._merge_parts(
                    path,
                    constants.OPTIMIZER,
                    f"{constants.OPTIMIZER}{constants.DB_SEPARATOR}{optimizer_id}"
                )
        if backtesting_id is not None:
            if optimizer_id is None:
                path = self._merge_parts(path, constants.BACKTESTING)
            if ignore_backtesting_id:
                return path
            return self._merge_parts(path, f"{constants.BACKTESTING}{constants.DB_SEPARATOR}{backtesting_id}")
        if optimizer_id is None:
            # live mode
            return self._merge_parts(path, constants.LIVE)
        return path

    def _merge_parts(self, *parts):
        return os.path.join(*parts) \
            if self.database_adaptor == adaptors.TinyDBAdaptor \
            else constants.DB_SEPARATOR.join(*parts)

    def _exists(self, identifier):
        if self.database_adaptor == adaptors.TinyDBAdaptor:
            return os.path.exists(identifier)
        raise RuntimeError(f"Unhandled database_adaptor {self.database_adaptor}")
