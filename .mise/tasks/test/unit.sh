#!/usr/bin/env bash
#MISE description="Run pytest on 'unit' tests."
#MISE depends=["test:lint"]

# Check if tests directory exists
if [[ ! -d "tests" ]]; then
    echo "No tests directory found, skipping unit tests."
    exit 0
fi

# Run Python unit tests
uv run pytest -sv --log-cli-level=WARN -W error::UserWarning tests/
