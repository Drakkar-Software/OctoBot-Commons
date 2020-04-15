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

import math
import numpy as np

from octobot_commons.constants import START_PENDING_EVAL_NOTE

UNSET_EVAL_TYPE = "unset_eval_type_param"


def check_valid_eval_note(eval_note, eval_type=UNSET_EVAL_TYPE, expected_eval_type=None):
    """
    Will also test evaluation type if if eval_type is provided.
    :param eval_note:
    :param eval_type:
    :param expected_eval_type: Default expected_eval_type is EVALUATOR_EVAL_DEFAULT_TYPE
    :return:
    """
    if eval_type != UNSET_EVAL_TYPE and (eval_type != expected_eval_type or expected_eval_type is None):
        return False
    return eval_note is not None \
        and eval_note is not START_PENDING_EVAL_NOTE \
        and not math.isnan(eval_note) \
        and not np.isnan(eval_note)
