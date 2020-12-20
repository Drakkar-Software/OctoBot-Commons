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
import json
import jsonschema


def validate(config, schema_file) -> None:
    """
    Validate a config file, raise upon validation error
    :param config: the config
    :param schema_file: the config schema
    :return: None
    """
    with open(schema_file) as json_schema:
        loaded_schema = json.load(json_schema)
    jsonschema.validate(instance=config, schema=loaded_schema)
