from fastapi import APIRouter as _APIRouter
from fastapi import FastAPI as _FastAPI
from fastapi.routing import _merge_lifespan_context
from starlette.types import Lifespan

from ._base import BaseBackporter


class _APIRouterWithLifespan(_APIRouter):
    def add_lifespan(self, lifespan: Lifespan) -> Lifespan:
        self.lifespan_context = _merge_lifespan_context(
            self.lifespan_context,
            lifespan,
        )
        return lifespan


class _FastAPIWithLifespan(_FastAPI):
    def add_lifespan(self, lifespan: Lifespan) -> Lifespan:
        return self.router.add_lifespan(lifespan)


class Backporter(BaseBackporter):
    @classmethod
    def label(cls) -> str:
        return "lifespan_decorator"

    @classmethod
    def backport(cls) -> None:
        _APIRouter.add_lifespan = _APIRouterWithLifespan.add_lifespan  # type: ignore[unresolved-attribute]
        _FastAPI.add_lifespan = _FastAPIWithLifespan.add_lifespan  # type: ignore[unresolved-attribute]


__all__ = [
    "Backporter",
]
