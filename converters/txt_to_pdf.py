from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import utils
from loguru import logger

MARGIN_X = 50
MARGIN_Y = inch
LINE_HEIGHT = 15
MAX_CHARS_PER_LINE = 80
FONT_NAME = "Helvetica"
FONT_SIZE = 12


def detect_encoding(file_path: Path) -> str:
    """Detect file encoding by checking BOM and content."""
    raw = file_path.read_bytes()

    if raw.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    if raw.startswith(b"\xff\xfe"):
        return "utf-16-le"
    if raw.startswith(b"\xfe\xff"):
        return "utf-16-be"

    if len(raw) >= 2:
        null_count = raw.count(b"\x00")
        if null_count > len(raw) * 0.25:
            if raw[0] == 0 or raw[1] == 0:
                return "utf-16-le"

    for enc in ["utf-8", "cp1252", "latin-1"]:
        try:
            raw.decode(enc)
            return enc
        except (UnicodeDecodeError, ValueError):
            continue

    return "utf-8"


def convert(input_path: str, output_path: str) -> str:
    """Convert text file to PDF."""
    logger.info("Converting {} to PDF", input_path)

    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    encoding = detect_encoding(input_path)
    logger.info("Detected encoding: {}", encoding)

    with open(input_path, "r", encoding=encoding) as f:
        text = f.read()

    text = text.lstrip("\ufeff")

    if not text.strip():
        raise ValueError("File is empty")

    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4

    y = height - 1 * inch
    c.setFont(FONT_NAME, FONT_SIZE)

    for line in text.split("\n"):
        if line.strip():
            if len(line) > MAX_CHARS_PER_LINE:
                wrapped = utils.simpleSplit(
                    line, FONT_NAME, FONT_SIZE, width - 2 * MARGIN_X
                )
                for chunk in wrapped:
                    c.drawString(MARGIN_X, y, chunk)
                    y -= LINE_HEIGHT
                    if y < MARGIN_Y:
                        c.showPage()
                        y = height - 1 * inch
                        c.setFont(FONT_NAME, FONT_SIZE)
            else:
                c.drawString(MARGIN_X, y, line)
                y -= LINE_HEIGHT
        else:
            y -= LINE_HEIGHT

        if y < MARGIN_Y:
            c.showPage()
            y = height - 1 * inch
            c.setFont(FONT_NAME, FONT_SIZE)

    c.save()
    logger.info("Saved PDF to: {}", output_path)
    return output_path
