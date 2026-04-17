from pathlib import Path
from pypdf import PdfReader, PdfWriter
from loguru import logger


def parse_pages(pages_str: str, total_pages: int) -> list[int]:
    """Parse page ranges like '1,3-5,7' into list of 0-based indices.

    Args:
        pages_str: Comma-separated page numbers/ranges (1-based).
        total_pages: Total number of pages in the PDF.

    Returns:
        Sorted list of unique 0-based page indices.

    Raises:
        ValueError: If page numbers are out of range or malformed.
    """
    pages: set[int] = set()
    parts = pages_str.split(",")
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_str, end_str = part.split("-", 1)
            start = int(start_str.strip())
            end = int(end_str.strip())
            if start < 1 or end > total_pages or start > end:
                raise ValueError(
                    f"Invalid range '{part}' for PDF with {total_pages} pages"
                )
            for p in range(start, end + 1):
                pages.add(p - 1)
        else:
            p = int(part)
            if p < 1 or p > total_pages:
                raise ValueError(f"Page {p} out of range (PDF has {total_pages} pages)")
            pages.add(p - 1)
    if not pages:
        raise ValueError("No valid pages specified")
    return sorted(pages)


def extract_pages(input_path: str, output_path: str, pages_str: str) -> str:
    """Extract specific pages from a PDF.

    Args:
        input_path: Path to source PDF.
        output_path: Path for output PDF.
        pages_str: Comma-separated page numbers/ranges (1-based).

    Returns:
        Path to the extracted PDF.

    Raises:
        FileNotFoundError: If input file does not exist.
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    logger.info("Extracting pages {} from {}", pages_str, input_path)

    reader = PdfReader(str(input_path))
    total = len(reader.pages)
    page_indices = parse_pages(pages_str, total)

    writer = PdfWriter()
    for idx in page_indices:
        writer.add_page(reader.pages[idx])

    writer.write(str(output_path))
    logger.info("Saved extracted PDF to: {}", output_path)
    return output_path
