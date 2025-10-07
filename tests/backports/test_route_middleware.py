import pytest
from fastapi import WebSocket, status
from fastapi.testclient import TestClient
from starlette.middleware import Middleware
from starlette.types import ASGIApp

from fastapi_backports import APIRouter, FastAPI
from fastapi_backports._backports.route_middleware import Backporter
from tests.backports.utils import skip_if_backport_not_needed


def _add_header_middleware(app: ASGIApp, header_name: str, header_value: str) -> ASGIApp:
    async def middleware(scope, receive, send):
        async def _send(message):
            if message["type"] == "http.response.start":
                headers = message.setdefault("headers", [])
                headers.append((header_name.encode(), header_value.encode()))
            await send(message)

        await app(scope, receive, _send)

    return middleware


@skip_if_backport_not_needed(Backporter)
class TestRouteBackport:
    @pytest.fixture
    def app(self):
        return FastAPI()

    @pytest.fixture
    def client(self, app):
        return TestClient(app)

    @pytest.mark.parametrize("path", ["/path1", "/path2"])
    @pytest.mark.parametrize("method", ["get", "post", "put", "delete", "patch", "options", "head", "trace"])
    def test_route_middleware_base(self, app, client, path, method):
        router = APIRouter(
            middleware=[Middleware(_add_header_middleware, "x-outer-middleware", "outer")],
        )

        decorator = getattr(router, method)

        @decorator(
            "/path1",
            middleware=[Middleware(_add_header_middleware, "x-inner-middleware", "inner")],
        )
        async def route():
            return {"message": "Hello, World!"}

        router.add_api_route(
            "/path2",
            route,
            methods=[method.upper()],
            middleware=[Middleware(_add_header_middleware, "x-inner-middleware", "inner")],
        )

        app.include_router(router)

        response = client.request(method, path)
        assert response.status_code == status.HTTP_200_OK

        if method == "head":
            assert response.content == b""
        else:
            assert response.json() == {"message": "Hello, World!"}

        assert response.headers.get("x-inner-middleware") == "inner"
        assert response.headers.get("x-outer-middleware") == "outer"

    def test_route_middleware_ordering(self, app, client):
        async def route():
            return {"message": "Hello, World!"}

        child_router = APIRouter(
            middleware=[Middleware(_add_header_middleware, "x-where", "child-router")],
        )

        child_router.add_api_route(
            "/",
            route,
            methods=["GET"],
            middleware=[Middleware(_add_header_middleware, "x-where", "route")],
        )

        parent_router = APIRouter(
            middleware=[Middleware(_add_header_middleware, "x-where", "parent-router")],
        )

        parent_router.include_router(
            child_router,
            middleware=[Middleware(_add_header_middleware, "x-where", "included-router")],
        )

        app.include_router(
            parent_router,
            middleware=[Middleware(_add_header_middleware, "x-where", "app-router")],
        )

        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Hello, World!"}
        assert response.headers.get("x-where") == "route, child-router, included-router, parent-router, app-router"

    @pytest.mark.parametrize("path", ["/ws1", "/ws2"])
    def test_websocket_route_middleware(self, app, client, path):
        router = APIRouter(
            middleware=[Middleware(_add_header_middleware, "x-outer-middleware", "outer")],
        )

        @router.websocket(
            "/ws1",
            middleware=[Middleware(_add_header_middleware, "x-inner-middleware", "inner")],
        )
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            await websocket.send_json({"message": "Hello, WebSocket!"})
            await websocket.close()

        router.add_api_websocket_route(
            "/ws2",
            websocket_endpoint,
            middleware=[Middleware(_add_header_middleware, "x-inner-middleware", "inner")],
        )

        app.include_router(router)

        with client.websocket_connect(path) as websocket:
            data = websocket.receive_json()
            assert data == {"message": "Hello, WebSocket!"}
