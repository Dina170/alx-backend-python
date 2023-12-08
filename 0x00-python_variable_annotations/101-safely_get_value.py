#!/usr/bin/env python3
"""Add type annotations to the function using TypeVar"""
from typing import Union, Any, Mapping, TypeVar

T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[T, None] = None) -> Union[Any, T]:
    """Returns the value in dict of a given key"""
    if key in dct:
        return dct[key]
    else:
        return default
