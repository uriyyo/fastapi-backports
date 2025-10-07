from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, status
from fastapi.testclient import TestClient
from typing_extensions import Annotated

from fastapi_backports import FastAPI
from fastapi_backports._backports.postponed_annotations import Backporter
from tests.backports.utils import skip_if_backport_not_needed

app = FastAPI()


def get_potato() -> Potato:
    return Potato(color="red", size=10)


@app.get("/")
async def read_root(potato: Annotated[Potato, Depends(get_potato)]) -> Potato:
    return potato


@dataclass
class Potato:
    color: str
    size: int


@skip_if_backport_not_needed(Backporter)
class TestPostponedAnnotations:
    def test_postponed_annotations(self) -> None:
        with TestClient(app) as client:
            response = client.get("/")

            assert response.status_code == status.HTTP_200_OK
            assert response.json() == {"color": "red", "size": 10}
