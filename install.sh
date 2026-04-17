#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV="$SCRIPT_DIR/venv"
DESKTOP_FILE="$HOME/.local/share/applications/pdftools.desktop"
DESKTOP_ICON="$SCRIPT_DIR/icon.png"

echo "========================================"
echo "PDF Tools - Installazione"
echo "========================================"

if [ ! -f "$VENV/bin/python" ]; then
    echo "[1/2] Creazione virtual environment..."
    python3 -m venv "$VENV"
    "$VENV/bin/pip" install -r requirements.txt --quiet
    echo "       Fatto"
else
    echo "[1/2] Virtual environment gia esistente, skip"
fi

PYTHON="$VENV/bin/python"

if [ ! -f "$DESKTOP_FILE" ]; then
    echo "[2/2] Creazione desktop entry..."

    if [ -f "$SCRIPT_DIR/icon.ico" ] && [ ! -f "$DESKTOP_ICON" ]; then
        "$PYTHON" -c "from PIL import Image; Image.open('$SCRIPT_DIR/icon.ico').save('$DESKTOP_ICON')"
    fi

    ICON_PATH="$DESKTOP_ICON"
    [ ! -f "$ICON_PATH" ] && ICON_PATH=""

    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Name=PDF Tools
Exec=$SCRIPT_DIR/run.sh
Type=Application
Icon=$ICON_PATH
Terminal=false
Categories=Utility;
EOF

    chmod +x "$DESKTOP_FILE"
    echo "       Desktop entry creato"
else
    echo "[2/2] Desktop entry gia esistente, skip"
fi

echo "========================================"
echo "Installazione completata!"
echo "Esegui: $SCRIPT_DIR/run.sh"
echo "========================================"