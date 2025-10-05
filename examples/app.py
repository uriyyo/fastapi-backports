from typing import Annotated, Any

from fastapi import FastAPI, Query
from pydantic import BaseModel

import fastapi_backports.apply  # noqa: F401

app = FastAPI()


class UserFilters(BaseModel):
    min_age: int | None = None
    max_age: int | None = None


class GroupFilters(BaseModel):
    min_size: int | None = None
    max_size: int | None = None


type UserFiltersDependency = Annotated[
    UserFilters,
    Query(),
]

type GroupFiltersDependency = Annotated[
    GroupFilters,
    Query(),
]


@app.get("/filters")
async def get_filters(
    user_filters: UserFiltersDependency,
    group_filters: GroupFiltersDependency,
) -> dict[str, Any]:
    return {
        "user_filters": user_filters,
        "group_filters": group_filters,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
