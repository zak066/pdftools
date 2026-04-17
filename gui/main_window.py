from pathlib import Path
from typing import Optional
from PySide6.QtWidgets import (
    QWidget,
    QFileDialog,
    QHBoxLayout,
    QSplitter,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt

from qfluentwidgets import (
    FluentWindow,
    NavigationItemPosition,
    InfoBar,
    InfoBarPosition,
    MessageBox,
    CommandBar,
    Action,
    FluentIcon,
    Theme,
    setFont,
)

from gui.widgets.pdf_sidebar import PDFSidebar
from gui.widgets.pdf_preview import PDFPreview
from gui.dialogs.merge_dialog import MergeDialog
from gui.dialogs.extract_dialog import ExtractDialog
from gui.dialogs.create_dialog import CreateDialog
from gui.theme import toggle_theme
from core.pdf_split import split_pdf
from utils.updater import get_version
from loguru import logger
from config import (
    SIDEBAR_WIDTH,
    PREVIEW_MAX_WIDTH,
    MIN_WINDOW_WIDTH,
    MIN_WINDOW_HEIGHT,
)

# Import converters
from converters.txt_to_pdf import convert as convert_txt
from converters.docx_to_pdf import convert as convert_docx
from converters.odt_to_pdf import convert as convert_odt
from converters.xlsx_to_pdf import convert as convert_xlsx
from converters.csv_to_pdf import convert as convert_csv

# Map of converters for dynamic lookup
CONVERTERS = {
    "txt": convert_txt,
    "docx": convert_docx,
    "odt": convert_odt,
    "xls": convert_xlsx,
    "csv": convert_csv,
}

# File type info
FILE_TYPES = {
    "txt": ("File di testo (*.txt)", ".txt"),
    "docx": ("Documenti Word (*.docx)", ".docx"),
    "odt": ("Documenti LibreOffice (*.odt)", ".odt"),
    "xls": ("File Excel (*.xlsx *.xls)", ".xlsx"),
    "csv": ("File CSV (*.csv)", ".csv"),
}


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self._current_pdf_path: Optional[str] = None
        self._setup_window()
        self._setup_ui()
        self._setup_toolbar()
        self._setup_navigation()
        logger.info("Main window created")

    def _setup_window(self):
        self.setWindowTitle("PDF Tools")
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self.resize(1200, 800)
        self.titleBar.titleLabel.hide()

    def _setup_ui(self):
        wrapper = QWidget()
        wrapper.setObjectName("homeWidget")

        main_layout = QVBoxLayout(wrapper)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._home_widget = QWidget()
        content_layout = QHBoxLayout(self._home_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self._sidebar = PDFSidebar()
        self._sidebar.setMinimumWidth(100)
        self._sidebar.setMaximumWidth(400)
        self._sidebar.page_selected.connect(self._on_page_selected)
        self._sidebar.pages_selected.connect(self._on_pages_selected)

        self._preview = PDFPreview()
        self._preview.pdf_dropped.connect(self._on_pdf_dropped)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self._sidebar)
        splitter.addWidget(self._preview)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([SIDEBAR_WIDTH, MIN_WINDOW_WIDTH - SIDEBAR_WIDTH])
        content_layout.addWidget(splitter)

        main_layout.addWidget(self._home_widget)

        self._status = QLabel()
        self._status.setFixedHeight(22)
        self._status.setStyleSheet(
            "QLabel { background: #f5f5f5; border-top: 1px solid #e0e0e0; "
            "padding: 0px 8px; color: #666; font-size: 11px; }"
        )
        self._status.setText(f"  Pronto - v{get_version()}")
        main_layout.addWidget(self._status)

        self.addSubInterface(wrapper, FluentIcon.HOME, "Home")

    def _setup_toolbar(self):
        self._app_title = QLabel("PDF Tools")
        self._app_title.setStyleSheet(
            "QLabel { font-size: 14px; font-weight: bold; padding: 0px 12px; }"
        )

        self.commandBar = CommandBar(self)
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.commandBar.setFixedHeight(48)

        self.commandBar.addAction(
            Action(
                FluentIcon.FOLDER,
                "Apri",
                triggered=self._on_open_pdf,
                shortcut="Ctrl+O",
            )
        )
        self.commandBar.addAction(
            Action(
                FluentIcon.SAVE, "Salva", triggered=self._on_save_pdf, shortcut="Ctrl+S"
            )
        )
        self.commandBar.addSeparator()
        self.commandBar.addAction(
            Action(
                FluentIcon.ADD,
                "Crea PDF",
                triggered=self._on_create_pdf,
                shortcut="Ctrl+N",
            )
        )
        self.commandBar.addAction(
            Action(
                FluentIcon.SEND,
                "Merge",
                triggered=self._on_merge_pdf,
                shortcut="Ctrl+M",
            )
        )
        self.commandBar.addAction(
            Action(
                FluentIcon.COPY,
                "Estrai",
                triggered=self._on_extract_selected,
                shortcut="Ctrl+E",
            )
        )
        self.commandBar.addAction(
            Action(
                FluentIcon.CUT,
                "Dividi",
                triggered=self._on_split_pdf,
                shortcut="Ctrl+D",
            )
        )
        self.commandBar.addSeparator()
        self.commandBar.addAction(
            Action(
                FluentIcon.DELETE,
                "Elimina",
                triggered=self._on_delete_selected,
                shortcut="Del",
            )
        )
        self.commandBar.addAction(
            Action(FluentIcon.ROTATE, "Ruota +90", triggered=self._on_rotate_cw)
        )
        self.commandBar.addAction(
            Action(FluentIcon.ROTATE, "Ruota -90", triggered=self._on_rotate_ccw)
        )
        self.commandBar.addSeparator()
        self.commandBar.addAction(
            Action(
                FluentIcon.UP, "Sposta su", triggered=self._on_move_up, shortcut="PgUp"
            )
        )
        self.commandBar.addAction(
            Action(
                FluentIcon.DOWN,
                "Sposta giu",
                triggered=self._on_move_down,
                shortcut="PgDown",
            )
        )

        self.titleBar.hBoxLayout.insertWidget(0, self._app_title, 0)
        self.titleBar.hBoxLayout.insertWidget(1, self.commandBar, 1)
        self.titleBar.hBoxLayout.insertSpacing(2, 10)

    def _setup_navigation(self):
        self.navigationInterface.addItem(
            routeKey="settings",
            icon=FluentIcon.SETTING,
            text="Impostazioni",
            onClick=self._on_settings,
            position=NavigationItemPosition.BOTTOM,
        )

    def _show_info(self, title: str, message: str, is_success: bool = True):
        if is_success:
            InfoBar.success(
                title,
                message,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=3000,
                parent=self,
            )
        else:
            InfoBar.warning(
                title,
                message,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=3000,
                parent=self,
            )

    def _show_error(self, title: str, message: str):
        InfoBar.error(
            title,
            message,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=5000,
            parent=self,
        )

    def _load_pdf(self, file_path: str):
        if not Path(file_path).exists():
            logger.error("File not found: {}", file_path)
            return

        self._current_pdf_path = file_path
        self._sidebar.load_pdf(file_path)
        self._preview.load_page(file_path, 0)
        self._status.setText(f"  Caricato: {Path(file_path).name}")

    def _on_pdf_dropped(self, file_path: str):
        self._load_pdf(file_path)

    def _on_open_pdf(self):
        filters = "PDF (*.pdf)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Apri PDF", "", filters)
        if file_path:
            self._load_pdf(file_path)

    def _on_save_pdf(self):
        if not self._preview.has_pdf():
            self._show_error("Nessun PDF", "Carica prima un PDF")
            return

        filters = "PDF (*.pdf)"
        out_path, _ = QFileDialog.getSaveFileName(self, "Salva PDF", "", filters)
        if not out_path:
            return

        self._save_current_pdf(out_path)

    def _save_current_pdf(self, out_path: str):
        from shutil import copy2

        copy2(self._preview.get_pdf_path(), out_path)
        self._current_pdf_path = out_path
        self._status.setText(f"  Salvato: {Path(out_path).name}")

    def _on_page_selected(self, page_num: int):
        if self._preview.has_pdf():
            self._preview.load_page(self._preview.get_pdf_path(), page_num)

    def _on_pages_selected(self, page_nums: list):
        if page_nums:
            self._status.setText(f"  Selezionate {len(page_nums)} pagine")

    def _on_create_pdf(self):
        dialog = CreateDialog(self)
        dialog.exec()

    def _create_pdf_from_file(self, file_type: str):
        if file_type not in FILE_TYPES:
            self._show_error("Errore", f"Tipo file non supportato: {file_type}")
            return

        filter_str, ext = FILE_TYPES[file_type]

        file_path, _ = QFileDialog.getOpenFileName(
            self, f"Seleziona file {file_type.upper()}", "", filter_str
        )

        if not file_path:
            return

        output_path = str(Path(file_path).with_suffix(".pdf"))

        try:
            converter = CONVERTERS[file_type]
            converter(file_path, output_path)
            self._status.setText(f"  Creato PDF: {Path(output_path).name}")
        except Exception as e:
            logger.error("Errore conversione: {}", e)
            self._show_error("Errore", str(e))

    def _on_merge_pdf(self):
        dialog = MergeDialog(self)
        dialog.exec()

    def _on_extract_pages(self):
        if not self._preview.has_pdf():
            self._show_error("Nessun PDF", "Carica prima un PDF")
            return
        dialog = ExtractDialog(self)
        dialog.exec()

    def _on_extract_selected(self):
        selected = self._sidebar.get_selected_pages()
        if not selected:
            selected = [self._preview.get_page_num()]

        if not self._preview.has_pdf():
            self._show_error("Nessun PDF", "Carica prima un PDF")
            return

        filters = "PDF (*.pdf)"
        out_path, _ = QFileDialog.getSaveFileName(self, "Estrai pagine", "", filters)
        if not out_path:
            return

        pages_str = ",".join(str(p + 1) for p in selected)
        from core.pdf_extract import extract_pages

        extract_pages(self._preview.get_pdf_path(), out_path, pages_str)
        self._status.setText(f"  Estratte pagine: {pages_str}")

    def _on_split_pdf(self):
        if not self._preview.has_pdf():
            self._show_error("Nessun PDF", "Carica prima un PDF")
            return

        out_dir = QFileDialog.getExistingDirectory(self, "Seleziona cartella")
        if not out_dir:
            return

        split_pdf(self._preview.get_pdf_path(), out_dir)
        self._status.setText("  PDF diviso in pagine separate")

    def _on_delete_selected(self):
        selected = self._sidebar.get_selected_pages()
        if not selected:
            selected = [self._preview.get_page_num()]

        if not self._preview.has_pdf():
            self._show_error("Nessun PDF", "Carica prima un PDF")
            return

        w = MessageBox(
            "Conferma eliminazione",
            f"Eliminare {len(selected)} pagina/e?",
            self,
        )
        if not w.exec():
            return

        filters = "PDF (*.pdf)"
        out_path, _ = QFileDialog.getSaveFileName(self, "Salva PDF", "", filters)
        if not out_path:
            return

        from core.pdf_edit import delete_pages

        delete_pages(self._preview.get_pdf_path(), out_path, selected)
        self._load_pdf(out_path)

    def _on_rotate_cw(self):
        self._rotate_page(90)

    def _on_rotate_ccw(self):
        self._rotate_page(-90)

    def _rotate_page(self, degrees: int):
        if not self._preview.has_pdf():
            self._show_error("Nessun PDF", "Carica prima un PDF")
            return

        current = self._preview.get_page_num()
        filters = "PDF (*.pdf)"
        out_path, _ = QFileDialog.getSaveFileName(
            self, "Salva PDF ruotato", "", filters
        )
        if not out_path:
            return

        from core.pdf_edit import rotate_pages

        rotation = {current: degrees}
        rotate_pages(self._preview.get_pdf_path(), out_path, rotation)
        self._load_pdf(out_path)

    def _on_move_up(self):
        self._move_page(-1)

    def _on_move_down(self):
        self._move_page(1)

    def _move_page(self, offset: int):
        if not self._preview.has_pdf():
            self._show_error("Nessun PDF", "Carica prima un PDF")
            return

        current = self._preview.get_page_num()
        total = self._sidebar.page_count
        new_pos = current + offset

        if new_pos < 0 or new_pos >= total:
            self._show_info("Limite", "Pagina gia in posizione limite")
            return

        filters = "PDF (*.pdf)"
        out_path, _ = QFileDialog.getSaveFileName(self, "Salva PDF", "", filters)
        if not out_path:
            return

        from core.pdf_edit import move_page

        move_page(self._preview.get_pdf_path(), out_path, current, new_pos)
        self._load_pdf(out_path)

    def _on_settings(self):
        from qfluentwidgets import MessageBox
        from gui.theme import load_theme_preference, toggle_theme

        current = load_theme_preference()
        theme_name = "Scuro" if current == Theme.DARK else "Chiaro"

        w = MessageBox(
            "Impostazioni",
            f"Tema corrente: {theme_name}\n\nVuoi cambiare tema?",
            self,
        )
        w.yesButton.setText("Cambia tema")
        if w.exec():
            new_theme = toggle_theme()
            theme_name = "Scuro" if new_theme == Theme.DARK else "Chiaro"
            self._show_info("Tema cambiato", f"Tema {theme_name} applicato")

    def _on_about(self):
        from utils.updater import get_version

        version = get_version()
        w = MessageBox(
            "Informazioni su PDF Tools",
            f"PDF Tools v{version}\n\n"
            f"Applicazione per la manipolazione di file PDF.\n\n"
            f"Funzionalita:\n"
            f"- Crea PDF da file txt, docx, odt, xlsx, csv\n"
            f"- Merge, estrai, dividi PDF\n"
            f"- Modifica e manipola pagine\n\n"
            f"© 2026",
            self,
        )
        w.cancelButton().hide()
        w.exec()
