#!/usr/bin/env bash

PYDANTIC_V2=${PYDANTIC_V2:-false}
FASTAPI_VERSION=${FASTAPI_VERSION:-"current"}
RUN_MODULE_TYPING=${RUN_MODULE_TYPING:-false}

# The module typing tests (marked "module_typing") run "ty" against the whole
# package and are version-specific, so they are excluded by default and run only
# on a dedicated job for the latest FastAPI version.
if [[ "$RUN_MODULE_TYPING" == "true" ]]; then
    PYTEST_MARKER="module_typing"
else
    PYTEST_MARKER="not module_typing"
fi

if [[ "$PYDANTIC_V2" == "true" ]]; then
    echo "Using Pydantic v2"
else
    echo "Using Pydantic v1"
    uv pip install "pydantic<2.0.0"
fi

VERSIONS_TO_TEST=()
if [[ "$FASTAPI_VERSION" == "current" ]]; then
    VERSIONS_TO_TEST+=("current")
else
    VERSIONS_TO_TEST+=("$FASTAPI_VERSION")
fi

for version in "${VERSIONS_TO_TEST[@]}"; do
    echo "Testing with FastAPI version: $version"

    if [[ "$version" != "current" ]]; then
        uv pip install "fastapi==$version"
    fi

    uv run --no-project pytest tests -m "$PYTEST_MARKER" || {
      echo "Tests failed with FastAPI version: $version"
      exit 1
    }

    echo "Tests passed with FastAPI version: $version"
done
