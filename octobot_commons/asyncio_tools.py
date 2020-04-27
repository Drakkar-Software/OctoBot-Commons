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

import asyncio

from octobot_commons.constants import DEFAULT_FUTURE_TIMEOUT
from octobot_commons.logging.logging_util import get_logger


LOGGER = get_logger("asyncio_tools")


def run_coroutine_in_asyncio_loop(coroutine, async_loop):
    """
    Run a coroutine in the specified asyncio loop
    :param coroutine: the coroutine to run
    :param async_loop: the asyncio loop
    :return: the execution result
    """
    current_task_before_start = asyncio.current_task(async_loop)
    future = asyncio.run_coroutine_threadsafe(coroutine, async_loop)
    try:
        return future.result(DEFAULT_FUTURE_TIMEOUT)
    except asyncio.TimeoutError as timeout_error:
        LOGGER.error(
            f"{coroutine} coroutine took too long to execute, cancelling the task. "
            f"(current task before starting this one: {current_task_before_start}, actual current "
            f"task before cancel: {asyncio.current_task(async_loop)})"
        )
        future.cancel()
        raise timeout_error
    except Exception as global_exception:
        LOGGER.exception(
            global_exception,
            True,
            f"{coroutine} coroutine raised an exception: {global_exception}",
        )
        raise global_exception
