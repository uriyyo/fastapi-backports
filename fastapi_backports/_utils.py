from __future__ import annotations

from typing import Any

try:
    from fastapi.utils import create_cloned_field as _fastapi_create_cloned_field  # type: ignore[ty:unresolved-import]
except ImportError:
    _fastapi_create_cloned_field = None

from fastapi.dependencies.utils import (
    ModelField,
    lenient_issubclass,
)


def create_cloned_field(field: ModelField) -> ModelField:
    if _fastapi_create_cloned_field is not None:
        return _fastapi_create_cloned_field(field)

    return field


def check_field_is_subclass(field: ModelField, cls: type[Any] | tuple[type[Any], ...]) -> bool:
    return lenient_issubclass(get_field_type(field), cls)


def check_field_is_instance(field: ModelField, cls: type[Any] | tuple[type[Any], ...]) -> bool:
    return isinstance(get_field_type(field), cls)


def get_field_type(field: ModelField) -> Any:
    try:
        return field.field_info.annotation
    except AttributeError:
        return field.type_  # type: ignore[ty:unresolved-attribute]


__all__ = [
    "check_field_is_instance",
    "check_field_is_subclass",
    "create_cloned_field",
    "get_field_type",
]
