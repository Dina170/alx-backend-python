#!/usr/bin/env python3
"""Augment the code with the correct duck-typed annotations"""
from typing import Union, Sequence, Any


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Returns first element in list if it exists"""
    if lst:
        return lst[0]
    else:
        return None
