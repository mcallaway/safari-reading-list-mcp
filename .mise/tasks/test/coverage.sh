#!/usr/bin/env bash
#MISE description="Run pytest coverage."

# Check if tests directory exists
if [[ ! -d "tests" ]]; then
    echo "No tests directory found, skipping coverage."
    exit 0
fi

uv run pytest --cov-report term --cov=safari_reading_list_mcp tests/
