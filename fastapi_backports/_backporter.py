from typing import Iterable, Type

from typing_extensions import NotRequired, TypedDict, Unpack

from ._backports import (
    BaseBackporter,
    multiple_query_models,
    type_alias_type,
)

_BACKPORTED = set()


def _run_backports(backports: Iterable[Type[BaseBackporter]]) -> None:
    for _backport in backports:
        if not _backport.needs_backport():
            continue

        if _backport.label() in _BACKPORTED:
            continue

        _backport.backport()
        _BACKPORTED.add(_backport.label())


class _AvailableBackports(TypedDict):
    multiple_query_models: NotRequired[bool]
    type_alias_type: NotRequired[bool]
    annotated_forward_ref: NotRequired[bool]


def _resolve_backports(**kwargs: Unpack[_AvailableBackports]) -> Iterable[Type[BaseBackporter]]:
    if kwargs.get("multiple_query_models", True):
        yield multiple_query_models.Backporter

    if kwargs.get("type_alias_type", True):
        yield type_alias_type.Backporter


def backport(**kwargs: Unpack[_AvailableBackports]) -> None:
    _run_backports(_resolve_backports(**kwargs))


__all__ = [
    "backport",
]
