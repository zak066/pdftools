from pathlib import Path
from pypdf import PdfReader, PdfWriter
from loguru import logger


def merge_pdfs(input_paths: list[str], output_path: str) -> str:
    """Merge multiple PDF files into one.

    Args:
        input_paths: List of PDF file paths to merge.
        output_path: Path for the merged output PDF.

    Returns:
        Path to the merged PDF.

    Raises:
        FileNotFoundError: If any input file does not exist.
        ValueError: If fewer than 2 input files provided.
    """
    if len(input_paths) < 2:
        raise ValueError("At least 2 PDF files are required for merge")

    for path in input_paths:
        if not Path(path).exists():
            raise FileNotFoundError(f"File not found: {path}")

    writer = PdfWriter()

    for path in input_paths:
        logger.info("Merging: {}", path)
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)

    writer.write(output_path)
    logger.info("Saved merged PDF to: {}", output_path)
    return output_path
