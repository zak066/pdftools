from pathlib import Path
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap

from qfluentwidgets import FluentIcon


class DropArea(QWidget):
    pdf_dropped = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 500)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        self._label = QLabel(
            "Nessun PDF caricato\n\nUsa File → Apri (Ctrl+O)\nper caricare un PDF"
        )
        self._label.setAlignment(Qt.AlignCenter)
        self._label.setStyleSheet(
            "color: gray; font-size: 14px; border: 2px dashed #555; border-radius: 8px; padding: 20px;"
        )
        self._label.setMinimumSize(400, 500)
        layout.addWidget(self._label)

    def set_pixmap(self, pixmap: QPixmap):
        self._label.setPixmap(pixmap)
        self._label.setAlignment(Qt.AlignCenter)
        self._label.setStyleSheet("")

    def set_text(self, text: str):
        self._label.setText(text)
