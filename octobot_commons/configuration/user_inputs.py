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


class UserInput:
    def __init__(
        self,
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
        is_nested_config=None,
        nested_tentacle=None,
        parent_input_name=None,
        show_in_summary=True,
        show_in_optimizer=True,
        path=None,
        order=None
    ):
        self.name = name
        self.input_type = input_type
        self.value = value
        self.def_val = def_val
        self.tentacle_type = tentacle_type
        self.tentacle_name = tentacle_name
        self.min_val = min_val
        self.max_val = max_val
        self.options = options
        self.title = title
        self.item_title = item_title
        self.other_schema_values = other_schema_values
        self.editor_options = editor_options
        self.read_only = read_only
        self.is_nested_config = is_nested_config
        self.nested_tentacle = nested_tentacle
        self.parent_input_name = parent_input_name
        self.show_in_summary = show_in_summary
        self.show_in_optimizer = show_in_optimizer
        self.path = path
        self.order = order

    def to_dict(self):
        return {
            "name": self.name,
            "input_type": self.input_type if isinstance(self.input_type, str) else self.input_type.value,
            "value": self.value,
            "def_val": self.def_val,
            "min_val": self.min_val,
            "max_val": self.max_val,
            "options": self.options,
            "title": self.title,
            "item_title": self.item_title,
            "other_schema_values": self.other_schema_values,
            "editor_options": self.editor_options,
            "read_only": self.read_only,
            "tentacle_type": self.tentacle_type,
            "tentacle": self.tentacle_name,
            "nested_tentacle": self.nested_tentacle,
            "parent_input_name": self.parent_input_name,
            "is_nested_config": self.is_nested_config,
            "in_summary": self.show_in_summary,
            "in_optimizer": self.show_in_optimizer,
            "path": self.path,
            "order": self.order,
        }


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
    u_input = UserInput(
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
        u_input,
        run_data_writer,
        flush_if_necessary=flush_if_necessary,
        skip_flush=skip_flush,
    )
    return value


def sanitize_user_input_name(name):
    return name.replace(" ", "_")


async def save_user_input(
    u_input: UserInput,
    run_data_writer,
    flush_if_necessary=False,
    skip_flush=False,
):
    if not await run_data_writer.contains_row(
        enums.DBTables.INPUTS.value,
        {
            "name": u_input.name,
            "tentacle": u_input.tentacle_name,
            "nested_tentacle": u_input.nested_tentacle,
            "parent_input_name": u_input.parent_input_name,
            "is_nested_config": u_input.is_nested_config,
        },
    ):
        await run_data_writer.log(
            enums.DBTables.INPUTS.value,
            u_input.to_dict(),
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
