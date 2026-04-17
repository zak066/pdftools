import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt
from loguru import logger

from gui.main_window import MainWindow
from gui.theme import apply_theme
from utils.logger import setup_logger
from utils.exceptions import setup_exceptions


class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        setup_logger()
        setup_exceptions()

        self.setApplicationName("PDF Tools")
        self.setApplicationVersion("1.0.0")
        self.setOrganizationName("PDF Tools")

        apply_theme()

        self._main_window = None
        logger.info("Application initialized")

    def exec(self):
        self._main_window = MainWindow()
        self._main_window.show()
        logger.info("Main window displayed")
        return super().exec()

    def critical_error(self, title: str, message: str):
        logger.critical(f"{title}: {message}")
        QMessageBox.critical(None, title, message)
        sys.exit(1)


app_instance = None


def get_app() -> Application:
    global app_instance
    if app_instance is None:
        app_instance = Application(sys.argv)
    return app_instance
