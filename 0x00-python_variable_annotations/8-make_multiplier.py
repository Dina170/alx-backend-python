#!/usr/bin/env python3
"""Defines a type-annotated function make_multiplier that
   takes: a float multiplier as argument and
   returns: a function that multiplies a float by multiplier
"""


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Returns a function"""
    return lambda num: num * multiplier
