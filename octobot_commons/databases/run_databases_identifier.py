# pylint: disable=R0902,R0913,C0415
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

import octobot_commons.databases.document_database_adaptors as adaptors
import octobot_commons.constants as constants
import octobot_commons.enums as enums
import octobot_commons.symbols.symbol_util as symbol_util


class RunDatabasesIdentifier:
    def __init__(
        self,
        tentacle_class,
        optimization_campaign_name=None,
        database_adaptor=adaptors.TinyDBAdaptor,
        backtesting_id=None,
        optimizer_id=None,
        context=None,
    ):
        self.database_adaptor = database_adaptor
        self.optimization_campaign_name = optimization_campaign_name
        self.backtesting_id = backtesting_id
        self.optimizer_id = optimizer_id
        self.tentacle_class = tentacle_class
        self.context = context
        self.data_path = self._merge_parts(constants.USER_FOLDER, constants.DATA_FOLDER)
        self.base_path = self._merge_parts(self.data_path, tentacle_class.__name__)
        self.suffix = (
            self.database_adaptor.get_db_file_ext()
            if self.database_adaptor.is_file_system_based()
            else ""
        )

    async def initialize(self, exchange=None, from_global_history=False):
        """
        Initializes the necessary elements for these run databases. Creates necessary folder on file system databases
        :param exchange: name of the associated exchange
        :param from_global_history: When True, initializes the run databases as not related to a specific trading mode.
        Used for live trading cross trading mode stats (such as profitability)
        """
        # global history is a live only feature
        from_global_history = from_global_history and self.backtesting_id is None
        deepest_identifier = (
            self._base_folder(from_global_history=from_global_history)
            if exchange is None
            else self._merge_parts(
                self._base_folder(from_global_history=from_global_history), exchange
            )
        )
        await self.database_adaptor.create_identifier(deepest_identifier)

    def get_run_data_db_identifier(self) -> str:
        """
        :return: the database identifier associated to the run database
        """
        return self._get_db_identifier(enums.RunDatabases.RUN_DATA_DB.value, None)

    def get_orders_db_identifier(self, exchange) -> str:
        """
        :return: the database identifier associated to this exchange's orders
        :param exchange: name of the associated exchange
        """
        return self._get_db_identifier(enums.RunDatabases.ORDERS_DB.value, exchange)

    def get_trades_db_identifier(self, exchange) -> str:
        """
        :return: the database identifier associated to this exchange's trades
        :param exchange: name of the associated exchange
        """
        return self._get_db_identifier(enums.RunDatabases.TRADES_DB.value, exchange)

    def get_transactions_db_identifier(self, exchange) -> str:
        """
        :return: the database identifier associated to this exchange's transactions
        :param exchange: name of the associated exchange
        """
        return self._get_db_identifier(
            enums.RunDatabases.TRANSACTIONS_DB.value, exchange
        )

    def get_symbol_db_identifier(self, exchange, symbol) -> str:
        """
        :return: the database identifier associated to this exchange's symbol data
        :param exchange: name of the associated exchange
        :param symbol: the associated symbol
        """
        return self._get_db_identifier(symbol_util.merge_symbol(symbol), exchange)

    def get_historical_portfolio_value_db_identifier(
        self, exchange, portfolio_type_suffix
    ) -> str:
        """
        :return: the database identifier associated to this exchange's historical portfolio value
        :param exchange: name of the associated exchange
        :param portfolio_type_suffix: a suffix identifying the type of portfolio (future / sandbox etc)
        """
        return self._get_db_identifier(
            f"{enums.RunDatabases.PORTFOLIO_VALUE_DB.value}{portfolio_type_suffix}",
            exchange,
            from_global_history=self.backtesting_id is None,
        )

    def get_backtesting_metadata_identifier(self) -> str:
        """
        :return: the database identifier associated to backtesting metadata
        """
        return self._get_db_identifier(
            f"{enums.RunDatabases.METADATA.value}", None, ignore_backtesting_id=True
        )

    def _get_db_identifier(self, run_database_name, exchange, **base_folder_kwargs):
        if exchange is None:
            return self._merge_parts(
                self._base_folder(**base_folder_kwargs),
                f"{run_database_name}{self.suffix}",
            )
        return self._merge_parts(
            self._base_folder(**base_folder_kwargs),
            exchange,
            f"{run_database_name}{self.suffix}",
        )

    async def exchange_base_identifier_exists(self, exchange) -> bool:
        """
        :return: True if there are data under this exchange name
        """
        identifier = self._merge_parts(self._base_folder(), exchange)
        return await self.database_adaptor.identifier_exists(identifier, False)

    async def get_single_existing_exchange(self) -> str:
        """
        :return: the name of the only exchange the backtesting happened on if it only ran on a single exchange,
        None otherwise
        """
        ignored_folders = [enums.RunDatabases.LIVE.value]
        try:
            import octobot_tentacles_manager.constants as tentacles_manager_constants

            ignored_folders.append(
                tentacles_manager_constants.TENTACLES_SPECIFIC_CONFIG_FOLDER
            )
        except ImportError:
            pass
        return await self.database_adaptor.get_single_sub_identifier(
            self._base_folder(), ignored_folders
        )

    async def symbol_base_identifier_exists(self, exchange, symbol) -> bool:
        """
        :return: True if there are data under this exchange name
        """
        identifier = self._merge_parts(
            self._base_folder(),
            exchange,
            f"{symbol_util.merge_symbol(symbol)}{self.suffix}",
        )
        return await self.database_adaptor.identifier_exists(identifier, True)

    def get_backtesting_run_folder(self) -> str:
        """
        :return: base folder associated to a backtesting run
        """
        return self._base_folder()

    def get_optimizer_runs_schedule_identifier(self) -> str:
        """
        :return: the identifier associated to the optimizer run schedule database
        """
        return self._merge_parts(
            self.base_path,
            self.optimization_campaign_name,
            enums.RunDatabases.OPTIMIZER.value,
            f"{enums.RunDatabases.OPTIMIZER_RUNS_SCHEDULE_DB.value}" f"{self.suffix}",
        )

    async def generate_new_backtesting_id(self) -> int:
        """
        :return: a new unique backtesting id
        """
        return await self._generate_new_id(is_optimizer=False)

    async def generate_new_optimizer_id(self, back_list) -> int:
        """
        :return: a new unique optimizer id
        """
        return await self._generate_new_id(back_list=back_list, is_optimizer=True)

    def remove_all(self):
        """
        Clears every data from a backtesting run
        """
        identifier = self._base_folder()
        if self.database_adaptor.is_file_system_based():
            if os.path.isdir(identifier):
                shutil.rmtree(identifier)
            return
        raise RuntimeError(f"Unhandled database_adaptor {self.database_adaptor}")

    async def _generate_new_id(self, back_list=None, is_optimizer=False):
        back_list = back_list or []
        max_runs = (
            constants.MAX_OPTIMIZER_RUNS
            if is_optimizer
            else constants.MAX_BACKTESTING_RUNS
        )
        for index in range(1, max_runs + 1):
            if index in back_list:
                continue
            name_candidate = (
                self._base_folder(optimizer_id=index)
                if is_optimizer
                else self._base_folder(backtesting_id=index)
            )
            if not await self.database_adaptor.identifier_exists(name_candidate, False):
                return index
        raise RuntimeError(
            f"Reached maximum number of {'optimizer' if is_optimizer else 'backtesting'} runs "
            f"({constants.MAX_BACKTESTING_RUNS}). Please remove some."
        )

    async def get_optimization_campaign_names(self) -> list:
        """
        :return: a list of every existing campaign name
        """
        optimization_campaign_folder = self._merge_parts(self.base_path)
        if await self.database_adaptor.identifier_exists(
            optimization_campaign_folder, False
        ):
            return [
                self._parse_optimizer_id(element)
                async for element in self.database_adaptor.get_sub_identifiers(
                    optimization_campaign_folder, [enums.RunDatabases.LIVE.value]
                )
            ]

    async def get_optimizer_run_ids(self) -> list:
        """
        :return: a list of every optimizer id in the current campaign
        """
        optimizer_runs_path = self._merge_parts(
            self.base_path,
            self.optimization_campaign_name,
            enums.RunDatabases.OPTIMIZER.value,
        )
        if await self.database_adaptor.identifier_exists(optimizer_runs_path, False):
            return [
                self._parse_optimizer_id(element)
                async for element in self.database_adaptor.get_sub_identifiers(
                    optimizer_runs_path, []
                )
            ]

    @staticmethod
    def _parse_optimizer_id(identifier) -> str:
        return identifier.split(constants.DB_SEPARATOR)[-1]

    def _get_base_path(self, from_global_history, backtesting_id, optimizer_id):
        if from_global_history and (backtesting_id is None and optimizer_id is None):
            # in live global history, use self.data_path as it's not related to a trading mode
            return self.data_path
        return self.base_path

    def _base_folder(
        self,
        ignore_backtesting_id=False,
        backtesting_id=None,
        ignore_optimizer_id=False,
        optimizer_id=None,
        from_global_history=False,
    ) -> str:
        path = self._get_base_path(from_global_history, backtesting_id, optimizer_id)
        backtesting_id = backtesting_id or self.backtesting_id
        optimizer_id = optimizer_id or self.optimizer_id
        # when in optimizer or backtesting: wrap it into the current campaign
        if backtesting_id is not None or optimizer_id is not None:
            if self.optimization_campaign_name is None:
                raise RuntimeError(
                    f"optimization_campaign_name is required in {RunDatabasesIdentifier} "
                    f"constructor while in a backtesting or optimizer context"
                )
            path = self._merge_parts(path, self.optimization_campaign_name)
        if optimizer_id is not None:
            if ignore_optimizer_id:
                path = self._merge_parts(path, enums.RunDatabases.OPTIMIZER.value)
            else:
                path = self._merge_parts(
                    path,
                    enums.RunDatabases.OPTIMIZER.value,
                    f"{enums.RunDatabases.OPTIMIZER.value}{constants.DB_SEPARATOR}{optimizer_id}",
                )
        if backtesting_id is not None:
            if optimizer_id is None:
                path = self._merge_parts(path, enums.RunDatabases.BACKTESTING.value)
            if ignore_backtesting_id:
                return path
            return self._merge_parts(
                path,
                f"{enums.RunDatabases.BACKTESTING.value}"
                f"{constants.DB_SEPARATOR}{backtesting_id}",
            )
        if optimizer_id is None:
            # live mode
            return self._merge_parts(path, enums.RunDatabases.LIVE.value)
        return path

    def _merge_parts(self, *parts):
        return (
            os.path.join(*parts)
            if self.database_adaptor.is_file_system_based()
            else constants.DB_SEPARATOR.join(*parts)
        )
