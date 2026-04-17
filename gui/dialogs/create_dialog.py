from pathlib import Path
from PySide6.QtWidgets import QVBoxLayout, QLabel
from PySide6.QtCore import Signal, Qt

from qfluentwidgets import (
    Dialog,
    PushButton,
    FluentIcon,
    InfoBar,
    InfoBarPosition,
)
from loguru import logger

from converters.txt_to_pdf import convert as convert_txt
from converters.docx_to_pdf import convert as convert_docx
from converters.odt_to_pdf import convert as convert_odt
from converters.xlsx_to_pdf import convert as convert_xlsx
from converters.csv_to_pdf import convert as convert_csv


class CreateDialog(Dialog):
    file_created = Signal(str)

    def __init__(self, parent=None):
        super().__init__("Crea PDF", "Seleziona un file da convertire in PDF:", parent)
        self.setMinimumWidth(450)
        self._setup_ui()

    def _setup_ui(self):
        btn = PushButton("Seleziona File...", self)
        btn.setIcon(FluentIcon.FOLDER)
        btn.setFixedWidth(200)
        btn.clicked.connect(self._select_file)
        self.textLayout.addWidget(btn, alignment=Qt.AlignCenter)

        self.yesButton.setText("Chiudi")
        self.cancelButton.hide()

    def _select_file(self):
        from PySide6.QtWidgets import QFileDialog

        filters = (
            "File supportati (*.txt *.docx *.odt *.xlsx *.xls *.csv);;"
            "File di testo (*.txt);;"
            "Documenti Word (*.docx);;"
            "Documenti LibreOffice (*.odt);;"
            "File Excel (*.xlsx *.xls);;"
            "File CSV (*.csv);;"
            "Tutti i file (*.*)"
        )
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleziona file", "", filters)
        if file_path:
            logger.info("File selezionato: {}", file_path)
            self._convert_file(file_path)

    def _convert_file(self, file_path: str):
        src = Path(file_path)
        output_path = str(src.with_suffix(".pdf"))

        try:
            converters = {
                ".txt": convert_txt,
                ".docx": convert_docx,
                ".odt": convert_odt,
                ".xlsx": convert_xlsx,
                ".xls": convert_xlsx,
                ".csv": convert_csv,
            }

            ext = src.suffix.lower()
            if ext not in converters:
                logger.warning("Formato non supportato: {}", ext)
                return

            converters[ext](file_path, output_path)
            self.file_created.emit(output_path)
            InfoBar.success(
                "Successo",
                f"PDF creato: {output_path}",
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=3000,
                parent=self.parent(),
            )
        except Exception as e:
            logger.error("Errore conversione: {}", e)
            InfoBar.error(
                "Errore",
                str(e),
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=5000,
                parent=self.parent(),
            )
