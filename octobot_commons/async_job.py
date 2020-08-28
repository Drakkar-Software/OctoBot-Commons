# pylint: disable=W0703,R0902,R0913
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

import time

from octobot_commons.logging.logging_util import get_logger


class AsyncJob:
    """
    Async job management
    """

    NO_DELAY = -1

    def __init__(
        self,
        callback,
        execution_interval_delay=NO_DELAY,
        min_execution_delay=NO_DELAY,
        job_dependencies=None,
    ):
        self.logger = get_logger(self.__class__.__name__)
        self.is_running = False
        self.is_scheduled = False
        self.last_execution_time = 0
        self.execution_interval_delay = execution_interval_delay
        self.min_execution_delay = min_execution_delay
        self.callback = callback
        self.job_dependencies = job_dependencies if job_dependencies else []
        self.job_task = None

    async def run(self, force=False):
        """
        Run the job if possible
        Reschedule the jab in the end
        :param force: When True, force the execution of the job
        """
        if not self.is_running and (self._should_run() or force):
            await self._run()
        if not self.is_scheduled:
            await self._reschedule()

    def is_job_running(self):
        """
        :return: publicly is_running attribute value
        """
        return self.is_running

    async def _run(self):
        """
        Execute the job callback
        Reset the last_execution_time
        """
        self.is_running = True
        try:
            await self.callback()
        except Exception as exception:
            self.logger.error(f"Failed to run job action : {exception}")
        finally:
            self.last_execution_time = time.time()
            self.is_running = False
            self.is_scheduled = False

    async def _reschedule(self):
        """
        Reschedule the job according to execution_interval_delay
        if execution_interval_delay == AsyncJob.NO_DELAY, tries to execute without delay (in the next async loop)
        else schedule the execution at now + execution_interval_delay
        """
        if self.execution_interval_delay != AsyncJob.NO_DELAY:
            self.job_task = asyncio.create_task(self._postpone_run())
        else:
            await self.run()
        self.is_scheduled = True

    async def _postpone_run(self):
        """
        Postpone the run() call at execution_interval_delay
        """
        await asyncio.sleep(self.execution_interval_delay)
        await self.run()

    def _should_run(self):
        """
        Return True if the job is not already running, if dependent jobs are also not running
        and if min_execution_delay < last_execution_time
        """
        return not any([job.is_running for job in self.job_dependencies]) and (
            time.time() - self.min_execution_delay > self.last_execution_time
            or self.min_execution_delay == AsyncJob.NO_DELAY
            or self.last_execution_time == 0
        )

    def stop(self):
        """
        Stop the job by cancelling the execution task
        """
        if self.job_task is not None:
            self.job_task.cancel()

    def clear(self):
        """
        Clear job object references and stop it
        """
        self.job_dependencies = None
        self.stop()
