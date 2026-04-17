from pathlib import Path
from pypdf import PdfReader, PdfWriter
from loguru import logger


def reorder_pages(input_path: str, output_path: str, page_order: list[int]) -> str:
    """Reorder pages in PDF.

    Args:
        input_path: Path to source PDF.
        output_path: Path for output PDF.
        page_order: List of 0-based page indices in desired order.

    Returns:
        Path to the reordered PDF.

    Raises:
        FileNotFoundError: If input file does not exist.
        ValueError: If page_order is invalid.
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    logger.info("Reordering pages: {}", page_order)

    reader = PdfReader(str(input_path))
    total = len(reader.pages)

    if not page_order:
        raise ValueError("page_order cannot be empty")

    for idx in page_order:
        if idx < 0 or idx >= total:
            raise ValueError(f"Invalid page index {idx} (PDF has {total} pages)")

    writer = PdfWriter()
    for idx in page_order:
        writer.add_page(reader.pages[idx])

    writer.write(str(output_path))
    logger.info("Saved reordered PDF to: {}", output_path)
    return output_path


def delete_pages(input_path: str, output_path: str, pages_to_delete: list[int]) -> str:
    """Delete specific pages from PDF.

    Args:
        input_path: Path to source PDF.
        output_path: Path for output PDF.
        pages_to_delete: List of 0-based page indices to remove.

    Returns:
        Path to the modified PDF.

    Raises:
        FileNotFoundError: If input file does not exist.
        ValueError: If all pages would be deleted.
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    logger.info("Deleting pages: {}", pages_to_delete)

    reader = PdfReader(str(input_path))
    total = len(reader.pages)
    delete_set = set(pages_to_delete)

    if len(delete_set) >= total:
        raise ValueError("Cannot delete all pages from PDF")

    writer = PdfWriter()
    for idx, page in enumerate(reader.pages):
        if idx not in delete_set:
            writer.add_page(page)

    writer.write(str(output_path))
    logger.info("Saved PDF (pages deleted) to: {}", output_path)
    return output_path


def rotate_pages(input_path: str, output_path: str, rotations: dict[int, int]) -> str:
    """Rotate pages in PDF.

    Args:
        input_path: Path to source PDF.
        output_path: Path for output PDF.
        rotations: Dict mapping 0-based page index to rotation degrees (90, 180, 270, -90).

    Returns:
        Path to the rotated PDF.

    Raises:
        FileNotFoundError: If input file does not exist.
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    logger.info("Rotating pages: {}", rotations)

    reader = PdfReader(str(input_path))
    writer = PdfWriter()

    for idx, page in enumerate(reader.pages):
        if idx in rotations:
            page.rotate(rotations[idx])
        writer.add_page(page)

    writer.write(str(output_path))
    logger.info("Saved rotated PDF to: {}", output_path)
    return output_path


def move_page(input_path: str, output_path: str, from_idx: int, to_idx: int) -> str:
    """Move a page from one position to another.

    Args:
        input_path: Path to source PDF.
        output_path: Path for output PDF.
        from_idx: 0-based index of page to move.
        to_idx: 0-based destination position.

    Returns:
        Path to the modified PDF.

    Raises:
        FileNotFoundError: If input file does not exist.
        ValueError: If indices are out of range.
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    reader = PdfReader(str(input_path))
    total = len(reader.pages)

    if from_idx < 0 or from_idx >= total or to_idx < 0 or to_idx >= total:
        raise ValueError(
            f"Invalid indices: from={from_idx}, to={to_idx}, total={total}"
        )

    pages = list(reader.pages)
    page = pages.pop(from_idx)
    pages.insert(to_idx, page)

    writer = PdfWriter()
    for p in pages:
        writer.add_page(p)

    writer.write(str(output_path))
    logger.info("Moved page {} to position {}", from_idx, to_idx)
    return output_path
