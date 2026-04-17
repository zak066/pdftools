import traceback
from loguru import logger
import sys


def setup_exceptions():
    """Setup global exception handler."""
    sys.excepthook = exception_handler


def exception_handler(exc_type, exc_value, exc_traceback):
    """Handle uncaught exceptions."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception: {}", exc_value)
    logger.trace("".join(("".join(traceback.format_tb(exc_traceback)))))

    from PySide6.QtWidgets import QMessageBox

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(str(exc_value))
    msg.setWindowTitle("Error")
    msg.exec()
