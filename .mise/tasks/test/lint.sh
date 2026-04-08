#!/usr/bin/env bash
#MISE description="Run ruff linter"

set -e

echo "Running ruff check..."
uv run ruff check .
