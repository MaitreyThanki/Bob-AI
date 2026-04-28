#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment if it exists, otherwise use system python
if [ -d "$SCRIPT_DIR/bobenv" ]; then
    PYTHON_EXEC="$SCRIPT_DIR/bobenv/bin/python"
else
    PYTHON_EXEC="python3"
fi

# Check if rich is installed, if not try to install it
if ! $PYTHON_EXEC -c "import rich" &>/dev/null; then
    echo "Installing missing dependencies (rich)..."
    $PYTHON_EXEC -m pip install rich
fi

# Load .env variables if file exists
if [ -f "$SCRIPT_DIR/.env" ]; then
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
fi

# Run the TUI
$PYTHON_EXEC "$SCRIPT_DIR/bob_tui.py"
