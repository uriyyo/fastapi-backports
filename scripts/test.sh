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
      "0.118.0"
      "0.117.1"
      "0.117.0"
      "0.116.1"
      "0.116.0"
      "0.115.14"
      "0.115.13"
      "0.115.12"
      "0.115.11"
      "0.115.10"
      "0.115.9"
      "0.115.8"
      "0.115.7"
      "0.115.6"
      "0.115.5"
      "0.115.4"
      "0.115.3"
      "0.115.2"
      "0.115.1"
      "0.115.0"
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
