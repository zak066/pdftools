#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV="$SCRIPT_DIR/venv"

if [ ! -f "$VENV/bin/python" ]; then
    echo "Prima esegui: ./install.sh"
    exit 1
fi

exec "$VENV/bin/python" "$SCRIPT_DIR/main.py"