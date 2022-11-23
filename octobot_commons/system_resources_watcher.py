# pylint: disable=W0703
#  Drakkar-Software OctoBot
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
import threading

import octobot_commons.constants as commons_constants
import octobot_commons.singleton as singleton
import octobot_commons.logging as logging
import octobot_commons.async_job as async_job
import octobot_commons.os_util as os_util


class SystemResourcesWatcher(singleton.Singleton):
    DEFAULT_WATCHER_INTERVAL = (
        commons_constants.RESOURCES_WATCHER_MINUTES_INTERVAL
        * commons_constants.MINUTE_TO_SECONDS
    )
    CPU_WATCHING_SECONDS = 2

    def __init__(self):
        super().__init__()
        self.watcher_job = None
        self.watcher_interval = self.DEFAULT_WATCHER_INTERVAL
        self.logger = logging.get_logger(self.__class__.__name__)

    def _exec_log_used_resources(self):
        try:
            # warning: blocking to monitor CPU usage, to be used in a thread
            cpu, percent_ram, ram, process_ram = os_util.get_cpu_and_ram_usage(
                self.CPU_WATCHING_SECONDS
            )
            self.logger.debug(
                f"Used system resources: {cpu}% CPU, {round(ram, 3)} GB in RAM ({percent_ram}% of total "
                f"including {round(process_ram, 3)} GB from this process). "
            )
        except Exception as err:
            self.logger.exception(err, False)
            self.logger.debug(f"Error when checking system resources: {err}")

    async def _log_used_resources(self):
        threading.Thread(
            target=self._exec_log_used_resources,
            daemon=True,
            name=f"{self.__class__.__name__}-_exec_log_used_resources",
        ).start()

    async def start(self):
        """
        Synch the clock and start the clock synchronization loop if possible on this system
        """
        self.logger.debug("Starting system resources watcher")
        self.watcher_job = async_job.AsyncJob(
            self._log_used_resources,
            execution_interval_delay=self.watcher_interval,
        )
        await self.watcher_job.run()

    def stop(self):
        """
        Stop the synchronization loop
        """
        self.logger.debug("Stopping system resources watcher")
        if self.watcher_job is not None and not self.watcher_job.is_stopped():
            self.watcher_job.stop()


async def start_system_resources_watcher():
    """
    Start the resources watcher loop
    """
    await SystemResourcesWatcher.instance().start()


async def stop_system_resources_watcher():
    """
    Stop the watcher loop
    """
    return SystemResourcesWatcher.instance().stop()
