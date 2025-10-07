from typing import Final, Iterable, Set, Type

from ._backports import (
    BaseBackporter,
    lifespan_decorator,
    multiple_query_models,
    postponed_annotations,
    query_method,
    route_middleware,
    type_alias_type,
)

_BACKPORTED: Final[Set[str]] = set()


def _run_backports(backports: Iterable[Type[BaseBackporter]]) -> None:
    for _backport in backports:
        if not _backport.needs_backport():
            continue

        if _backport.label() in _BACKPORTED:
            continue

        _backport.backport()
        _BACKPORTED.add(_backport.label())


def backport() -> None:
    _run_backports(
        [
            route_middleware.Backporter,
            multiple_query_models.Backporter,
            type_alias_type.Backporter,
            postponed_annotations.Backporter,
            query_method.Backporter,
            lifespan_decorator.Backporter,
        ],
    )


__all__ = [
    "backport",
]
