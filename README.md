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

### 🔍 QUERY HTTP method support

- **Issue**: [Will FastAPI support QUERY http method? "app.query"](https://github.com/fastapi/fastapi/issues/12965)
- **Description**: Adds support for the QUERY HTTP method, allowing safe query operations with request bodies
- **Benefits**: Enables complex queries with large payloads while maintaining REST semantics

**What this fixes:**

```python
import fastapi_backports.apply  # noqa: F401

from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel

class SearchQuery(BaseModel):
    filters: dict[str, Any]
    sort_by: str | None = None
    limit: int = 100

app = FastAPI()

# ❌ Without backport: QUERY method not supported
# ✅ With backport: You can now use the QUERY HTTP method
@app.query("/search")
async def search_items(query: SearchQuery) -> dict[str, Any]:
    return {
        "results": ["item1", "item2", "item3"],
        "filters_applied": query.filters,
        "sorted_by": query.sort_by,
        "total": 150
    }

# QUERY method allows complex search parameters in request body
# while maintaining safe, idempotent semantics
# Usage: QUERY /search with JSON body containing SearchQuery data
```

### 📝 Postponed Type Annotations Support

- **Issue**: [Can't use Annotated with ForwardRef](https://github.com/fastapi/fastapi/issues/13056)
- **Description**: Fixes handling of postponed type annotations (PEP 563) and forward references in FastAPI
- **Benefits**: Enables proper type checking and dependency injection with complex type hierarchies

**What this fixes:**

```python
from __future__ import annotations

import fastapi_backports.apply  # noqa: F401

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


# Forward reference to a class defined later
def get_potato() -> Potato:
    return Potato(color='red', size=10)


# ❌ Without backport: ForwardRef causes issues with dependency injection
# ✅ With backport: Forward references work seamlessly
@app.get('/')
async def read_root(potato: Annotated[Potato, Depends(get_potato)]) -> Potato:
    return potato


@dataclass
class Potato:
    color: str
    size: int
```


### 🔄 Multiple Lifespans Support

- **Issue**: [Support multiple Lifespan in FastAPI app](https://github.com/fastapi/fastapi/discussions/9397)
- **Description**: Enables adding multiple lifespan context managers to FastAPI applications and routers
- **Benefits**: Better organization of startup/shutdown logic and modular lifespan management

**What this fixes:**

```python
from contextlib import asynccontextmanager
from typing import AsyncIterator, Any

import fastapi_backports.apply  # noqa: F401

from fastapi import FastAPI

app = FastAPI()

# ❌ Without backport: Only one lifespan context is supported
# ✅ With backport: You can add multiple lifespan contexts

@app.add_lifespan
@asynccontextmanager
async def database_lifespan(_app: FastAPI) -> AsyncIterator[dict[str, Any]]:
    print("Starting database connection")
    yield {"db": "connection"}
    print("Closing database connection")


@app.add_lifespan
@asynccontextmanager
async def cache_lifespan(_app: FastAPI) -> AsyncIterator[dict[str, Any]]:
    print("Starting cache")
    yield {"cache": "connection"}
    print("Stopping cache")

    
@app.get("/")
async def read_root():
    return {"message": "Hello World"}

# Both lifespans will be executed in order during startup/shutdown
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

> **💡 Note**: The `# noqa: F401` comment is needed to prevent linters from complaining about an "unused import". While
> the import appears unused, it actually applies the backports through side effects when imported.

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

> **⚠️ Important**: Always call `fastapi_backports.backport()` **before** creating your FastAPI application instance or
> defining any routes. The backports modify FastAPI's internal behavior and must be applied before FastAPI processes your
> route definitions.
