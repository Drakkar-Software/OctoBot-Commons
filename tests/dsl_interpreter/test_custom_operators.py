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
import typing
import pytest
import ast

import octobot_commons.dsl_interpreter as dsl_interpreter
import octobot_commons.enums as commons_enums
import octobot_commons.constants as commons_constants
import octobot_commons.errors as commons_errors


async def get_x_value_async() -> int:
    return 666


class SumPlusXOperatorWithoutInit(dsl_interpreter.NaryOperator):
    def __init__(self, *parameters: dsl_interpreter.OperatorParameterType, **kwargs: typing.Any):
        super().__init__(*parameters, **kwargs)
        self.x_value = 42
    
    @staticmethod
    def get_name() -> str:
        return "plus_42"

    def compute(self) -> dsl_interpreter.ComputedOperatorParameterType:
        computed_parameters = self.get_computed_parameters()
        return sum(computed_parameters) + self.x_value


class SumPlusXOperatorWithPreCompute(dsl_interpreter.NaryOperator):
    def __init__(self, *parameters: dsl_interpreter.OperatorParameterType, **kwargs: typing.Any):
        super().__init__(*parameters, **kwargs)
        self.x_value = 42
    
    @staticmethod
    def get_name() -> str:
        return "plus_x"

    @staticmethod
    def get_parameters() -> list[dsl_interpreter.OperatorParameter]:
        return [
            dsl_interpreter.OperatorParameter(name="data", description="the data to compute the sum of", required=True, type=int),
            dsl_interpreter.OperatorParameter(name="data2", description="the data to compute the sum of", required=False, type=int),
        ]

    async def pre_compute(self) -> None:
        await super().pre_compute()
        self.x_value = await get_x_value_async()

    def compute(self) -> dsl_interpreter.ComputedOperatorParameterType:
        computed_parameters = self.get_computed_parameters()
        return sum(computed_parameters) + self.x_value


class TimeFrameToSecondsOperator(dsl_interpreter.CallOperator):
    MIN_PARAMS = 1
    MAX_PARAMS = 1

    def __init__(self, *params, **kwargs: typing.Any):
        super().__init__(*params, **kwargs)

    @staticmethod
    def get_name() -> str:
        return "time_frame_to_seconds"

    def compute(self) -> dsl_interpreter.ComputedOperatorParameterType:
        computed_parameters = self.get_computed_parameters()
        return commons_enums.TimeFramesMinutes[commons_enums.TimeFrames(computed_parameters[0])] * commons_constants.MINUTE_TO_SECONDS


class AddOperator(dsl_interpreter.BinaryOperator):
    @staticmethod
    def get_name() -> str:
        return ast.Add.__name__

    def compute(self) -> dsl_interpreter.ComputedOperatorParameterType:
        left, right = self.get_computed_left_and_right_parameters()
        return left + right

class Add2Operator(dsl_interpreter.CallOperator):
    @staticmethod
    def get_name() -> str:
        return "add2"

    @staticmethod
    def get_parameters() -> list[dsl_interpreter.OperatorParameter]:
        return [
            dsl_interpreter.OperatorParameter(name="left", description="the left operand", required=True, type=int),
            dsl_interpreter.OperatorParameter(name="right", description="the right operand", required=True, type=int),
        ]

    def compute(self) -> dsl_interpreter.ComputedOperatorParameterType:
        left, right = self.get_computed_left_and_right_parameters()
        return left + right


@pytest.fixture
def interpreter():
    return dsl_interpreter.Interpreter(
        dsl_interpreter.get_all_operators() + [
            SumPlusXOperatorWithoutInit, SumPlusXOperatorWithPreCompute, TimeFrameToSecondsOperator, AddOperator, Add2Operator
        ]
    )


@pytest.mark.asyncio
async def test_interpreter_basic_operations(interpreter):
    assert await interpreter.interprete("plus_42()") == 42
    assert await interpreter.interprete("plus_42(6)") == 48
    assert await interpreter.interprete("plus_42(1, 2, 3)") == 48
    assert await interpreter.interprete("plus_42(1, 1 + 1, 1.5 +1.5)") == 48
    assert await interpreter.interprete("plus_x(1, 1)") == 668
    assert await interpreter.interprete("10 + (plus_x(1, 1) + plus_x(1, 1))") == 10 + (668 + 668) == 1346
    assert await interpreter.interprete("time_frame_to_seconds('1m')") == 60
    assert await interpreter.interprete("time_frame_to_seconds('1d')") == 86400
    assert await interpreter.interprete("time_frame_to_seconds('1'+'h')") == 3600


@pytest.mark.asyncio
async def test_interpreter_invalid_parameters(interpreter):
    with pytest.raises(commons_errors.InvalidParametersError, match="plus_x requires at least 1 parameter\(s\): 1: data"):
        interpreter.prepare("plus_x()")
    with pytest.raises(commons_errors.InvalidParametersError, match="plus_x requires at least 1 parameter\(s\): 1: data"):
        await interpreter.interprete("plus_x()")
    with pytest.raises(commons_errors.InvalidParametersError, match="add2 requires at least 2 parameter\(s\): 1: left"):
        interpreter.prepare("add2()")
    with pytest.raises(commons_errors.InvalidParametersError, match="add2 requires at least 2 parameter\(s\): 1: left"):
        await interpreter.interprete("add2()")
    with pytest.raises(commons_errors.InvalidParametersError, match="add2 supports up to 2 parameters:"):
        interpreter.prepare("add2(1, 2, 3)")
    with pytest.raises(commons_errors.InvalidParametersError, match="add2 supports up to 2 parameters:"):
        await interpreter.interprete("add2(1, 2, 3)")
    with pytest.raises(commons_errors.InvalidParametersError, match="time_frame_to_seconds requires at least 1 parameter\(s\)"):
        interpreter.prepare("time_frame_to_seconds()")
    with pytest.raises(commons_errors.InvalidParametersError, match="time_frame_to_seconds requires at least 1 parameter\(s\)"):
        await interpreter.interprete("time_frame_to_seconds()")
    with pytest.raises(commons_errors.InvalidParametersError, match="time_frame_to_seconds supports up to 1 parameters"):
        interpreter.prepare("time_frame_to_seconds(1, 2, 3)")
    with pytest.raises(commons_errors.InvalidParametersError, match="time_frame_to_seconds supports up to 1 parameters"):
        await interpreter.interprete("time_frame_to_seconds(1, 2, 3)")
