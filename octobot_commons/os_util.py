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


import sys
import os
import platform

import octobot_commons.constants as constants
import octobot_commons.enums as enums


def get_current_platform():
    """
    Return the current platform details
    Return examples
    For Windows :
    >>> 'Windows:10:AMD64'
    For Linux :
    >>> 'Linux:4.15.0-46-generic:x86_64'
    For Raspberry :
    >>> 'Linux:4.14.98-v7+:armv7l'
    :return: the current platform details
    """
    return (
        f"{platform.system()}{constants.PLATFORM_DATA_SEPARATOR}{platform.release()}{constants.PLATFORM_DATA_SEPARATOR}"
        f"{platform.machine()}"
    )


def get_octobot_type():
    """
    Return OctoBot running type from OctoBotTypes
    :return: the OctoBot running type
    """
    try:
        execution_arg = sys.argv[0]
        # sys.argv[0] is always the name of the python script called when using a command "python xyz.py"
        if execution_arg.endswith(".py"):
            if _is_on_docker():
                return enums.OctoBotTypes.DOCKER.value
            return enums.OctoBotTypes.PYTHON.value
        # sys.argv[0] is the name of the binary when using a binary version: ends with nothing or .exe"
        return enums.OctoBotTypes.BINARY.value
    except IndexError:
        return enums.OctoBotTypes.BINARY.value


def get_os():
    """
    Return the OS name
    :return: the OS name
    """
    return enums.PlatformsName(os.name)


def is_machine_64bit() -> bool:
    """
    Win: AMD64
    Debian-64: x86_64
    From https://stackoverflow.com/questions/2208828/detect-64bit-os-windows-in-python
    :return: True if the machine is 64bit
    """
    return platform.machine().endswith("64")


def is_arm_machine() -> bool:
    """
    Can be armv7l or aarch64 (raspberry, Android smartphone...)
    From https://raspberrypi.stackexchange.com/questions/5100/detect-that-a-python-program-is-running-on-the-pi
    :return: True if the machine is 64bit
    """
    return platform.machine() in ["armv7l", "aarch64"]


def _is_on_docker():
    """
    Check if the current platform is docker
    :return: True if OctoBot is running with docker
    """
    file_to_check = "/proc/self/cgroup"
    try:
        return os.path.exists("/.dockerenv") or (
            os.path.isfile(file_to_check)
            and any("docker" in line for line in open(file_to_check))
        )
    except FileNotFoundError:
        return False
