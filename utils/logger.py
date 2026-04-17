import sys
import os
from pathlib import Path
from loguru import logger


def setup_logger():
    """Configure application logger."""
    logger.remove()

    # Per app windowed, stderr potrebbe essere None
    if sys.stderr is not None and hasattr(sys, "stderr") and sys.stderr:
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
            level="INFO",
        )

    # Determina la directory dei log
    # Per PyInstaller, usa la directory accanto all'exe
    if getattr(sys, "frozen", False):
        # L'app è in freeze (exe compilato)
        app_dir = Path(sys.executable).parent
    else:
        # L'app è in modalità Python normale
        app_dir = Path.home() / ".pdftools"

    log_dir = app_dir / ".pdftools"
    log_dir.mkdir(parents=True, exist_ok=True)

    logger.add(
        log_dir / "pdftools.log",
        rotation="10 MB",
        retention="7 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    )

    logger.info("Logger initialized - log file: {}", log_dir / "pdftools.log")
