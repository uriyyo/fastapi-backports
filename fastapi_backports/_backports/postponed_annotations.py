from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, AsyncIterator, Iterable, Optional, Union
from typing import ForwardRef as _Typing_ForwardRef

from fastapi import FastAPI
from fastapi import FastAPI as _FastAPI
from fastapi._compat import ModelField, lenient_issubclass
from fastapi.datastructures import DefaultPlaceholder
from fastapi.dependencies import utils as _dependencies_utils
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import (
    _should_embed_body_fields,
    get_body_field,
    get_dependant,
    get_flat_dependant,
    get_parameterless_sub_dependant,
    get_typed_return_annotation,
)
from fastapi.routing import (
    APIRoute as _APIRoute,
)
from fastapi.routing import (
    APIWebSocketRoute as _APIWebSocketRoute,
)
from fastapi.routing import (
    _merge_lifespan_context,
    get_websocket_app,
    websocket_session,
)
from fastapi.utils import create_cloned_field, create_model_field
from starlette.responses import Response
from starlette.routing import BaseRoute
from typing_extensions import ForwardRef as _TypingExt_ForwardRef
from typing_extensions import TypeAlias, TypeIs

from fastapi_backports._retyped import APIRoute, APIWebSocketRoute

from ._base import BaseBackporter

try:
    from fastapi.routing import request_response
except ImportError:
    from starlette.routing import request_response

_APIRouteType: TypeAlias = Union[APIRoute, APIWebSocketRoute]

_forward_refs_type = (_Typing_ForwardRef, _TypingExt_ForwardRef)


def _is_postponed_model_field(field: ModelField) -> bool:
    try:
        return isinstance(field.type_, _forward_refs_type)
    except TypeError:
        return False


def _all_dependant_fields(dependant: Dependant) -> Iterable[ModelField]:
    yield from dependant.path_params
    yield from dependant.query_params
    yield from dependant.header_params
    yield from dependant.cookie_params
    yield from dependant.body_params

    for sub_dependant in dependant.dependencies:
        yield from _all_dependant_fields(sub_dependant)


def _all_model_fields(route: _APIRouteType) -> Iterable[ModelField]:
    if isinstance(route, APIRoute) and route.response_field:
        yield route.response_field

    yield from _all_dependant_fields(route._flat_dependant)


def _is_postponed_route_declaration(route: BaseRoute) -> TypeIs[_APIRouteType]:
    if isinstance(route, (APIRoute, APIWebSocketRoute)):
        return any(_is_postponed_model_field(field) for field in _all_model_fields(route))

    return False


def _recreate_route_dependant(route: _APIRouteType) -> _APIRouteType:
    if isinstance(route, APIRoute):
        if not getattr(route, "_custom_response_model", False):
            return_annotation = get_typed_return_annotation(route.endpoint)
            if lenient_issubclass(return_annotation, Response):
                route.response_model = None
            else:
                route.response_model = return_annotation

        if route.response_model:
            response_name = "Response_" + route.unique_id
            route.response_field = create_model_field(
                name=response_name,
                type_=route.response_model,
                mode="serialization",
            )

            route.secure_cloned_response_field = create_cloned_field(route.response_field)
        else:
            route.response_field = None
            route.secure_cloned_response_field = None

        route.dependant = get_dependant(path=route.path_format, call=route.endpoint)
        for depends in route.dependencies[::-1]:
            route.dependant.dependencies.insert(
                0,
                get_parameterless_sub_dependant(depends=depends, path=route.path_format),
            )
        route._flat_dependant = get_flat_dependant(route.dependant)
        route._embed_body_fields = _should_embed_body_fields(route._flat_dependant.body_params)
        route.body_field = get_body_field(
            flat_dependant=route._flat_dependant,
            name=route.unique_id,
            embed_body_fields=route._embed_body_fields,
        )
        route.app = request_response(route.get_route_handler())
    elif isinstance(route, APIWebSocketRoute):
        route.dependant = get_dependant(path=route.path_format, call=route.endpoint)
        for depends in route.dependencies[::-1]:
            route.dependant.dependencies.insert(
                0,
                get_parameterless_sub_dependant(depends=depends, path=route.path_format),
            )
        route._flat_dependant = get_flat_dependant(route.dependant)
        route._embed_body_fields = _should_embed_body_fields(route._flat_dependant.body_params)
        route.app = websocket_session(
            get_websocket_app(
                dependant=route.dependant,
                dependency_overrides_provider=route.dependency_overrides_provider,
                embed_body_fields=route._embed_body_fields,
            )
        )

    # make sure we keep any middleware applied to the route
    for cls, _args, _kwargs in reversed(route.middleware or ()):
        route.app = cls(route.app, *_args, **_kwargs)

    return route


def _update_postponed_routes(app: FastAPI) -> None:
    for i, route in enumerate(app.router.routes):
        if _is_postponed_route_declaration(route):
            app.router.routes[i] = _recreate_route_dependant(route)


@asynccontextmanager
async def _validate_postponed_routes(app: FastAPI) -> AsyncIterator[None]:
    _update_postponed_routes(app)
    yield


def _create_overrides() -> Any:
    _original_init = _FastAPI.__init__

    class _FastAPIPatched(_FastAPI):
        @wraps(_original_init)
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            _original_init(self, *args, **kwargs)

            self.router.lifespan_context = _merge_lifespan_context(
                _validate_postponed_routes,
                self.router.lifespan_context,
            )

    _original_websocket_init = _APIWebSocketRoute.__init__

    class _APIWebSocketRoutePatched(_APIWebSocketRoute):
        @wraps(_original_websocket_init)
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            _original_websocket_init(self, *args, **kwargs)
            self.dependency_overrides_provider = kwargs.get("dependency_overrides_provider")

    _original_route_init = _APIRoute.__init__

    class _APIRoutePatched(_APIRoute):
        @wraps(_original_route_init)
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            if "response_model" in kwargs:
                self._custom_response_model = not isinstance(kwargs["response_model"], DefaultPlaceholder)
            else:
                self._custom_response_model = False

            _original_route_init(self, *args, **kwargs)

    return _APIRoutePatched, _APIWebSocketRoutePatched, _FastAPIPatched


_original_evaluate_forwardref = _dependencies_utils.evaluate_forwardref


@wraps(_original_evaluate_forwardref)
def evaluate_forwardref(
    value: Any,
    globalns: Optional[Any] = None,
    localns: Optional[Any] = None,
) -> Any:
    try:
        return _original_evaluate_forwardref(value, globalns, localns)
    except (NameError, TypeError):
        return value


class PostponedAnnotationsBackporter(BaseBackporter):
    @classmethod
    def label(cls) -> str:
        return "issues/13056"

    @classmethod
    def backport(cls) -> None:
        _APIRoutePatched, _APIWebSocketRoutePatched, _FastAPIPatched = _create_overrides()  # noqa: N806

        _FastAPI.__init__ = _FastAPIPatched.__init__  # type: ignore[assignment]
        _APIRoute.__init__ = _APIRoutePatched.__init__  # type: ignore[assignment]
        _APIWebSocketRoutePatched.__init__ = _APIWebSocketRoutePatched.__init__  # type: ignore[assignment]

        _dependencies_utils.evaluate_forwardref = evaluate_forwardref  # type: ignore[assignment]


__all__ = [
    "PostponedAnnotationsBackporter",
]
