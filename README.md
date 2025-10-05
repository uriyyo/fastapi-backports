# FastAPI Backports

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI 0.118.0+](https://img.shields.io/badge/fastapi-0.118.0+-green.svg)](https://fastapi.tiangolo.com/)

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
from dataclasses import dataclass
from fastapi_backports import FastAPI
from fastapi import Query
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
from typing import Annotated
from fastapi_backports import FastAPI
from fastapi import Depends

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

## Installation

```bash
pip install fastapi-backports
```

## Usage

### Basic Usage

Simply replace your FastAPI imports with fastapi-backports imports:

```python
# Instead of: from fastapi import FastAPI, APIRouter
from fastapi_backports import FastAPI, APIRouter

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

The backports are automatically applied when you import `FastAPI` or `APIRouter` from `fastapi_backports`.

### Manual Backport Control

You can also manually control which backports to apply:

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

You can also apply specific backports only:

```python
import fastapi_backports
from fastapi import FastAPI

# Apply only specific backports
fastapi_backports.backport(
    multiple_query_models=True,
    type_alias_type=False
)

app = FastAPI()
```

> **⚠️ Important**: When using manual backport control, always call `fastapi_backports.backport()` **before** creating your FastAPI application instance or defining any routes. The backports modify FastAPI's internal behavior and must be applied before FastAPI processes your route definitions.
