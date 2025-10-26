from typing import TYPE_CHECKING, Any

from ._backporter import backport
from ._backports.lifespan_decorator import LifespanDecoratorBackporter
from ._backports.multiple_query_models import MultipleQueryModelsBackporter
from ._backports.postponed_annotations import PostponedAnnotationsBackporter
from ._backports.query_method import QueryMethodBackporter
from ._backports.route_middleware import RouteMiddlewareBackporter
from ._backports.type_alias_type import TypeAliasTypeBackporter

if TYPE_CHECKING:
    from ._retyped import APIRoute, APIRouter, APIWebSocketRoute, FastAPI
else:

    def __getattr__(name: str) -> Any:
        from . import _retyped

        if name in _retyped.__all__:
            return getattr(_retyped, name)

        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "APIRoute",
    "APIRouter",
    "APIWebSocketRoute",
    "FastAPI",
    "LifespanDecoratorBackporter",
    "MultipleQueryModelsBackporter",
    "PostponedAnnotationsBackporter",
    "QueryMethodBackporter",
    "RouteMiddlewareBackporter",
    "TypeAliasTypeBackporter",
    "backport",
]
