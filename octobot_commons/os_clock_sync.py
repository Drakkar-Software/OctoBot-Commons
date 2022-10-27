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
import asyncio

import octobot_commons.constants as commons_constants
import octobot_commons.enums as commons_enums
import octobot_commons.singleton as singleton
import octobot_commons.logging as logging
import octobot_commons.async_job as async_job
import octobot_commons.os_util as os_util


class ClockSynchronizer(singleton.Singleton):
    DEFAULT_SYNC_REFRESH_INTERVAL = (
        commons_constants.CLOCK_REFRESH_HOURS_INTERVAL
        * commons_constants.HOURS_TO_SECONDS
    )

    def __init__(self):
        super().__init__()
        self.sync_job = None
        self.sync_interval = self.DEFAULT_SYNC_REFRESH_INTERVAL
        self.logger = logging.get_logger(self.__class__.__name__)

    def _get_sync_cmd(self):
        platform = os_util.get_os()
        if platform is commons_enums.PlatformsName.WINDOWS:
            # use 2x w32tm /resync as the 1st one often fails
            return "net stop w32time && net start w32time && w32tm /resync & w32tm /resync && w32tm /query /status"
        if platform is commons_enums.PlatformsName.LINUX:
            return "sudo service ntp stop && sudo ntpd -gq && sudo service ntp start"
        if platform is commons_enums.PlatformsName.MAC:
            raise NotImplementedError
        raise NotImplementedError

    async def _sync_clock(self):
        proc = await asyncio.create_subprocess_shell(
            self._get_sync_cmd(),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode == 0:
            self.logger.info("Successful os clock synchronization")
        else:
            self.logger.warning(
                f"Error: Time synchronization command exited with {proc.returncode}] "
                f'command: "{self._get_sync_cmd()}"'
            )
        if stdout:
            self.logger.debug(f"[stdout] {stdout}")
        if stderr:
            self.logger.debug(f"[stderr] {stderr}")

    async def start(self) -> bool:
        """
        Start the clock synchronization loop if possible on this system
        :return: True if the loop has been started
        """
        try:
            self._get_sync_cmd()
        except NotImplementedError:
            self.logger.debug(
                "Disable clock synchronizer: not implemented on this system."
            )
            return False
        if os_util.has_admin_rights():
            self.logger.debug("Starting clock synchronizer")
            self.sync_job = async_job.AsyncJob(
                self._sync_clock, execution_interval_delay=self.sync_interval
            )
            await self.sync_job.run()
            return True
        self.logger.debug(
            "Clock synch loop disabled: admin rights are required to synchronize the computer clock"
        )
        return False

    def stop(self):
        """
        Stop the synchronization loop
        """
        self.logger.debug("Stopping clock synchronizer")
        if self.sync_job is not None and not self.sync_job.should_stop:
            self.sync_job.stop()


async def start_clock_synchronizer():
    """
    Start the clock synchronization loop if possible on this system
    :return: True if the loop has been started
    """
    return await ClockSynchronizer.instance().start()


async def stop_clock_synchronizer():
    """
    Stop the synchronization loop
    """
    return ClockSynchronizer.instance().stop()
