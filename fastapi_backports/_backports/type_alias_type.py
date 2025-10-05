from typing import Any

from fastapi.dependencies import utils as _deps_utils
from typing_extensions import Protocol, TypeIs

from fastapi_backports._backports import BaseBackporter

try:
    from typing_extensions import TypeAliasType as _TETypeAliasType
except ImportError:

    class _TETypeAliasType:  # type: ignore[misc]
        __value__: Any


try:
    from typing import TypeAliasType as _BuiltinTypeAliasType  # type: ignore[unresolved-import]
except ImportError:

    class _BuiltinTypeAliasType:  # type: ignore[misc]
        __value__: Any


_original_analyze_param = _deps_utils.analyze_param


class _HasValue(Protocol):
    __value__: Any


def _is_type_alias_type(annotation: Any) -> TypeIs[_HasValue]:
    return isinstance(annotation, (_TETypeAliasType, _BuiltinTypeAliasType))


def analyze_param(
    *,
    param_name: str,
    annotation: Any,
    value: Any,
    is_path_param: bool,
) -> _deps_utils.ParamDetails:
    if _is_type_alias_type(annotation):
        annotation = annotation.__value__

    return _original_analyze_param(
        param_name=param_name,
        annotation=annotation,
        value=value,
        is_path_param=is_path_param,
    )


class Backporter(BaseBackporter):
    @classmethod
    def label(cls) -> str:
        return "type_alias_type"

    @classmethod
    def backport(cls) -> None:
        _deps_utils.analyze_param = analyze_param  # type: ignore[assignment]


__all__ = [
    "Backporter",
]
