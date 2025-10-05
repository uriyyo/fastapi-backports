from typing import Any, Dict, List, Mapping, Sequence, Tuple, Union

from fastapi import params
from fastapi.dependencies.utils import (
    ModelField,
    _get_multidict_value,
    _validate_value_with_model_field,
    get_cached_model_fields,
    lenient_issubclass,
)
from pydantic import BaseModel
from starlette.datastructures import Headers, QueryParams

from ._base import BaseBackporter


def _get_flat_fields_from_params(fields: List[ModelField]) -> List[ModelField]:
    if not fields:
        return fields

    fields_to_extract = []
    for f in fields:
        if lenient_issubclass(f.type_, BaseModel):
            fields_to_extract.extend(get_cached_model_fields(f.type_))
        else:
            fields_to_extract.append(f)
    return fields_to_extract


def request_params_to_args(
    fields: Sequence[ModelField],
    received_params: Union[Mapping[str, Any], QueryParams, Headers],
) -> Tuple[Dict[str, Any], List[Any]]:
    values: Dict[str, Any] = {}
    errors: List[Dict[str, Any]] = []

    if not fields:
        return values, errors

    default_convert_underscores = True

    params_to_process: Dict[str, Any] = {}

    fields_to_extract = [
        (field, cached_field)
        for field in fields
        if lenient_issubclass(field.type_, BaseModel)
        for cached_field in get_cached_model_fields(field.type_)
    ]

    processed_keys = set()

    for parent_field, field in fields_to_extract:
        alias = None
        if isinstance(received_params, Headers):
            # Handle fields extracted from a Pydantic Model for a header, each field
            # doesn't have a FieldInfo of type Header with the default convert_underscores=True
            convert_underscores = getattr(
                parent_field.field_info,
                "convert_underscores",
                default_convert_underscores,
            )
            if convert_underscores:
                alias = field.alias if field.alias != field.name else field.name.replace("_", "-")
        value = _get_multidict_value(field, received_params, alias=alias)
        if value is not None:
            params_to_process[field.name] = value
        processed_keys.add(alias or field.alias)
        processed_keys.add(field.name)

    for key, value in received_params.items():
        if key not in processed_keys:
            params_to_process[key] = value

    for field in fields:
        field_info = field.field_info
        assert isinstance(field_info, params.Param), "Params must be subclasses of Param"

        if lenient_issubclass(field.type_, BaseModel):
            loc: Tuple[str, ...] = (field_info.in_.value,)
            v_, errors_ = _validate_value_with_model_field(field=field, value=params_to_process, values=values, loc=loc)
        else:
            value = _get_multidict_value(field, received_params)
            loc = (field_info.in_.value, field.alias)
            v_, errors_ = _validate_value_with_model_field(field=field, value=value, values=values, loc=loc)

        if errors_:
            errors.extend(errors_)
        else:
            values[field.name] = v_
    return values, errors


class Backporter(BaseBackporter):
    @classmethod
    def label(cls) -> str:
        return "multiple_query_models"

    @classmethod
    def backport(cls) -> None:
        from fastapi.dependencies import utils as _deps_utils
        from fastapi.openapi import utils as _openapi_utils

        _deps_utils.request_params_to_args = request_params_to_args  # type: ignore[invalid-assignment]
        _deps_utils._get_flat_fields_from_params = _get_flat_fields_from_params  # type: ignore[invalid-assignment]

        _openapi_utils._get_flat_fields_from_params = _get_flat_fields_from_params  # type: ignore[invalid-assignment]


__all__ = [
    "Backporter",
]
