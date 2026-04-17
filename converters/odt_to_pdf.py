from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import utils
from odf import text, teletype
from odf.opendocument import load
from loguru import logger

MARGIN_X = 50
MARGIN_Y = inch
LINE_HEIGHT = 20
FONT_NAME = "Helvetica"
FONT_SIZE = 12


def convert(input_path: str, output_path: str) -> str:
    """Convert ODT file to PDF."""
    logger.info("Converting {} to PDF", input_path)

    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    doc = load(str(input_path))

    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4
    y = height - 1 * inch
    available_width = width - 2 * MARGIN_X

    has_content = False
    for para in doc.getElementsByType(text.P):
        text_content = teletype.extractText(para).strip()
        if not text_content:
            y -= LINE_HEIGHT
            if y < MARGIN_Y:
                c.showPage()
                y = height - 1 * inch
            continue

        has_content = True
        c.setFont(FONT_NAME, FONT_SIZE)

        wrapped = utils.simpleSplit(text_content, FONT_NAME, FONT_SIZE, available_width)
        for line in wrapped:
            if y < MARGIN_Y:
                c.showPage()
                y = height - 1 * inch
                c.setFont(FONT_NAME, FONT_SIZE)
            c.drawString(MARGIN_X, y, line)
            y -= LINE_HEIGHT

    if not has_content:
        raise ValueError("Document has no content")

    c.save()
    logger.info("Saved PDF to: {}", output_path)
    return output_path
