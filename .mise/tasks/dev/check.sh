#!/usr/bin/env bash
#MISE description="Ensure dev dependencies are present."

for TOOL in git mise uv python; do
    if ! command -v $TOOL > /dev/null; then
        echo "Missing tool: $TOOL"
        exit 1
    fi
done

if [[ ! -f pyproject.toml ]]; then
    echo "Error: pyproject.toml not found in the current directory."
    exit 1
fi

# Check for virtualenv directory
VIRTUAL_ENV=.venv
if [[ ! -d "$VIRTUAL_ENV" ]]; then
    echo "Error: virtualenv directory is missing."
    echo "VIRTUAL_ENV=$VIRTUAL_ENV"
    exit 1
fi

echo -n "Python is: "
which python
python --version
echo -n "UV is: "
which uv
uv --version
echo "Virtual env is: $VIRTUAL_ENV"

echo
echo "All tools found. Environment is ready."
