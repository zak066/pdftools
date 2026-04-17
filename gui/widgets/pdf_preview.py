from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from loguru import logger

from gui.widgets.drop_area import DropArea
from config import PREVIEW_MAX_WIDTH


class PDFPreview(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pdf_path = None
        self._page_num = 0
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._drop_area = DropArea()
        layout.addWidget(self._drop_area)

        self._page_label = QLabel("")
        self._page_label.setAlignment(Qt.AlignCenter)
        self._page_label.setStyleSheet("color: gray; font-size: 12px;")
        layout.addWidget(self._page_label)

    def load_page(self, file_path: str, page_num: int = 0):
        self._pdf_path = file_path
        self._page_num = page_num

        pixmap = self._render_page(file_path, page_num)
        if pixmap:
            self._drop_area.set_pixmap(pixmap)
            self._page_label.setText(f"Pagina {page_num + 1}")
        else:
            self._drop_area.set_text("Errore nel caricamento")

    def _render_page(
        self, file_path: str, page_num: int, max_width: int = PREVIEW_MAX_WIDTH
    ):
        import fitz

        try:
            doc = fitz.open(file_path)
            page = doc[page_num]
            zoom = max_width / page.rect.width
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            doc.close()

            img_data = pix.tobytes("png")
            pixmap = QPixmap()
            pixmap.loadFromData(img_data)
            return pixmap
        except Exception as e:
            logger.error("Error rendering: {}", e)
            return None

    def clear(self):
        self._drop_area.set_text("Trascina un PDF qui")
        self._page_label.setText("")
        self._pdf_path = None

    @property
    def pdf_path(self) -> str | None:
        return self._pdf_path

    @property
    def page_num(self) -> int:
        return self._page_num

    def has_pdf(self) -> bool:
        return self._pdf_path is not None

    def get_pdf_path(self) -> str | None:
        return self._pdf_path

    def get_page_num(self) -> int:
        return self._page_num
