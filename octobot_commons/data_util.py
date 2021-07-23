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

import numpy as np


def normalize_data(data):
    """
    Normalize the specified data
    :param data: the data to normalize
    :return: normalized data
    """
    if data.size > 1:
        return (data - np.mean(data)) / (data.max() - data.min())
    return data

def HL2(high, low):
    """
    Return a list of HL2 value (high + low ) / 2
    :param high: list of high
    :param low: list of low
    :return: list of HL2
    """
    return np.array(list(map((lambda high, low: mean([high, low])), high, low)))

def HLC3(high, low, close):
    """
    Return a list of HLC3 values (high + low + close) / 3
    :param high: list of high
    :param low: list of low
    :param close: list of close
    :return: list of HLC3
    """
    return np.array(list(map((lambda high, low, close: 
                        mean([high, low, close])), 
                        high, low, close)))

def OHLC4(open, high, low, close):
    """
    Return a list of OHLC4 value (open + high + low + close) / 4
    :param open: list of open
    :param high: list of high
    :param low: list of low
    :param close: close of candle
    :return: list of OHLC4
    """
    return np.array(list((map((lambda open, high, low, close: 
                        mean([open, high, low, close])), 
                        open, high, low, close))))

def HeikinAshi(open, high, low, close):
    """
    Return HeikinAshi array of the given candles
    :param open: list of open
    :param high: list of high
    :param low: list of low
    :param close: close of candle
    :return: HAopen, HAhigh, HAlow, HAclose
    """
    haOpen, haHigh, haLow, haClose = [np.array([]) for i in range(4)]
    for i, (open_value, high_value, low_value, close_value) \
                        in enumerate(zip(open, high, low, close)):
        if i == 0:
            haOpen = np.append(haOpen, open_value)
            haHigh = np.append(haHigh, high_value)
            haLow = np.append(haLow, low_value)
            haClose = np.append(haClose, close_value)
            continue
        haOpen = np.append(haOpen, mean([open[i-1], close[i-1]]))
        haHigh = np.append(haHigh, high_value)
        haLow = np.append(haLow, low_value)
        haClose = np.append(haClose, mean([open_value, high_value, low_value, close_value]))
    return haOpen, haHigh, haLow, haClose

def drop_nan(data):
    """
    Drop nan of a numpy array
    :param data: the numpy array
    :return: the numpy array without nan value
    """
    return data[~np.isnan(data)]


def mean(number_list):
    """
    Return the list average
    :param number_list: the list to use
    :return: the list average
    """
    return sum(number_list) / len(number_list) if number_list else 0


def shift_value_array(array, shift_count=-1, fill_value=np.nan, dtype=np.float64):
    """
    Shift a numpy array
    :param array: the numpy array
    :param shift_count: the shift direction (- / +) and counter
    :param fill_value: the new value of the shifted indexes
    :param dtype: the type of the numpy array (and also the :fill_value:)
    :return: the shifted array
    """
    new_array = np.empty_like(array, dtype=dtype)
    if shift_count > 0:
        new_array[:shift_count] = fill_value
        new_array[shift_count:] = array[:-shift_count]
    elif shift_count < 0:
        new_array[shift_count:] = fill_value
        new_array[:shift_count] = array[-shift_count:]
    else:
        new_array[:] = array
    return new_array
