from typing import Final, Iterable, Optional, Set, Type

from ._backports import (
    BaseBackporter,
)
from ._backports.lifespan_decorator import LifespanDecoratorBackporter
from ._backports.multiple_query_models import MultipleQueryModelsBackporter
from ._backports.postponed_annotations import PostponedAnnotationsBackporter
from ._backports.query_method import QueryMethodBackporter
from ._backports.route_middleware import RouteMiddlewareBackporter
from ._backports.type_alias_type import TypeAliasTypeBackporter

_BACKPORTED: Final[Set[str]] = set()


def _run_backports(backports: Iterable[Type[BaseBackporter]]) -> None:
    for _backport in backports:
        if not _backport.needs_backport():
            continue

        if _backport.label() in _BACKPORTED:
            continue

        _backport.backport()
        _BACKPORTED.add(_backport.label())


def backport(backports: Optional[Iterable[Type[BaseBackporter]]] = None) -> None:
    if not backports:
        _run_backports(
            [
                RouteMiddlewareBackporter,
                MultipleQueryModelsBackporter,
                TypeAliasTypeBackporter,
                PostponedAnnotationsBackporter,
                QueryMethodBackporter,
                LifespanDecoratorBackporter,
            ],
        )
    else:
        _run_backports(backports)


__all__ = [
    "backport",
]
