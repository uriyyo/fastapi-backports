import pytest
from fastapi import Depends, FastAPI, status
from starlette.testclient import TestClient
from typing_extensions import Annotated

from fastapi_backports._backports.type_alias_type import Backporter
from tests.backports.utils import require_python_3_12, skip_if_backport_not_needed

pytestmark = pytest.mark.skipif(
    not Backporter.needs_backport(),
    reason="TypeAliasType backport not needed, skipping tests",
)


@skip_if_backport_not_needed(Backporter)
@require_python_3_12
class TestTypeAliasType:
    def test_type_alias_type_backport(self) -> None:
        app = FastAPI()
        client = TestClient(app)

        async def some_value() -> int:
            assert Annotated is not None
            assert Depends is not None

            return 42

        ns = {}
        exec("type _Dependency = Annotated[int, Depends(some_value)]", globals() | {"some_value": some_value}, ns)  # noqa: S102
        _dependency = ns["_Dependency"]

        @app.get("/")
        async def read_root(value: _dependency) -> dict:
            return {"value": value}

        response = client.get("/")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"value": 42}
