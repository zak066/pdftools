import io
from PIL import Image
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QIcon
from loguru import logger

from qfluentwidgets import CaptionLabel

from utils.pdf_utils import generate_thumbnail, get_pdf_page_count


def pil_to_qpixmap(img: Image.Image) -> QPixmap:
    """Convert PIL Image to QPixmap."""
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    pixmap = QPixmap()
    pixmap.loadFromData(buffer.read())
    return pixmap


class PDFSidebar(QWidget):
    page_selected = Signal(int)
    pages_selected = Signal(list)
    pages_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pdf_path = None
        self._page_count = 0
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._list = QListWidget()
        self._list.setIconSize(QSize(120, 160))
        self._list.setSpacing(5)
        self._list.setSelectionMode(QListWidget.ExtendedSelection)
        self._list.itemClicked.connect(self._on_item_clicked)
        self._list.itemSelectionChanged.connect(self._on_selection_changed)
        layout.addWidget(self._list)

        self._label_info = CaptionLabel("Nessun PDF caricato")
        self._label_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._label_info)

    def load_pdf(self, file_path: str):
        """Load PDF and display thumbnails."""
        self._pdf_path = file_path
        self._page_count = get_pdf_page_count(file_path)
        self._label_info.setText(f"Pagine: {self._page_count}")

        self._list.clear()
        logger.info("Loading {} pages from {}", self._page_count, file_path)

        for i in range(self._page_count):
            thumb = generate_thumbnail(file_path, i, width=120)
            if thumb:
                pixmap = pil_to_qpixmap(thumb)
                icon = QIcon(pixmap)
                item = QListWidgetItem(icon, f"Pagina {i + 1}")
                item.setData(Qt.UserRole, i)
                item.setSizeHint(QSize(130, 170))
                self._list.addItem(item)

        self.pages_changed.emit()

    def _on_item_clicked(self, item):
        page_num = item.data(Qt.UserRole)
        self.page_selected.emit(page_num)

    def _on_selection_changed(self):
        selected = self.get_selected_pages()
        self.pages_selected.emit(selected)

    def get_selected_pages(self) -> list[int]:
        """Get list of selected page numbers (0-based)."""
        selected = []
        for item in self._list.selectedItems():
            selected.append(item.data(Qt.UserRole))
        return selected

    def get_current_page(self) -> int:
        """Get currently selected page (0-based)."""
        current = self._list.currentItem()
        if current:
            return current.data(Qt.UserRole)
        return 0

    @property
    def page_count(self) -> int:
        return self._page_count

    @property
    def pdf_path(self) -> str | None:
        return self._pdf_path

    def clear(self):
        """Clear the sidebar."""
        self._list.clear()
        self._pdf_path = None
        self._page_count = 0
        self._label_info.setText("Nessun PDF caricato")
