#!/usr/bin/env bash

PYDANTIC_V2=${PYDANTIC_V2:-false}
FASTAPI_VERSION=${FASTAPI_VERSION:-"current"}

if [[ "$PYDANTIC_V2" == "true" ]]; then
    echo "Using Pydantic v2"
else
    echo "Using Pydantic v1"
    uv pip install "pydantic<2.0.0"
fi

VERSIONS_TO_TEST=()
if [[ "$FASTAPI_VERSION" == "current" ]]; then
    VERSIONS_TO_TEST+=("current")
elif [[ "$FASTAPI_VERSION" == "all" ]]; then
    VERSIONS_TO_TEST+=(
      "0.136.1"
    )
else
    VERSIONS_TO_TEST+=("$FASTAPI_VERSION")
fi

for version in "${VERSIONS_TO_TEST[@]}"; do
    echo "Testing with FastAPI version: $version"

    if [[ "$version" != "current" ]]; then
        uv pip install "fastapi==$version"
    fi

    uv run --no-project pytest tests || {
      echo "Tests failed with FastAPI version: $version"
      exit 1
    }

    echo "Tests passed with FastAPI version: $version"
done
