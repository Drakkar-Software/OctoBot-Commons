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
import json
import requests

from octobot_commons.logging.logging_util import get_logger
from octobot_commons.constants import EXTERNAL_RESOURCE_URL


def _handle_exception(exception, resource_key, catch_exception, default_response):
    if catch_exception:
        get_logger("ExternalResourcesManager") \
            .warning(f"Exception when calling get_external_resource for {resource_key} key: {exception}")
        return default_response
    else:
        raise exception


def get_external_resource(resource_key, catch_exception=False, default_response="") -> object:
    try:
        external_resources = json.loads(requests.get(EXTERNAL_RESOURCE_URL).text)
        return external_resources[resource_key]
    except Exception as e:
        return _handle_exception(e, resource_key, catch_exception, default_response)


async def async_get_external_resource(resource_key, aiohttp_session,
                                      catch_exception=False, default_response="") -> object:
    try:
        async with aiohttp_session.get(EXTERNAL_RESOURCE_URL) as resp:
            external_resources = json.loads(resp.text())
            return external_resources[resource_key]
    except Exception as e:
        return _handle_exception(e, resource_key, catch_exception, default_response)
