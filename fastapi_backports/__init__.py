from typing import TYPE_CHECKING, Any

from ._backporter import backport

if TYPE_CHECKING:
    from ._retyped import APIRoute, APIRouter, APIWebSocketRoute, FastAPI
else:

    def __getattr__(name: str) -> Any:
        from . import _retyped

        if name in _retyped.__all__:
            backport()
            return getattr(_retyped, name)

        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "APIRoute",
    "APIRouter",
    "APIWebSocketRoute",
    "FastAPI",
    "backport",
]
