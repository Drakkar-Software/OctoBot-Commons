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
    def __init__(self, tentacle_class, database_adaptor=adaptors.TinyDBAdaptor, backtesting_id=None,
                 optimizer_id=None, context=None):
        self.database_adaptor = database_adaptor
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

    def get_symbol_db_identifier(self, exchange, symbol) -> str:
        return self._merge_parts(self._base_folder(), exchange, f"{symbol_util.merge_symbol(symbol)}{self.suffix}")

    def get_backtesting_metadata_identifier(self) -> str:
        return self._merge_parts(self._base_folder(ignore_backtesting_id=True, ignore_optimizer_id=True),
                                 f"{constants.METADATA}{self.suffix}")

    def get_optimizer_runs_schedule_identifier(self) -> str:
        return self._merge_parts(self.base_path, constants.OPTIMIZER,
                                 f"{constants.OPTIMIZER_RUNS_SCHEDULE_DB}{self.suffix}")

    async def generate_new_backtesting_id(self) -> int:
        index = 1
        while index < constants.MAX_BACKTESTING_RUNS:
            name_candidate = self._base_folder(backtesting_id=index)
            if self._exists(name_candidate):
                index += 1
            else:
                return index
        raise RuntimeError(f"Reached maximum number of backtesting runs ({constants.MAX_BACKTESTING_RUNS}). "
                           f"Please remove some.")

    async def get_optimizer_run_ids(self) -> list:
        if self.database_adaptor == adaptors.TinyDBAdaptor:
            optimizer_runs_path = self._merge_parts(self.base_path, constants.OPTIMIZER)
            if os.path.exists(optimizer_runs_path):
                return [folder
                        for folder in os.scandir(optimizer_runs_path)
                        if os.path.isdir(folder)]
        return []

    def _base_folder(self, ignore_backtesting_id=False, backtesting_id=None, ignore_optimizer_id=False) -> str:
        path = self.base_path
        backtesting_id = backtesting_id or self.backtesting_id
        if self.optimizer_id is not None:
            if ignore_optimizer_id:
                path = self._merge_parts(path, constants.OPTIMIZER)
            else:
                path = self._merge_parts(
                    path,
                    constants.OPTIMIZER,
                    f"{constants.OPTIMIZER}{constants.DB_SEPARATOR}{self.optimizer_id}"
                )
        if backtesting_id is not None:
            if self.optimizer_id is None:
                path = self._merge_parts(path, constants.BACKTESTING)
            if ignore_backtesting_id:
                return path
            return self._merge_parts(path, f"{constants.BACKTESTING}{constants.DB_SEPARATOR}{backtesting_id}")
        if self.optimizer_id is None:
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
