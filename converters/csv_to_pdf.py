from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate
from reportlab.lib import colors
from reportlab.lib.units import inch
import pandas as pd
from loguru import logger

MARGIN = 50
FONT_SIZE = 10
FONT_NAME = "Helvetica"


def convert(input_path: str, output_path: str) -> str:
    """Convert CSV file to PDF."""
    logger.info("Converting {} to PDF", input_path)

    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    encodings = ["utf-8", "latin-1", "cp1252"]
    df = None
    for enc in encodings:
        try:
            df = pd.read_csv(str(input_path), encoding=enc)
            break
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue

    if df is None:
        raise ValueError(f"Unable to parse CSV with any of: {encodings}")

    if df.empty:
        raise ValueError("CSV file is empty")

    data = [df.columns.tolist()] + df.values.tolist()
    data = [[str(cell) if pd.notna(cell) else "" for cell in row] for row in data]

    width, height = A4
    available_width = width - 2 * MARGIN
    num_cols = len(data[0])
    col_width = available_width / num_cols

    table = Table(data, colWidths=[col_width] * num_cols)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, -1), FONT_NAME),
                ("FONTSIZE", (0, 0), (-1, -1), FONT_SIZE),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]
        )
    )

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
    )
    doc.build([table])

    logger.info("Saved PDF to: {}", output_path)
    return output_path
