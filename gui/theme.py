"""Theme and styling configuration for Fluent UI."""

import json
from pathlib import Path
from qfluentwidgets import setTheme, Theme, setThemeColor

CONFIG_FILE = Path.home() / ".pdftools" / "theme.json"


def load_theme_preference() -> Theme:
    """Load saved theme preference."""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return Theme(data.get("theme", "Light"))
    except Exception:
        pass
    return Theme.LIGHT


def save_theme_preference(theme: Theme):
    """Save theme preference."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"theme": theme.value}, f)


def toggle_theme():
    """Toggle between Light and Dark theme."""
    current = load_theme_preference()
    new_theme = Theme.DARK if current == Theme.LIGHT else Theme.LIGHT
    setTheme(new_theme)
    save_theme_preference(new_theme)
    return new_theme


def apply_theme():
    """Apply Fluent UI theme to the application."""
    theme = load_theme_preference()
    setTheme(theme)
    setThemeColor("#0078D4")
