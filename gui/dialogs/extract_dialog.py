from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Signal, Qt

from qfluentwidgets import (
    Dialog,
    PushButton,
    LineEdit,
    FluentIcon,
    InfoBar,
    InfoBarPosition,
    CaptionLabel,
)
from loguru import logger


class ExtractDialog(Dialog):
    pages_extracted = Signal(str)

    def __init__(self, parent=None):
        super().__init__(
            "Estrai Pagine", "Seleziona un PDF e le pagine da estrarre:", parent
        )
        self.setMinimumSize(450, 300)
        self._setup_ui()

    def _setup_ui(self):
        self._file_input = LineEdit()
        self._file_input.setReadOnly(True)
        self._file_input.setPlaceholderText("Nessun file selezionato")
        self.textLayout.addWidget(self._file_input)

        btn_select = PushButton("Seleziona file...", self)
        btn_select.setIcon(FluentIcon.FOLDER)
        btn_select.clicked.connect(self._select_file)
        self.textLayout.addWidget(btn_select, alignment=Qt.AlignCenter)

        self.textLayout.addWidget(CaptionLabel("Pagine da estrarre (es: 1,3-5,7):"))

        self._pages_input = LineEdit()
        self._pages_input.setPlaceholderText("1,3-5,7")
        self.textLayout.addWidget(self._pages_input)

        btn_extract = PushButton("Estrai pagine", self)
        btn_extract.setIcon(FluentIcon.COPY)
        btn_extract.setFixedWidth(150)
        btn_extract.clicked.connect(self._do_extract)
        self.textLayout.addWidget(btn_extract, alignment=Qt.AlignCenter)

        self.yesButton.setText("Chiudi")
        self.cancelButton.hide()

    def _select_file(self):
        from PySide6.QtWidgets import QFileDialog

        filters = "PDF (*.pdf)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleziona PDF", "", filters)
        if file_path:
            self._file_input.setText(file_path)

    def _do_extract(self):
        file_path = self._file_input.text()
        if not file_path:
            InfoBar.warning(
                "Attenzione",
                "Seleziona un file PDF",
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=3000,
                parent=self,
            )
            return

        pages = self._pages_input.text().strip()
        if not pages:
            InfoBar.warning(
                "Attenzione",
                "Inserisci le pagine da estrarre",
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=3000,
                parent=self,
            )
            return

        from PySide6.QtWidgets import QFileDialog

        out_path, _ = QFileDialog.getSaveFileName(self, "Salva PDF", "", "PDF (*.pdf)")
        if not out_path:
            return

        try:
            from core.pdf_extract import extract_pages

            extract_pages(file_path, out_path, pages)
            self.pages_extracted.emit(out_path)
            InfoBar.success(
                "Successo",
                "Pagine estratte con successo!",
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=3000,
                parent=self,
            )
        except Exception as e:
            logger.error("Errore estrazione: {}", e)
            InfoBar.error(
                "Errore",
                str(e),
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=5000,
                parent=self,
            )
