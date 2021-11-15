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
import multiprocessing
import contextlib


_LOCKS = {}


def register_lock(name: str, lock: multiprocessing.RLock):
    _LOCKS[name] = lock


def unregister_lock(name: str) -> multiprocessing.RLock:
    return _LOCKS.pop(name)


@contextlib.contextmanager
def registered_lock(name: str, lock: multiprocessing.RLock):
    try:
        register_lock(name, lock)
        yield lock
    finally:
        unregister_lock(name)


def get_lock(name: str) -> multiprocessing.RLock:
    return _LOCKS[name]
