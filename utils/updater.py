import json
import os
import sys
from typing import Optional
import urllib.request
from pathlib import Path
from loguru import logger

DEFAULT_UPDATE_URL = os.environ.get(
    "PDFTOOLS_UPDATE_URL", "https://api.github.com/repos/user/pdftools/releases/latest"
)
current_version = "1.0.1"


def get_config_path() -> Path:
    """Get config file path - check multiple locations."""
    app_data = os.environ.get("APPDATA", "")
    config_locations = [
        Path(app_data) / "pdftools" / "config.json" if app_data else None,
        Path(sys.executable).parent / "config.json"
        if getattr(sys, "frozen", False)
        else None,
        Path("config.json"),
    ]

    for loc in config_locations:
        if loc and loc.exists():
            return loc

    for loc in config_locations:
        if loc:
            return loc

    return Path("config.json")


def get_update_url() -> str:
    """Get update URL from env var, config, or default."""
    env_url = os.environ.get("PDFTOOLS_UPDATE_URL")
    if env_url:
        logger.info("Using update URL from environment: {}", env_url)
        return env_url

    config_path = get_config_path()
    try:
        if config_path.exists():
            with open(config_path, "r") as f:
                config = json.load(f)
                url = config.get("update_url")
                if url:
                    logger.info("Using update URL from config: {}", url)
                    return url
    except Exception as e:
        logger.warning("Error reading config: {}", e)

    logger.info("Using default update URL: {}", DEFAULT_UPDATE_URL)
    return DEFAULT_UPDATE_URL


def check_for_updates(silent: bool = False) -> Optional[dict]:
    """Check for updates from server.

    Args:
        silent: If True, don't log errors (for startup check)

    Returns:
        dict with update info or None if no update available
    """
    url = get_update_url()

    try:
        timeout = 5 if silent else 10
        with urllib.request.urlopen(url, timeout=timeout) as response:
            data = json.load(response)

        new_version = data.get("version", "") or data.get("tag_name", "").lstrip("v")

        if new_version and new_version != current_version:
            logger.info("Update available: {} -> {}", current_version, new_version)
            return data
        else:
            logger.info("Already on latest version: {}", current_version)
            return None

    except Exception as e:
        if not silent:
            logger.error("Error checking for updates: {}", e)
        return None


def download_update(url: str, dest_path: Optional[str] = None) -> Optional[str]:
    """Download update.

    Args:
        url: URL to download the update from.
        dest_path: Where to save - default: temp directory under APPDATA.

    Returns:
        Path to downloaded file or None on error.
    """
    if dest_path is None:
        app_data = os.environ.get("APPDATA", "")
        if app_data:
            update_dir = Path(app_data) / "pdftools" / "update"
            update_dir.mkdir(parents=True, exist_ok=True)
            dest_path = str(update_dir / "pdftools_update.exe")
        else:
            dest_path = "pdftools_update.exe"

    try:
        logger.info("Downloading update from: {}", url)

        with urllib.request.urlopen(url, timeout=60) as response:
            total_size = int(response.headers.get("Content-Length", 0))
            downloaded = 0

            with open(dest_path, "wb") as f:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)

                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        logger.info("Downloaded: {:.1f}%", percent)

        logger.info("Update downloaded to: {}", dest_path)
        return dest_path

    except Exception as e:
        logger.error("Error downloading update: {}", e)
        return None


def get_version() -> str:
    """Get current version."""
    return current_version


def set_version(version: str) -> None:
    """Set current version (for testing or config)."""
    global current_version
    current_version = version
