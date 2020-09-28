# cython: language_level=3
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

cdef class AsyncJob:
    cdef object logger                      # logging.Logger
    cdef object callback                    # Callable
    cdef object job_task                    # Asyncio.Task
    cdef object job_periodic_task           # Asyncio.Task
    cdef public object idle_task_event      # Asyncio.Event

    cdef bint is_started
    cdef bint should_stop
    cdef bint is_periodic
    cdef bint enable_multiple_runs
    cdef int simultaneous_calls
    cdef int successive_failures
    cdef int max_successive_failures

    cdef double last_execution_time
    cdef double execution_interval_delay
    cdef double min_execution_delay

    cdef list job_dependencies

    cpdef void add_job_dependency(self, AsyncJob job)
    cpdef bint is_job_idle(self)
    cpdef void clear(self)
    cpdef void stop(self)

    cdef void _handle_run_exception(self, object exception, bint error_on_single_failure)
    cdef bint _should_run_job(self, bint force=*, ignore_dependencies=*)
    cdef bint _has_enough_time_elapsed(self)
    cdef bint _are_job_dependencies_idle(self)
