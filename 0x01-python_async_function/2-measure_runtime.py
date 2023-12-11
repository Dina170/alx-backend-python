#!/usr/bin/env python3
"""Defines a measure_time function with integers n and max_delay
   as arguments that measures the total execution time for
   wait_n(n, max_delay), and returns total_time / n
"""
import asyncio
import time
wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int = 10) -> float:
    """Measures the total execution time for wait_n(n, max_delay),
       returns total_time / n
    """
    start_time = time.time()
    asyncio.run(wait_n(n, max_delay))
    return (time.time() - start_time) / n
