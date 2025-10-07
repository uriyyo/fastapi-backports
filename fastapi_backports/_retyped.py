from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Sequence, Set, Type, Union

from fastapi import params
from fastapi.applications import FastAPI as _FastAPI
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.routing import APIRoute as _APIRoute
from fastapi.routing import APIRouter as _APIRouter
from fastapi.routing import APIWebSocketRoute as _APIWebSocketRoute
from fastapi.types import DecoratedCallable, IncEx
from fastapi.utils import generate_unique_id
from starlette.middleware import Middleware
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute
from starlette.types import ASGIApp, Lifespan
from typing_extensions import override

if TYPE_CHECKING:

    class _CommonRouterMethodsMixin:
        def get(
            self,
            path: str,
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
            operation_id: Optional[str] = None,
            response_model_include: Optional[IncEx] = None,
            response_model_exclude: Optional[IncEx] = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: Type[Response] = Default(JSONResponse),
            name: Optional[str] = None,
            callbacks: Optional[List[BaseRoute]] = None,
            openapi_extra: Optional[Dict[str, Any]] = None,
            generate_unique_id_function: Callable[[APIRoute], str] = Default(generate_unique_id),
            middleware: Optional[Sequence[Middleware]] = None,
        ) -> Callable[[DecoratedCallable], DecoratedCallable]:
            pass

        def post(
            self,
            path: str,
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
            operation_id: Optional[str] = None,
            response_model_include: Optional[IncEx] = None,
            response_model_exclude: Optional[IncEx] = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: Type[Response] = Default(JSONResponse),
            name: Optional[str] = None,
            callbacks: Optional[List[BaseRoute]] = None,
            openapi_extra: Optional[Dict[str, Any]] = None,
            generate_unique_id_function: Callable[[APIRoute], str] = Default(generate_unique_id),
            middleware: Optional[Sequence[Middleware]] = None,
        ) -> Callable[[DecoratedCallable], DecoratedCallable]:
            pass

        def patch(
            self,
            path: str,
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
            operation_id: Optional[str] = None,
            response_model_include: Optional[IncEx] = None,
            response_model_exclude: Optional[IncEx] = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: Type[Response] = Default(JSONResponse),
            name: Optional[str] = None,
            callbacks: Optional[List[BaseRoute]] = None,
            openapi_extra: Optional[Dict[str, Any]] = None,
            generate_unique_id_function: Callable[[APIRoute], str] = Default(generate_unique_id),
            middleware: Optional[Sequence[Middleware]] = None,
        ) -> Callable[[DecoratedCallable], DecoratedCallable]:
            pass

        def put(
            self,
            path: str,
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
            operation_id: Optional[str] = None,
            response_model_include: Optional[IncEx] = None,
            response_model_exclude: Optional[IncEx] = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: Type[Response] = Default(JSONResponse),
            name: Optional[str] = None,
            callbacks: Optional[List[BaseRoute]] = None,
            openapi_extra: Optional[Dict[str, Any]] = None,
            generate_unique_id_function: Callable[[APIRoute], str] = Default(generate_unique_id),
            middleware: Optional[Sequence[Middleware]] = None,
        ) -> Callable[[DecoratedCallable], DecoratedCallable]:
            pass

        def head(
            self,
            path: str,
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
            operation_id: Optional[str] = None,
            response_model_include: Optional[IncEx] = None,
            response_model_exclude: Optional[IncEx] = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: Type[Response] = Default(JSONResponse),
            name: Optional[str] = None,
            callbacks: Optional[List[BaseRoute]] = None,
            openapi_extra: Optional[Dict[str, Any]] = None,
            generate_unique_id_function: Callable[[APIRoute], str] = Default(generate_unique_id),
            middleware: Optional[Sequence[Middleware]] = None,
        ) -> Callable[[DecoratedCallable], DecoratedCallable]:
            pass

        def options(
            self,
            path: str,
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
            operation_id: Optional[str] = None,
            response_model_include: Optional[IncEx] = None,
            response_model_exclude: Optional[IncEx] = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: Type[Response] = Default(JSONResponse),
            name: Optional[str] = None,
            callbacks: Optional[List[BaseRoute]] = None,
            openapi_extra: Optional[Dict[str, Any]] = None,
            generate_unique_id_function: Callable[[APIRoute], str] = Default(generate_unique_id),
            middleware: Optional[Sequence[Middleware]] = None,
        ) -> Callable[[DecoratedCallable], DecoratedCallable]:
            pass

        def delete(
            self,
            path: str,
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
            operation_id: Optional[str] = None,
            response_model_include: Optional[IncEx] = None,
            response_model_exclude: Optional[IncEx] = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: Type[Response] = Default(JSONResponse),
            name: Optional[str] = None,
            callbacks: Optional[List[BaseRoute]] = None,
            openapi_extra: Optional[Dict[str, Any]] = None,
            generate_unique_id_function: Callable[[APIRoute], str] = Default(generate_unique_id),
            middleware: Optional[Sequence[Middleware]] = None,
        ) -> Callable[[DecoratedCallable], DecoratedCallable]:
            pass

        def trace(
            self,
            path: str,
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
            operation_id: Optional[str] = None,
            response_model_include: Optional[IncEx] = None,
            response_model_exclude: Optional[IncEx] = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: Type[Response] = Default(JSONResponse),
            name: Optional[str] = None,
            callbacks: Optional[List[BaseRoute]] = None,
            openapi_extra: Optional[Dict[str, Any]] = None,
            generate_unique_id_function: Callable[[APIRoute], str] = Default(generate_unique_id),
            middleware: Optional[Sequence[Middleware]] = None,
        ) -> Callable[[DecoratedCallable], DecoratedCallable]:
            pass

        def query(
            self,
            path: str,
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
            operation_id: Optional[str] = None,
            response_model_include: Optional[IncEx] = None,
            response_model_exclude: Optional[IncEx] = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: Type[Response] = Default(JSONResponse),
            name: Optional[str] = None,
            callbacks: Optional[List[BaseRoute]] = None,
            openapi_extra: Optional[Dict[str, Any]] = None,
            generate_unique_id_function: Callable[[APIRoute], str] = Default(generate_unique_id),
            middleware: Optional[Sequence[Middleware]] = None,
        ) -> Callable[[DecoratedCallable], DecoratedCallable]:
            pass

        def include_router(
            self,
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
            pass

        def add_api_route(
            self,
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
            generate_unique_id_function: Union[Callable[[APIRoute], str], DefaultPlaceholder] = Default(
                generate_unique_id
            ),
            middleware: Optional[Sequence[Middleware]] = None,
        ) -> None:
            pass

        def api_route(
            self,
            path: str,
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
            methods: Optional[List[str]] = None,
            operation_id: Optional[str] = None,
            response_model_include: Optional[IncEx] = None,
            response_model_exclude: Optional[IncEx] = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: Type[Response] = Default(JSONResponse),
            name: Optional[str] = None,
            callbacks: Optional[List[BaseRoute]] = None,
            openapi_extra: Optional[Dict[str, Any]] = None,
            generate_unique_id_function: Callable[[APIRoute], str] = Default(generate_unique_id),
            middleware: Optional[Sequence[Middleware]] = None,
        ) -> Callable[[DecoratedCallable], DecoratedCallable]:
            pass

        def add_api_websocket_route(
            self,
            path: str,
            endpoint: Callable[..., Any],
            name: Optional[str] = None,
            *,
            middleware: Optional[Sequence[Middleware]] = None,
            dependencies: Optional[Sequence[params.Depends]] = None,
        ) -> None:
            pass

        def websocket(
            self,
            path: str,
            name: Optional[str] = None,
            *,
            dependencies: Optional[Sequence[params.Depends]] = None,
            middleware: Optional[Sequence[Middleware]] = None,
        ) -> Callable[[DecoratedCallable], DecoratedCallable]:
            pass

    class APIRoute(_APIRoute):
        middleware: Optional[Sequence[Middleware]]

        @override
        def __init__(
            self,
            path: str,
            endpoint: Callable[..., Any],
            *,
            response_model: Any = None,
            status_code: Optional[int] = None,
            tags: Optional[List[Union[str, Enum]]] = None,
            dependencies: Optional[Sequence[params.Depends]] = None,
            summary: Optional[str] = None,
            description: Optional[str] = None,
            response_description: str = "Successful Response",
            responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
            deprecated: Optional[bool] = None,
            name: Optional[str] = None,
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
            dependency_overrides_provider: Optional[Any] = None,
            callbacks: Optional[List[BaseRoute]] = None,
            openapi_extra: Optional[Dict[str, Any]] = None,
            generate_unique_id_function: Union[Callable[[APIRoute], str], DefaultPlaceholder] = Default(
                generate_unique_id
            ),
            middleware: Optional[Sequence[Middleware]] = None,
        ) -> None:
            pass

    class APIWebSocketRoute(_APIWebSocketRoute):
        middleware: Optional[Sequence[Middleware]]

        @override
        def __init__(
            self,
            path: str,
            endpoint: Callable[..., Any],
            *,
            name: Optional[str] = None,
            dependencies: Optional[Sequence[params.Depends]] = None,
            dependency_overrides_provider: Optional[Any] = None,
            middleware: Optional[Sequence[Middleware]] = None,
        ) -> None:
            pass

    class APIRouter(_CommonRouterMethodsMixin, _APIRouter):
        middleware: Optional[Sequence[Middleware]]

        @override
        def __init__(
            self,
            *,
            prefix: str = "",
            tags: Optional[List[Union[str, Enum]]] = None,
            dependencies: Optional[Sequence[params.Depends]] = None,
            default_response_class: Type[Response] = Default(JSONResponse),
            responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
            callbacks: Optional[List[BaseRoute]] = None,
            routes: Optional[List[BaseRoute]] = None,
            redirect_slashes: bool = True,
            default: Optional[ASGIApp] = None,
            dependency_overrides_provider: Optional[Any] = None,
            route_class: Type[APIRoute] = APIRoute,
            on_startup: Optional[Sequence[Callable[[], Any]]] = None,
            on_shutdown: Optional[Sequence[Callable[[], Any]]] = None,
            # the generic to Lifespan[AppType] is the type of the top level application
            # which the router cannot know statically, so we use typing.Any
            lifespan: Optional[Lifespan[Any]] = None,
            deprecated: Optional[bool] = None,
            include_in_schema: bool = True,
            generate_unique_id_function: Callable[[APIRoute], str] = Default(generate_unique_id),
            middleware: Optional[Sequence[Middleware]] = None,
        ) -> None:
            pass

    class FastAPI(_CommonRouterMethodsMixin, _FastAPI):
        pass
else:
    from fastapi import FastAPI
    from fastapi.routing import APIRoute, APIRouter, APIWebSocketRoute

__all__ = [
    "APIRoute",
    "APIRouter",
    "APIWebSocketRoute",
    "FastAPI",
]
