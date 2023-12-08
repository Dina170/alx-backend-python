#!/usr/bin/env python3
"""Adds annotations the below function’s parameters and
   returns values with the appropriate types
"""


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Returns a list of tuples and each tuple consists of
       the element and its length"""
    return [(i, len(i)) for i in lst]
