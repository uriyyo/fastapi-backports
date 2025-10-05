import sys
from typing import Callable, Type, TypeVar

import pytest

from fastapi_backports._backports import BaseBackporter

_T = TypeVar("_T")


def skip_if_backport_not_needed(backporter: Type[BaseBackporter]) -> Callable[[_T], _T]:
    return pytest.mark.skipif(
        not backporter.needs_backport(),
        reason=f"Backport '{backporter.label()}' is not needed in this environment",
    )


require_python_3_12 = pytest.mark.skipif(
    sys.version_info < (3, 12),
    reason="Requires Python 3.12+",
)

__all__ = [
    "require_python_3_12",
    "skip_if_backport_not_needed",
]
