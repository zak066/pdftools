from pathlib import Path
from pypdf import PdfReader, PdfWriter
from loguru import logger


def split_pdf(input_path: str, output_dir: str) -> Path:
    """Split PDF into individual page files.

    Args:
        input_path: Path to source PDF.
        output_dir: Directory to save split pages.

    Returns:
        Path to the output directory.

    Raises:
        FileNotFoundError: If input file does not exist.
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(str(input_path))

    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)

        output_path = output_dir / f"{input_path.stem}_page{i + 1}.pdf"
        writer.write(str(output_path))
        logger.info("Created: {}", output_path)

    logger.info("Split complete: {} pages", len(reader.pages))
    return output_dir
