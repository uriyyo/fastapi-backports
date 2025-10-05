from ._backporter import backport

backport()

FASTAPI_BACKPORTED = True

__all__ = [
    "FASTAPI_BACKPORTED",
]
