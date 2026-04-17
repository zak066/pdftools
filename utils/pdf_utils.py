import io
from pathlib import Path
from typing import Optional
import fitz
from PIL import Image
from PySide6.QtGui import QPixmap
from loguru import logger

DEFAULT_THUMBNAIL_WIDTH = 150
DEFAULT_PREVIEW_WIDTH = 600


def pil_to_pixmap(img: Image.Image) -> QPixmap:
    """Convert PIL Image to QPixmap."""
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    pixmap = QPixmap()
    pixmap.loadFromData(buffer.read())
    return pixmap


def get_pdf_page_count(file_path: str) -> int:
    """Get number of pages in PDF."""
    doc = fitz.open(file_path)
    count = len(doc)
    doc.close()
    return count


def generate_thumbnail(
    file_path: str, page_num: int = 0, width: int = DEFAULT_THUMBNAIL_WIDTH
) -> Optional[Image.Image]:
    """Generate thumbnail for a PDF page."""
    try:
        doc = fitz.open(file_path)
        page = doc[page_num]
        zoom = width / page.rect.width
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        doc.close()

        img_data = pix.tobytes("png")
        return Image.open(io.BytesIO(img_data))
    except Exception as e:
        logger.error("Error generating thumbnail: {}", e)
        return None


def render_page(
    file_path: str, page_num: int = 0, width: int = DEFAULT_PREVIEW_WIDTH
) -> Optional[Image.Image]:
    """Render PDF page for preview."""
    return generate_thumbnail(file_path, page_num, width)


def extract_images_from_pdf(file_path: str, output_dir: str) -> list[str]:
    """Extract all images from PDF."""
    doc = fitz.open(file_path)
    output_files = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        for img_index, img in enumerate(page.get_images()):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            output_path = (
                Path(output_dir) / f"page{page_num + 1}_img{img_index + 1}.{image_ext}"
            )
            output_path.write_bytes(image_bytes)
            output_files.append(str(output_path))
            logger.info("Extracted image: {}", output_path)

    doc.close()
    return output_files


def extract_text_from_pdf(file_path: str) -> str:
    """Extract all text from PDF."""
    doc = fitz.open(file_path)
    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()
    return text


def add_text_overlay(
    input_pdf: str,
    output_pdf: str,
    text: str,
    x: float = 50,
    y: float = 50,
    fontsize: int = 12,
) -> str:
    """Add text overlay to PDF pages."""
    doc = fitz.open(input_pdf)

    for page in doc:
        page.insert_text((x, y), text, fontsize=fontsize, color=(1, 0, 0))

    doc.save(output_pdf)
    doc.close()
    logger.info("Added text overlay to: {}", output_pdf)
    return output_pdf
