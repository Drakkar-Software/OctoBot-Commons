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
import os
import time

from mock import AsyncMock, patch
import pytest

from octobot_commons.async_job import AsyncJob
from octobot_commons.asyncio_tools import wait_asyncio_next_cycle

pytestmark = pytest.mark.asyncio


async def callback():
    pass


async def test_should_run():
    job = AsyncJob(callback)
    if not os.getenv('CYTHON_IGNORE'):
        assert job._should_run()
        job.last_execution_time = time.time()
        assert job._should_run()
    job.stop()


async def test_should_run_with_delays():
    job = AsyncJob(callback, min_execution_delay=1)
    if not os.getenv('CYTHON_IGNORE'):
        assert job._should_run()
        job.last_execution_time = time.time()
        assert not job._should_run()
        await asyncio.sleep(1)
        assert job._should_run()
    job.stop()


async def test_should_run_with_dependencies():
    job2 = AsyncJob(callback)
    job3 = AsyncJob(callback)
    job = AsyncJob(callback, job_dependencies=[job2, job3])
    if not os.getenv('CYTHON_IGNORE'):
        assert job._should_run()
        job2.is_running = True
        assert not job._should_run()
        job2.is_running = True
        job3.is_running = True
        assert not job._should_run()
        job2.is_running = False
        assert not job._should_run()
        job3.is_running = False
        assert job._should_run()
    job.stop()


async def test_clear():
    AsyncJob(callback).clear()


async def test_run():
    job = AsyncJob(callback, execution_interval_delay=5, min_execution_delay=2)
    if not os.getenv('CYTHON_IGNORE'):
        with patch.object(job, 'callback', new=AsyncMock()) as mocked_test_job_callback:
            await wait_asyncio_next_cycle()
            mocked_test_job_callback.assert_not_called()
            assert not job.is_scheduled
            await job.run()
            await wait_asyncio_next_cycle()
            mocked_test_job_callback.assert_called_once()
            assert job.is_scheduled

            # delay has not been waited
            await job.run()
            await wait_asyncio_next_cycle()
            mocked_test_job_callback.assert_called_once()
            assert job.is_scheduled

            await asyncio.sleep(3)
            mocked_test_job_callback.assert_called_once()

            await asyncio.sleep(3)
            assert mocked_test_job_callback.call_count == 2

            await job.run(force=True)
            assert mocked_test_job_callback.call_count == 3

    job.stop()
