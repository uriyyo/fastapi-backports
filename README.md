# FastAPI Backports

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI 0.115.0+](https://img.shields.io/badge/fastapi-0.115.0+-green.svg)](https://fastapi.tiangolo.com/)

A Python library that provides backports for FastAPI features, allowing you to use newer FastAPI functionality on older
versions.

## Features

This library includes backports for:

### 🔄 Multiple Query Models Support

- **Issue**: [Support multiple Query() in a single endpoint](https://github.com/fastapi/fastapi/discussions/12212)
- **Description**: Enables using multiple Pydantic models as query parameters in a single FastAPI endpoint
- **Benefits**: Better organization of query parameters and improved API design

**What this fixes:**

```python
import fastapi_backports.apply  # noqa: F401

from dataclasses import dataclass
from fastapi import Query, FastAPI
from typing import Annotated, Any

@dataclass
class FilterParams:
    category: str | None = None
    min_price: float | None = None

@dataclass
class PaginationParams:
    page: int = 1
    size: int = 10

app = FastAPI()

# ❌ Without backport: This would not work as expected
@app.get("/items")
async def get_items(
    filters: Annotated[FilterParams, Query()],
    pagination: Annotated[PaginationParams, Query()],
) -> dict[str, Any]:
    return {"filters": filters, "pagination": pagination}


# ✅ With backport: This works perfectly!
# Query parameters are properly flattened and validated
# Example: /items?category=electronics&min_price=10&page=2&size=20
```

### 🏷️ PEP 695 Type Alias Support

- **Issue**: [Annotated dependencies are interpreted incorrectly when using PEP 695-style type alias](https://github.com/fastapi/fastapi/issues/10719)
- **Description**: Fixes handling of modern Python type aliases (PEP 695) in FastAPI dependencies
- **Benefits**: Full compatibility with modern Python typing features

**What this fixes:**

```python
import fastapi_backports.apply  # noqa: F401

from typing import Annotated
from fastapi import Depends, FastAPI

async def get_current_user_id() -> int:
    return 123

# PEP 695 style type alias (Python 3.12+)
type UserId = Annotated[int, Depends(get_current_user_id)]


app = FastAPI()

# ❌ Without backport: FastAPI doesn't recognize the type alias properly
# ✅ With backport: Type aliases work seamlessly in dependencies
@app.get("/users/{user_id}")
async def get_user(user_id: UserId):
    return {"user_id": user_id}
```

### 🕵️ Add middleware parameter to APIRouter

- **Issue**: [Add middleware parameter to APIRouter](https://github.com/fastapi/fastapi/pull/11010)
- **Description**: Enables adding middleware directly to APIRouter instances and individual routes
- **Benefits**: Better middleware organization and route-specific middleware support

**What this fixes:**

```python
import fastapi_backports.apply  # noqa: F401

from typing import Any

from fastapi_backports import FastAPI, APIRouter
from fastapi import Request
from fastapi.middleware import Middleware
from starlette.types import ASGIApp, Receive, Scope, Send


def add_header_middleware(_app: ASGIApp, header_name: str, header_value: str) -> ASGIApp:
    async def _middleware(scope: Scope, receive: Receive, send: Send) -> None:
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = message.setdefault("headers", [])
                headers.append((header_name.encode(), header_value.encode()))
            await send(message)

        await _app(scope, receive, send_wrapper)

    return _middleware


app = FastAPI()

# ❌ Without backport: APIRouter doesn't accept middleware parameter
# ✅ With backport: You can now add middleware to routers
router = APIRouter(
    prefix="/api/v1",
    middleware=[
        Middleware(add_header_middleware, header_name="X-Custom-Header", header_value="Value")
    ]
)


@router.get("/items")
async def get_items() -> dict[str, Any]:
    return {"items": ["item1", "item2"]}


# Middleware will be applied to all routes in this router
app.include_router(router)
```

## Installation

```bash
pip install fastapi-backports
```

## Usage

### Basic Usage

Import the backport module before using FastAPI:

```python
import fastapi_backports.apply  # noqa: F401
from fastapi import FastAPI, APIRouter

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

The backports are automatically applied when you import `fastapi_backports.apply`.

> **💡 Note**: The `# noqa: F401` comment is needed to prevent linters from complaining about an "unused import". While the import appears unused, it actually applies the backports through side effects when imported.

### Manual Backport Control

For more control over when backports are applied:

```python
import fastapi_backports
from fastapi import FastAPI

# ⚠️ IMPORTANT: Apply backports BEFORE creating FastAPI app or routes
fastapi_backports.backport()

# Now create your app
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

> **⚠️ Important**: Always call `fastapi_backports.backport()` **before** creating your FastAPI application instance or defining any routes. The backports modify FastAPI's internal behavior and must be applied before FastAPI processes your route definitions.
