"""Vector PDF rendering for deterministic synthetic electrical drawings."""

from pathlib import Path

from reportlab.pdfgen import canvas  # type: ignore[import-untyped]

from circuitmind.synthetic.spec import SyntheticDocument

SYMBOL_LABEL_FONT = "Helvetica"
SYMBOL_LABEL_FONT_SIZE = 9.0
TEXT_FONT = "Helvetica"
TEXT_FONT_SIZE = 10.0
WIRE_WIDTH = 1.0
SYMBOL_LINE_WIDTH = 1.0


def write_pdf_document(
    document: SyntheticDocument,
    output_directory: Path,
) -> Path:
    """Render one synthetic drawing document as a deterministic vector PDF."""

    output_directory.mkdir(parents=True, exist_ok=True)

    output_path = output_directory / document.filename
    first_page = document.pages[0]

    pdf = canvas.Canvas(
        str(output_path),
        pagesize=(first_page.width, first_page.height),
        pageCompression=0,
        invariant=1,
    )

    pdf.setTitle(document.id)

    for page in document.pages:
        pdf.setPageSize((page.width, page.height))

        pdf.setLineWidth(WIRE_WIDTH)

        for wire in page.wires:
            pdf.line(
                wire.start.x,
                wire.start.y,
                wire.end.x,
                wire.end.y,
            )

        pdf.setLineWidth(SYMBOL_LINE_WIDTH)

        for symbol in page.symbols:
            pdf.rect(
                symbol.position.x,
                symbol.position.y,
                symbol.width,
                symbol.height,
                stroke=1,
                fill=0,
            )

            pdf.setFont(
                SYMBOL_LABEL_FONT,
                SYMBOL_LABEL_FONT_SIZE,
            )

            label_x = symbol.position.x + (symbol.width / 2.0)
            label_y = symbol.position.y + (symbol.height / 2.0) - (SYMBOL_LABEL_FONT_SIZE / 3.0)

            pdf.drawCentredString(
                label_x,
                label_y,
                symbol.label,
            )

        pdf.setFont(
            TEXT_FONT,
            TEXT_FONT_SIZE,
        )

        for text in page.texts:
            pdf.drawString(
                text.position.x,
                text.position.y,
                text.text,
            )

        pdf.showPage()

    pdf.save()

    return output_path
