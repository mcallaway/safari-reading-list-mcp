#!/usr/bin/env bash
#MISE description="Run pyright type checks"

set -o pipefail
set -o nounset
set -o errexit

mise x npm:pyright -- pyright
