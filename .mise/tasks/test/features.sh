#!/usr/bin/env bash
#MISE description="Run pytest with feature coverage report."

if [[ ! -d "tests" ]]; then
    echo "No tests directory found, skipping feature coverage."
    exit 0
fi

uv run pytest --feature-coverage tests/
