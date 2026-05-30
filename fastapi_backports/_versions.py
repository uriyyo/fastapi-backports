from fastapi import __version__ as fastapi_version

FASTAPI_VERSION = tuple([int(digit) for digit in fastapi_version.split(".") if digit.isdigit()])

IS_0_128_3_OR_LATER = FASTAPI_VERSION >= (0, 128, 3)

__all__ = [
    "FASTAPI_VERSION",
    "IS_0_128_3_OR_LATER",
]
