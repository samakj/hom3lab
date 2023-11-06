from datetime import datetime
from typing import Union

type FilterTypes = Union[int, str, datetime, bool]
type FilterTypeLists = Union[list[int], list[str], list[datetime], list[bool]]


def to_filter[T: (int, str, datetime, bool)](value: T) -> str:
    if isinstance(value, int):
        return f"{value}"
    if isinstance(value, str):
        return f"'{value}'"
    if isinstance(value, datetime):
        return f"'{value.isoformat()}'"
    if isinstance(value, bool):
        return f"{value.upper()}"
    return to_filter(str(value))


def to_array_filter[T: (int, str, datetime, bool)](value: Union[T, list[T]]) -> str:
    if not isinstance(value, list):
        value = [value]
    return f"({', '.join([to_filter(item) for item in value])})"


def to_array_value[T: (int, str, datetime, bool)](value: Union[T, list[T]]) -> str:
    if not isinstance(value, list):
        value = [value]
    return f"ARRAY[{', '.join([to_filter(item) for item in value])}]"
