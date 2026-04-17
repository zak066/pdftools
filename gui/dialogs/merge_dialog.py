from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Signal, Qt

from qfluentwidgets import (
    Dialog,
    PushButton,
    ListWidget,
    FluentIcon,
    InfoBar,
    InfoBarPosition,
)
from loguru import logger


class MergeDialog(Dialog):
    pdf_merged = Signal(str)

    def __init__(self, parent=None):
        super().__init__("Merge PDF", "Seleziona i PDF da unire:", parent)
        self._files = []
        self.setMinimumSize(500, 450)
        self._setup_ui()

    def _setup_ui(self):
        self._file_list = ListWidget()
        self._file_list.setFixedHeight(200)
        self.textLayout.addWidget(self._file_list)

        btn_layout = QHBoxLayout()

        btn_add = PushButton("Aggiungi file...", self)
        btn_add.setIcon(FluentIcon.ADD)
        btn_add.clicked.connect(self._add_files)
        btn_layout.addWidget(btn_add)

        btn_remove = PushButton("Rimuovi", self)
        btn_remove.setIcon(FluentIcon.DELETE)
        btn_remove.clicked.connect(self._remove_selected)
        btn_layout.addWidget(btn_remove)

        self.textLayout.addLayout(btn_layout)

        btn_merge = PushButton("Unisci PDF", self)
        btn_merge.setIcon(FluentIcon.SEND)
        btn_merge.setFixedWidth(150)
        btn_merge.clicked.connect(self._do_merge)
        self.textLayout.addWidget(btn_merge, alignment=Qt.AlignCenter)

        self.yesButton.setText("Chiudi")
        self.cancelButton.hide()

    def _add_files(self):
        from PySide6.QtWidgets import QFileDialog

        filters = "PDF (*.pdf)"
        files, _ = QFileDialog.getOpenFileNames(self, "Seleziona PDF", "", filters)
        for f in files:
            if f not in self._files:
                self._files.append(f)
                self._file_list.addItem(f)

    def _remove_selected(self):
        row = self._file_list.currentRow()
        if row >= 0:
            self._files.pop(row)
            self._file_list.takeItem(row)

    def _do_merge(self):
        if len(self._files) < 2:
            InfoBar.warning(
                "Attenzione",
                "Seleziona almeno 2 file PDF",
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=3000,
                parent=self,
            )
            return

        from PySide6.QtWidgets import QFileDialog

        out_path, _ = QFileDialog.getSaveFileName(
            self, "Salva PDF unito", "", "PDF (*.pdf)"
        )
        if not out_path:
            return

        try:
            from core.pdf_merge import merge_pdfs

            merge_pdfs(self._files, out_path)
            self.pdf_merged.emit(out_path)
            InfoBar.success(
                "Successo",
                "PDF uniti con successo!",
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=3000,
                parent=self,
            )
        except Exception as e:
            logger.error("Errore merge: {}", e)
            InfoBar.error(
                "Errore",
                str(e),
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=5000,
                parent=self,
            )
