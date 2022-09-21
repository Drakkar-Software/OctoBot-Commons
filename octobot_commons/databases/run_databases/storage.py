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
import octobot_commons.databases.run_databases.run_databases_provider as run_databases_provider


async def init_bot_storage(bot_id, run_database_identifier):
    if not run_databases_provider.RunDatabasesProvider.instance().has_bot_id(bot_id):
        # only one run database per bot id
        await run_databases_provider.RunDatabasesProvider.instance().add_bot_id(bot_id, run_database_identifier)


def get_run_db(bot_id):
    return run_databases_provider.RunDatabasesProvider.instance().get_run_db(bot_id)


def get_symbol_db(bot_id, exchange, symbol):
    return run_databases_provider.RunDatabasesProvider.instance().get_symbol_db(bot_id, exchange, symbol)


async def close_bot_storage(bot_id):
    if run_databases_provider.RunDatabasesProvider.instance().has_bot_id(bot_id):
        await run_databases_provider.RunDatabasesProvider.instance().close(bot_id)

