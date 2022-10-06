# pylint: disable=W0703
#  Drakkar-Software OctoBot-Trading
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
import time
import pathlib

import octobot_commons.enums as enums
import octobot_commons.constants as constants
import octobot_commons.logging as logging
import octobot_commons.errors as errors
import octobot_commons.databases.implementations as databases_implementations
import octobot_commons.databases.run_databases.run_databases_identifier as run_databases_identifier


class RunDatabasesPruner:
    def __init__(self, databases_root_identifier, max_databases_size, database_adaptor):
        self.logger = logging.get_logger(self.__class__.__name__)
        self.databases_root_identifier = databases_root_identifier
        self.max_databases_size = max_databases_size
        self.database_adaptor = database_adaptor
        self.all_db_data = []

        separator = (
            os.path.sep
            if self.database_adaptor.is_file_system_based
            else constants.DB_SEPARATOR
        )
        self.backtesting_run_path_identifier = {
            f"{separator}{enums.RunDatabases.BACKTESTING.value}{separator}",
            f"{separator}{enums.RunDatabases.OPTIMIZER.value}{separator}",
        }
        self._run_db = f"{enums.RunDatabases.RUN_DATA_DB.value}{self.database_adaptor.get_db_file_ext()}"

    async def explore(self):
        """
        Explore self.databases_root_identifier to gather storage
        statistics to be used in prune_oldest_run_databases
        """
        t_start = time.time()
        if self.database_adaptor.is_file_system_based():
            self._explore_file_system_databases()
        else:
            raise errors.UnsupportedError(
                "Only file system based databases are supported for now"
            )
        total_time = round(time.time() - t_start, 2)
        if total_time > 1:
            self.logger.debug(
                f"Explored run databases for pruning in {total_time} seconds."
            )

    async def prune_oldest_run_databases(self):
        """
        Delete the necessary backtesting run data for the total backtesting storage
        size to be <= self.max_databases_size. Deletes oldest run data first
        """
        self.all_db_data = sorted(
            self.all_db_data, key=lambda data: data.last_modified_time
        )
        removed_databases = []
        while self._get_total_db_size() > self.max_databases_size:
            if self._prune_database(self.all_db_data[0]):
                removed_databases.append(self.all_db_data[0])
                self.all_db_data = self.all_db_data[1:]
        if removed_databases:
            await self._update_backtesting_metadata_files(removed_databases)
            self._log_summary(removed_databases)

    async def _update_backtesting_metadata_files(self, removed_databases):
        runs_folders = {
            pathlib.Path(removed_database.identifier).parent
            for removed_database in removed_databases
        }
        for runs_folder in runs_folders:
            await self._update_metadata(runs_folder)

    async def _update_metadata(self, runs_identifier):
        run_db_identifier = self._get_run_db_identifier(runs_identifier)
        if runs_identifier is not None:
            remaining_run_ids = {
                int(identifier)
                for identifier in await run_db_identifier.get_backtesting_run_ids()
            }
            async with databases_implementations.DBWriterReader.database(
                run_db_identifier.get_backtesting_metadata_identifier()
            ) as reader_writer:
                found_runs = await reader_writer.all(enums.DBTables.METADATA.value)
                metadata = [
                    run
                    for run in found_runs
                    if run[enums.BacktestingMetadata.ID.value] in remaining_run_ids
                ]
                await reader_writer.replace_all(enums.DBTables.METADATA.value, metadata)

    def _get_run_db_identifier(self, runs_identifier):
        split_path = pathlib.Path(runs_identifier).parts
        try:
            if split_path[-2] == enums.RunDatabases.OPTIMIZER.value:
                # in optimizer
                # ex: [..., 'DipAnalyserTradingMode', 'Dip Analyser strat designer test', 'optimizer', 'optimizer_1']
                optimizer_id = (
                    run_databases_identifier.RunDatabasesIdentifier.parse_optimizer_id(
                        split_path[-1]
                    )
                )
                campaign_name = split_path[-3]
                trading_mode = split_path[-4]
                return run_databases_identifier.RunDatabasesIdentifier(
                    trading_mode,
                    optimization_campaign_name=campaign_name,
                    backtesting_id=0,
                    optimizer_id=optimizer_id,
                )
            # in backtesting
            # ex: [..., 'DipAnalyserTradingMode', 'Dip Analyser strat designer test', 'backtesting']
            campaign_name = split_path[-2]
            trading_mode = split_path[-3]
            return run_databases_identifier.RunDatabasesIdentifier(
                trading_mode,
                optimization_campaign_name=campaign_name,
                backtesting_id=0,
            )
        except IndexError as err:
            self.logger.exception(
                err, True, f"Unhandled backtesting data path format: {runs_identifier}"
            )
            return None

    def _log_summary(self, removed_databases):
        first_removed = removed_databases[0].get_human_readable_last_modified_time()
        last_removed = removed_databases[-1].get_human_readable_last_modified_time()
        self.logger.debug(
            f"Deleted the {len(removed_databases)} oldest run data from the {first_removed} to the {last_removed}"
        )

    def _explore_file_system_databases(self):
        self.all_db_data = [
            DBData(
                directory, [DBPartData(f, True) for f in self._get_all_files(directory)]
            )
            for directory in self._get_file_system_runs(self.databases_root_identifier)
        ]

    def _get_file_system_runs(self, root):
        # use os.scandir as it is much faster than os.walk
        for entry in os.scandir(root):
            if self._is_run_top_level_folder(entry):
                yield entry
            elif entry.is_dir():
                yield from self._get_file_system_runs(entry)

    def _get_all_files(self, root):
        for entry in os.scandir(root):
            if entry.is_file():
                yield entry
            elif entry.is_dir():
                yield from self._get_all_files(entry)

    def _prune_database(self, db_data):
        if self.database_adaptor.is_file_system_based():
            return self._prune_file_system_database(db_data)
        raise errors.UnsupportedError(
            "Only file system based databases are supported for now"
        )

    def _prune_file_system_database(self, db_data):
        try:
            shutil.rmtree(db_data.identifier)
            return True
        except Exception as err:
            self.logger.exception(err, True, f"Error when deleting run database: {err}")
            return False

    def _get_total_db_size(self):
        return sum(db_data.size for db_data in self.all_db_data)

    def _is_run_top_level_folder(self, dir_entry):
        return os.path.isfile(os.path.join(dir_entry, self._run_db)) and any(
            identifier in dir_entry.path
            for identifier in self.backtesting_run_path_identifier
        )

    def _get_run_top_level_folder(self, parent_path, path):
        folder_path = os.path.join(parent_path, path)
        if os.path.isfile(os.path.join(folder_path, self._run_db)):
            return folder_path
        return None


class DBData:
    def __init__(self, identifier, parts):
        self.identifier = identifier
        self.parts = parts
        self.size = sum(part.size for part in self.parts)
        self.last_modified_time = max(part.last_modified_time for part in self.parts)

    def get_human_readable_last_modified_time(self):
        """
        :return: self.last_modified_time in a human-readable format
        """
        return time.strftime(
            "%Y-%m-%d %H:%M:%S", time.strptime(time.ctime(self.last_modified_time))
        )


class DBPartData:
    def __init__(self, identifier, is_file_system_based):
        self.identifier = identifier
        if is_file_system_based:
            self.size = os.path.getsize(self.identifier)
            self.last_modified_time = os.path.getmtime(self.identifier)
