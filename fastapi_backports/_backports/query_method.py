from typing import Callable

from fastapi import APIRouter as _APIRouter
from fastapi import FastAPI as _FastAPI
from fastapi.openapi.constants import METHODS_WITH_BODY
from fastapi.types import DecoratedCallable

from ._base import BaseBackporter


class _APIRouterWithQueryMethod(_APIRouter):
    def query(self, path, **kwargs) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(path, methods=["QUERY"], **kwargs)


class _FastAPIWithQueryMethod(_FastAPI):
    def query(self, path, **kwargs) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.router.query(path, **kwargs)


# TODO: Wait for https://github.com/swagger-api/swagger-ui/issues/10575 to be resolved
# and then add OpenAPI support for QUERY method
class QueryMethodBackporter(BaseBackporter):
    @classmethod
    def label(cls) -> str:
        return "issues/12965"

    @classmethod
    def backport(cls) -> None:
        _FastAPI.query = _FastAPIWithQueryMethod.query  # type: ignore[assignment]
        _APIRouter.query = _APIRouterWithQueryMethod.query  # type: ignore[assignment]

        METHODS_WITH_BODY.add("QUERY")


__all__ = [
    "QueryMethodBackporter",
]
