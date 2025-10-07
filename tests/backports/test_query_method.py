import pytest
from fastapi import Body, status
from starlette.testclient import TestClient
from typing_extensions import Annotated

from fastapi_backports import APIRouter, FastAPI
from fastapi_backports._backports.query_method import Backporter
from tests.backports.utils import skip_if_backport_not_needed


@skip_if_backport_not_needed(Backporter)
class TestQueryMethod:
    @pytest.fixture
    def app(self):
        return FastAPI()

    @pytest.fixture
    def client(self, app):
        return TestClient(app)

    @pytest.mark.parametrize("path", ["/app", "/router"])
    def test_query_method(self, app, client, path):
        @app.query("/app")
        async def app_route(param: Annotated[int, Body(..., embed=True)]):
            return {"param": param}

        router = APIRouter()

        @router.query("/router")
        async def router_route(param: Annotated[int, Body(..., embed=True)]):
            return {"param": param}

        app.include_router(router)

        response = client.request("QUERY", path, json={"param": 42})
        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json() == {"param": 42}
