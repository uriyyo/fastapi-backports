from __future__ import annotations

import types
from copy import copy
from enum import Enum
from functools import wraps
from typing import Any, Callable, Dict, List, Literal, Optional, Sequence, Set, Type, Union, cast

from fastapi import FastAPI as _FastAPI
from fastapi import params
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.exceptions import FastAPIError
from fastapi.routing import APIRoute as _APIRoute
from fastapi.routing import APIRouter as _APIRouter
from fastapi.routing import APIWebSocketRoute as _APIWebSocketRoute
from fastapi.routing import _merge_lifespan_context
from fastapi.types import DecoratedCallable, IncEx
from fastapi.utils import generate_unique_id, get_value_or_default
from starlette import routing
from starlette.middleware import Middleware
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute
from typing_extensions import TypeIs, override

from fastapi_backports._retyped import APIRoute, APIRouter, APIWebSocketRoute, FastAPI

from ._base import BaseBackporter

_APIRoute_init = _APIRoute.__init__
_APIWebSocketRoute_init = _APIWebSocketRoute.__init__
_APIRouter_init = _APIRouter.__init__


class _PatchedAPIRouter(_APIRouter):
    middleware: Optional[Sequence[Middleware]] = None

    @override
    def get(self, *args, **kwargs) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(*args, methods=["GET"], **kwargs)

    @override
    def post(self, *args, **kwargs) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(*args, methods=["POST"], **kwargs)

    @override
    def put(self, *args, **kwargs) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(*args, methods=["PUT"], **kwargs)

    @override
    def patch(self, *args, **kwargs) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(*args, methods=["PATCH"], **kwargs)

    @override
    def delete(self, *args, **kwargs) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(*args, methods=["DELETE"], **kwargs)

    @override
    def head(self, *args, **kwargs) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(*args, methods=["HEAD"], **kwargs)

    @override
    def options(self, *args, **kwargs) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(*args, methods=["OPTIONS"], **kwargs)

    @override
    def trace(self, *args, **kwargs) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(*args, methods=["TRACE"], **kwargs)

    @override
    def add_api_route(
        self: APIRouter,
        path: str,
        endpoint: Callable[..., Any],
        *,
        response_model: Any = Default(None),
        status_code: Optional[int] = None,
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        methods: Optional[Union[Set[str], List[str]]] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[IncEx] = None,
        response_model_exclude: Optional[IncEx] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(JSONResponse),
        name: Optional[str] = None,
        route_class_override: Optional[Type[APIRoute]] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        openapi_extra: Optional[Dict[str, Any]] = None,
        generate_unique_id_function: Union[Callable[[APIRoute], str], DefaultPlaceholder] = Default(generate_unique_id),
        middleware: Optional[Sequence[Middleware]] = None,
    ) -> None:
        route_class = route_class_override or self.route_class
        responses = responses or {}
        combined_responses = {**self.responses, **responses}
        current_response_class = get_value_or_default(response_class, self.default_response_class)
        current_tags = self.tags.copy()
        if tags:
            current_tags.extend(tags)
        current_dependencies = self.dependencies.copy()
        if dependencies:
            current_dependencies.extend(dependencies)
        current_callbacks = self.callbacks.copy()
        if callbacks:
            current_callbacks.extend(callbacks)
        current_middleware = [*copy(self.middleware or [])]
        if middleware:
            current_middleware.extend(middleware)
        current_generate_unique_id = get_value_or_default(generate_unique_id_function, self.generate_unique_id_function)
        route = route_class(
            self.prefix + path,
            endpoint=endpoint,
            response_model=response_model,
            status_code=status_code,
            tags=current_tags,
            dependencies=current_dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=combined_responses,
            deprecated=deprecated or self.deprecated,
            methods=methods,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema and self.include_in_schema,
            response_class=current_response_class,
            name=name,
            dependency_overrides_provider=self.dependency_overrides_provider,
            callbacks=current_callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=current_generate_unique_id,
            middleware=current_middleware,
        )
        self.routes.append(route)

    @override
    def api_route(
        self: APIRouter,
        path: str,
        **kwargs: Any,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            self.add_api_route(path, func, **kwargs)
            return func

        return decorator

    @override
    def add_api_websocket_route(
        self: APIRouter,
        path: str,
        endpoint: Callable[..., Any],
        name: Optional[str] = None,
        *,
        middleware: Optional[Sequence[Middleware]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
    ) -> None:
        current_dependencies = self.dependencies.copy()
        if dependencies:
            current_dependencies.extend(dependencies)
        current_middleware = [*copy(self.middleware or [])]
        if middleware:
            current_middleware.extend(middleware)
        route = APIWebSocketRoute(
            self.prefix + path,
            endpoint=endpoint,
            name=name,
            dependency_overrides_provider=self.dependency_overrides_provider,
            dependencies=current_dependencies,
            middleware=current_middleware,
        )
        self.routes.append(route)

    @override
    def websocket(
        self: APIRouter,
        path: str,
        **kwargs: Any,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            self.add_api_websocket_route(path, func, **kwargs)
            return func

        return decorator

    @override
    def include_router(
        self: APIRouter,
        router: APIRouter,
        *,
        prefix: str = "",
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        default_response_class: Type[Response] = Default(JSONResponse),
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
        generate_unique_id_function: Callable[[APIRoute], str] = Default(generate_unique_id),
        middleware: Optional[Sequence[Middleware]] = None,
    ) -> None:
        if prefix:
            assert prefix.startswith("/"), "A path prefix must start with '/'"
            assert not prefix.endswith("/"), "A path prefix must not end with '/', as the routes will start with '/'"
        else:
            for r in router.routes:
                path = getattr(r, "path")  # noqa: B009
                name = getattr(r, "name", "unknown")
                if path is not None and not path:
                    raise FastAPIError(f"Prefix and path cannot be both empty (path operation: {name})")
        if responses is None:
            responses = {}
        for route in router.routes:
            if isinstance(route, APIRoute):
                combined_responses = {**responses, **route.responses}
                use_response_class = get_value_or_default(
                    route.response_class,
                    router.default_response_class,
                    default_response_class,
                    self.default_response_class,
                )
                current_tags = []
                if tags:
                    current_tags.extend(tags)
                if route.tags:
                    current_tags.extend(route.tags)
                current_dependencies: List[params.Depends] = []
                if dependencies:
                    current_dependencies.extend(dependencies)
                if route.dependencies:
                    current_dependencies.extend(route.dependencies)
                current_callbacks = []
                if callbacks:
                    current_callbacks.extend(callbacks)
                if route.callbacks:
                    current_callbacks.extend(route.callbacks)
                current_middleware = []
                if middleware:
                    current_middleware.extend(middleware)
                if route.middleware:
                    current_middleware.extend(route.middleware)
                current_generate_unique_id = get_value_or_default(
                    route.generate_unique_id_function,
                    router.generate_unique_id_function,
                    generate_unique_id_function,
                    self.generate_unique_id_function,
                )
                self.add_api_route(
                    prefix + route.path,
                    route.endpoint,
                    response_model=route.response_model,
                    status_code=route.status_code,
                    tags=current_tags,
                    dependencies=current_dependencies,
                    summary=route.summary,
                    description=route.description,
                    response_description=route.response_description,
                    responses=combined_responses,
                    deprecated=route.deprecated or deprecated or self.deprecated,
                    methods=route.methods,
                    operation_id=route.operation_id,
                    response_model_include=route.response_model_include,
                    response_model_exclude=route.response_model_exclude,
                    response_model_by_alias=route.response_model_by_alias,
                    response_model_exclude_unset=route.response_model_exclude_unset,
                    response_model_exclude_defaults=route.response_model_exclude_defaults,
                    response_model_exclude_none=route.response_model_exclude_none,
                    include_in_schema=route.include_in_schema and self.include_in_schema and include_in_schema,
                    response_class=use_response_class,
                    name=route.name,
                    route_class_override=type(route),
                    callbacks=current_callbacks,
                    openapi_extra=route.openapi_extra,
                    generate_unique_id_function=current_generate_unique_id,
                    middleware=current_middleware,
                )
            elif isinstance(route, routing.Route):
                methods = list(route.methods or [])
                self.add_route(
                    prefix + route.path,
                    route.endpoint,
                    methods=methods,
                    include_in_schema=route.include_in_schema,
                    name=route.name,
                )
            elif isinstance(route, APIWebSocketRoute):
                current_dependencies = []
                if dependencies:
                    current_dependencies.extend(dependencies)
                if route.dependencies:
                    current_dependencies.extend(route.dependencies)
                current_middleware = [*copy(self.middleware or [])]
                if router.middleware:
                    current_middleware.extend(router.middleware)
                if middleware:
                    current_middleware.extend(middleware)
                self.add_api_websocket_route(
                    prefix + route.path,
                    route.endpoint,
                    dependencies=current_dependencies,
                    name=route.name,
                    middleware=current_middleware,
                )
            elif isinstance(route, routing.WebSocketRoute):
                self.add_websocket_route(prefix + route.path, route.endpoint, name=route.name)
        for handler in router.on_startup:
            self.add_event_handler("startup", handler)
        for handler in router.on_shutdown:
            self.add_event_handler("shutdown", handler)
        self.lifespan_context = _merge_lifespan_context(
            self.lifespan_context,
            router.lifespan_context,
        )


def _add_middleware_to_init(
    init_func: Callable[..., None],
    attr: Literal[
        "app",  # for APIRoute and APIWebSocketRoute
        "middleware_stack",  # for APIRouter
    ],
    *,
    wrap: bool = True,
) -> Callable[..., None]:
    @wraps(init_func)
    def _new_init(
        self: Any,
        *args: Any,
        middleware: Optional[Sequence[Middleware]] = None,
        **kwargs: Any,
    ) -> None:
        init_func(self, *args, **kwargs)

        # store original attribute to allow access to unwrapped app/middleware_stack
        setattr(self, f"_original_{attr}", getattr(self, attr))

        self.middleware = middleware

        if wrap:
            for cls, _args, _kwargs in reversed(middleware or ()):
                wrapped = cls(getattr(self, attr), *_args, **_kwargs)
                setattr(self, attr, wrapped)

    return _new_init


def _is_override(func: Any) -> TypeIs[types.FunctionType]:
    return getattr(func, "__override__", False)


def _create_delegate_method(name: str) -> Callable[..., Any]:
    def _delegate_method(self: FastAPI, *args: Any, **kwargs: Any) -> Any:
        return getattr(self.router, name)(*args, **kwargs)

    return _delegate_method


class Backporter(BaseBackporter):
    @classmethod
    def label(cls) -> str:
        return "route_middleware"

    @classmethod
    def backport(cls) -> None:
        _APIRoute.middleware = None  # type: ignore[unresolved-attribute]
        _APIRoute.__init__ = _add_middleware_to_init(_APIRoute_init, "app")  # type: ignore[assignment]

        _APIWebSocketRoute.middleware = None  # type: ignore[unresolved-attribute]
        _APIWebSocketRoute.__init__ = _add_middleware_to_init(_APIWebSocketRoute_init, "app")  # type: ignore[assignment]

        _APIRouter.middleware = None  # type: ignore[unresolved-attribute]
        _APIRouter.__init__ = _add_middleware_to_init(_APIRouter_init, "middleware_stack", wrap=False)  # type: ignore[assignment]

        # copy all overridden methods from _PatchedAPIRouter to original APIRouter and FastAPI
        for name, method in _PatchedAPIRouter.__dict__.items():
            if callable(method) and _is_override(method):
                original_method = cast("Callable[..., Any]", getattr(_APIRouter, name))

                wrapped = wraps(original_method)(method)
                setattr(_APIRouter, name, wrapped)

                original_method = getattr(_FastAPI, name)
                wrapped_app_method = wraps(original_method)(_create_delegate_method(name))

                setattr(_FastAPI, name, wrapped_app_method)


__all__ = [
    "Backporter",
]
