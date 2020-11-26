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

import concurrent.futures as futures


# pylint: disable=W0212
def stop_thread_pool_executor_non_gracefully(executor: futures.ThreadPoolExecutor):
    """
    From https://gist.github.com/clchiou/f2608cbe54403edb0b13
    Non graceful and non clean but only way to shutdown a ThreadPoolExecutor
    :param executor: the ThreadPoolExecutor to stop
    """
    executor.shutdown(False)
    executor._threads.clear()
    futures.thread._threads_queues.clear()
