from ipaddress import IPv4Address
import json
from dataclasses import asdict, is_dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel
from typing import Any

TYPES_TO_STRING = (Decimal, float, timedelta, IPv4Address)


def to_json_serialisable(object: Any) -> Any:
    if isinstance(object, (int, str)):
        return object
    if isinstance(object, (tuple, list, set)):
        return [to_json_serialisable(item) for item in object]
    if isinstance(object, dict):
        return {key: to_json_serialisable(value) for key, value in object.items()}
    if is_dataclass(object):
        return to_json_serialisable(asdict(object))
    if isinstance(object, BaseModel):
        return to_json_serialisable(object.dict())
    if isinstance(object, Enum):
        return object.name
    if isinstance(object, (date, datetime)):
        return object.isoformat()
    if isinstance(object, TYPES_TO_STRING):
        return str(object)
    return object


def serialise_json(object: Any, *args: Any, **kwargs: Any) -> str:
    return json.dumps(to_json_serialisable(object), *args, **kwargs)


def parse_json(object: Any, *args: Any, **kwargs: Any) -> Any:
    return json.loads(object, *args, **kwargs)
