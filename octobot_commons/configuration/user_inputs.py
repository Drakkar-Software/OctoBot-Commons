# pylint: disable=W1203
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
import octobot_commons.enums as enums


async def user_input(
    name,
    input_type,
    def_val,
    tentacle_type,
    tentacle_name,
    saved_config,
    run_data_writer,
    min_val=None,
    max_val=None,
    options=None,
    title=None,
    item_title=None,
    other_schema_values=None,
    editor_options=None,
    read_only=False,
    is_nested_config=None,
    nested_tentacle=None,
    parent_input_name=None,
    show_in_summary=True,
    show_in_optimizer=True,
    path=None,
    order=None,
    flush_if_necessary=False,
    skip_flush=False,
):
    """
    Set and return a user input value.
    Types are: int, float, boolean, options, multiple-options, text, object
    Note: parent_input_name to be set to add sub elements to a configuration.
    :return: the saved_config value if any, def_val otherwise
    """
    try:
        value = saved_config[name.replace(" ", "_")]
    except KeyError:
        saved_config[name.replace(" ", "_")] = def_val
        value = def_val
    formatted_input = format_user_input(
        name,
        input_type,
        value,
        def_val,
        tentacle_type,
        tentacle_name,
        min_val=min_val,
        max_val=max_val,
        options=options,
        title=title,
        item_title=item_title,
        other_schema_values=other_schema_values,
        editor_options=editor_options,
        read_only=read_only,
        is_nested_config=is_nested_config,
        nested_tentacle=nested_tentacle,
        parent_input_name=parent_input_name,
        show_in_summary=show_in_summary,
        show_in_optimizer=show_in_optimizer,
        path=path,
        order=order,
    )
    await save_user_input(
        formatted_input,
        run_data_writer,
        flush_if_necessary=flush_if_necessary,
        skip_flush=skip_flush,
    )
    return value


def sanitize_user_input_name(name):
    return name.replace(" ", "_")


def format_user_input(
    name,
    input_type,
    value,
    def_val,
    tentacle_type,
    tentacle_name,
    min_val=None,
    max_val=None,
    options=None,
    title=None,
    item_title=None,
    other_schema_values=None,
    editor_options=None,
    read_only=False,
    is_nested_config=False,
    parent_input_name=None,
    nested_tentacle=None,
    show_in_summary=True,
    show_in_optimizer=True,
    path=None,
    order=None,
):
    return {
        "name": name,
        "input_type": input_type if isinstance(input_type, str) else input_type.value,
        "value": value,
        "def_val": def_val,
        "min_val": min_val,
        "max_val": max_val,
        "options": options,
        "title": title,
        "item_title": item_title,
        "other_schema_values": other_schema_values,
        "editor_options": editor_options,
        "read_only": read_only,
        "tentacle_type": tentacle_type,
        "tentacle": tentacle_name,
        "nested_tentacle": nested_tentacle,
        "parent_input_name": parent_input_name,
        "is_nested_config": is_nested_config,
        "in_summary": show_in_summary,
        "in_optimizer": show_in_optimizer,
        "path": path,
        "order": order,
    }


async def save_user_input(
    formatted_input,
    run_data_writer,
    flush_if_necessary=False,
    skip_flush=False,
):
    if not await run_data_writer.contains_row(
        enums.DBTables.INPUTS.value,
        {
            "name": formatted_input["name"],
            "tentacle": formatted_input["tentacle"],
            "nested_tentacle": formatted_input["nested_tentacle"],
            "parent_input_name": formatted_input["parent_input_name"],
            "is_nested_config": formatted_input["is_nested_config"],
        },
    ):
        await run_data_writer.log(
            enums.DBTables.INPUTS.value,
            formatted_input,
        )
        if not skip_flush and (
            flush_if_necessary or run_data_writer.are_data_initialized
        ):
            # in some cases, user inputs might be setup after the 1st trading mode cycle: flush
            # writer in live mode to ensure writing
            await run_data_writer.flush()


def get_user_input_tentacle_type(tentacle) -> str:
    return (
        enums.UserInputTentacleTypes.TRADING_MODE.value
        if hasattr(tentacle, "trading_config")
        else enums.UserInputTentacleTypes.EVALUATOR.value
    )


async def get_user_inputs(reader, tentacle_name=None):
    all_inputs = await reader.all(enums.DBTables.INPUTS.value)
    if tentacle_name is None:
        return all_inputs
    return [
        selected_input
        for selected_input in all_inputs
        if selected_input["tentacle"] == tentacle_name
    ]


async def clear_user_inputs(writer, tentacle_name=None):
    if tentacle_name is None:
        await writer.delete_all(enums.DBTables.INPUTS.value)
    else:
        query = {"tentacle": tentacle_name}
        await writer.delete(enums.DBTables.INPUTS.value, query)
