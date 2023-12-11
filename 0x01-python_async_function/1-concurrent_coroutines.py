#!/usr/bin/env python3
"""Defines an async routine called wait_n that takes in
   2 int arguments (in this order): n and max_delay.
   spawn wait_random n times with the specified max_delay
"""
import asyncio
import random
from typing import List


async def wait_n(n: int, max_delay: int = 10) -> List[float]:
    """Spawn wait_random n times with the specified max_delay"""
    tasks = [wait_random(max_delay) for _ in range(n)]
    delays = await asyncio.gather(*tasks)
    return sorted(delays)
