from contextlib import asynccontextmanager

from fastapi.testclient import TestClient

from fastapi_backports import APIRouter, FastAPI
from fastapi_backports._backports.lifespan_decorator import Backporter
from tests.backports.utils import skip_if_backport_not_needed


@skip_if_backport_not_needed(Backporter)
class TestLifespanDecorator:
    def test_lifespan_decorator(self):
        @asynccontextmanager
        async def base_lifespan(_: FastAPI):
            yield {"base": True}

        app = FastAPI(lifespan=base_lifespan)

        @app.add_lifespan
        @asynccontextmanager
        async def additional_lifespan(_: FastAPI):
            yield {"additional": True}

        router = APIRouter()

        @router.add_lifespan
        @asynccontextmanager
        async def router_lifespan(_: APIRouter):
            yield {"router": True}

        app.include_router(router)

        with TestClient(app) as client:
            assert client.app_state == {"base": True, "additional": True, "router": True}
