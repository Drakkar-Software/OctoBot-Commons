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
import pytest

from octobot_commons.asyncio_tools import ErrorContainer

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


async def test_without_error_container():
    # will not propagate exception
    asyncio.get_event_loop().call_soon(_exception_raiser)


async def test_with_error_container():
    error_container = ErrorContainer()
    error_container.print_received_exceptions = False
    asyncio.get_event_loop().set_exception_handler(error_container.exception_handler)
    # will propagate exception
    asyncio.get_event_loop().call_soon(_exception_raiser)
    with pytest.raises(AssertionError):
        # ensure exception is caught
        await asyncio.create_task(error_container.check())


async def test_with_error_container_2_exceptions():
    error_container = ErrorContainer()
    error_container.print_received_exceptions = False
    asyncio.get_event_loop().set_exception_handler(error_container.exception_handler)
    # will propagate exception
    asyncio.get_event_loop().call_soon(_exception_raiser)
    asyncio.get_event_loop().call_soon(_exception_raiser)
    with pytest.raises(AssertionError):
        # ensure exception is caught
        await asyncio.create_task(error_container.check())


def _exception_raiser():
    raise RuntimeError("error")
