#!/usr/bin/env python3
"""Defines a function identical to wait_n called task_wait_n.
   except task_wait_random is being called.
"""
import asyncio
import random
from typing import List
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int = 10) -> List[float]:
    """Spawn task_wait_random n times with the specified max_delay"""
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    delays = await asyncio.gather(*tasks)
    return sorted(delays)
