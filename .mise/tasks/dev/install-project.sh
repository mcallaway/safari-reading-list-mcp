#!/usr/bin/env bash
#MISE description="Install this project with 'uv sync'."

set -o pipefail
set -o nounset
set -o errexit

echo "Installing project dependencies with uv sync..."
uv sync

echo "Installing project in editable mode..."
uv pip install -e .

echo "✓ Project installation complete"
