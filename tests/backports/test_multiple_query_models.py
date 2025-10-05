from typing import Any, Callable

import pytest
from fastapi import APIRouter, Cookie, FastAPI, Header, Query, status
from fastapi.testclient import TestClient
from pydantic import BaseModel
from typing_extensions import Annotated

from fastapi_backports._backports.multiple_query_models import Backporter
from tests.backports.utils import skip_if_backport_not_needed


class NameModel(BaseModel):
    name: str


class AgeModel(BaseModel):
    age: int


def add_routes(
    app: FastAPI,
    in_: Callable[..., Any],
    prefix: str,
) -> None:
    router = APIRouter(prefix=prefix)

    @router.get("/models")
    async def route_models(
        name_model: Annotated[NameModel, in_()],
        age_model: Annotated[AgeModel, in_()],
    ):
        return {
            "name": name_model.name,
            "age": age_model.age,
        }

    @router.get("/mixed")
    async def route_mixed(
        name_model: Annotated[NameModel, in_()],
        age: Annotated[int, in_()],
    ):
        return {
            "name": name_model.name,
            "age": age,
        }

    app.include_router(router)


@skip_if_backport_not_needed(Backporter)
class TestMultipleQueryParams:
    @pytest.fixture
    def app(self) -> FastAPI:
        app = FastAPI()

        add_routes(app, Query, "/query")
        add_routes(app, Header, "/header")
        add_routes(app, Cookie, "/cookie")

        return app

    @pytest.fixture
    def client(self, app) -> TestClient:
        return TestClient(app)

    @pytest.mark.parametrize(
        ("in_", "prefix", "call_arg"),
        [
            (Query, "/query", "params"),
            (Header, "/header", "headers"),
            (Cookie, "/cookie", "cookies"),
        ],
        ids=[
            "query",
            "header",
            "cookie",
        ],
    )
    @pytest.mark.parametrize(
        "type_",
        [
            "models",
            "mixed",
        ],
        ids=[
            "models",
            "mixed",
        ],
    )
    def test_multiple_params(self, client, in_, prefix, call_arg, type_):
        params = {"name": "John", "age": "42"}
        kwargs = {}

        if call_arg == "cookies":
            client.cookies = params
        else:
            kwargs[call_arg] = params

        response = client.get(f"{prefix}/{type_}", **kwargs)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"name": "John", "age": 42}

    @pytest.mark.parametrize(
        ("prefix", "in_"),
        [
            ("/query", "query"),
            ("/header", "header"),
            ("/cookie", "cookie"),
        ],
        ids=[
            "query",
            "header",
            "cookie",
        ],
    )
    @pytest.mark.parametrize(
        "type_",
        [
            "models",
            "mixed",
        ],
        ids=[
            "models",
            "mixed",
        ],
    )
    def test_openapi_schema(self, client, prefix, in_, type_):
        response = client.get("/openapi.json")

        assert response.status_code == status.HTTP_200_OK

        schema = response.json()
        assert schema["paths"][f"{prefix}/{type_}"]["get"]["parameters"] == [
            {
                "required": True,
                "in": in_,
                "name": "name",
                "schema": {"title": "Name", "type": "string"},
            },
            {
                "required": True,
                "in": in_,
                "name": "age",
                "schema": {"title": "Age", "type": "integer"},
            },
        ]
