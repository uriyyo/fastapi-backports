from typing import TYPE_CHECKING, Any

from ._backporter import backport

if TYPE_CHECKING:
    from fastapi import APIRouter, FastAPI
else:

    def __getattr__(name: str) -> Any:
        if name in ("FastAPI", "APIRouter"):
            backport()

            import fastapi

            return getattr(fastapi, name)

        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")  # noqa: TRY003


__all__ = [
    "APIRouter",
    "FastAPI",
    "backport",
]
