from abc import abstractmethod
from typing import Optional, Tuple

from fastapi import __version__
from typing_extensions import Protocol

FASTAPI_VERSION = tuple(int(part) if part.isdigit() else 0 for part in __version__.split(".")[:3])


class BaseBackporter(Protocol):
    @classmethod
    def fixed_in_version(cls) -> Optional[Tuple[int, ...]]:
        return None

    @classmethod
    def needs_backport(cls) -> bool:
        fixed_in = cls.fixed_in_version()

        if fixed_in and fixed_in <= FASTAPI_VERSION:  # noqa: SIM103
            return False

        return True

    @classmethod
    @abstractmethod
    def label(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def backport(cls) -> None:
        pass


__all__ = [
    "BaseBackporter",
]
