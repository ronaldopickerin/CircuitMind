"""Tests for synthetic vector PDF rendering."""

from pathlib import Path

from circuitmind.synthetic.cases import good_digital_input_case
from circuitmind.synthetic.pdf import write_pdf_document
from circuitmind.synthetic.spec import (
    SyntheticDocument,
    SyntheticPage,
    SyntheticPoint,
    SyntheticText,
    SyntheticWire,
)


def test_write_pdf_document_creates_expected_file(tmp_path: Path) -> None:
    case = good_digital_input_case()
    document = case.project.documents[0]

    output_path = write_pdf_document(
        document,
        tmp_path,
    )

    assert output_path == tmp_path / "control.pdf"
    assert output_path.is_file()


def test_write_pdf_document_creates_pdf_file(tmp_path: Path) -> None:
    case = good_digital_input_case()
    document = case.project.documents[0]

    output_path = write_pdf_document(
        document,
        tmp_path,
    )

    assert output_path.read_bytes().startswith(b"%PDF-")


def test_write_pdf_document_contains_source_text(tmp_path: Path) -> None:
    case = good_digital_input_case()
    document = case.project.documents[0]

    output_path = write_pdf_document(
        document,
        tmp_path,
    )

    pdf_bytes = output_path.read_bytes()

    assert b"-B101" in pdf_bytes
    assert b"-X1:1" in pdf_bytes
    assert b"B101_HOME" in pdf_bytes
    assert b"Conveyor home sensor" in pdf_bytes


def test_write_pdf_document_contains_no_raster_images(
    tmp_path: Path,
) -> None:
    case = good_digital_input_case()
    document = case.project.documents[0]

    output_path = write_pdf_document(
        document,
        tmp_path,
    )

    pdf_bytes = output_path.read_bytes()

    assert b"/Subtype /Image" not in pdf_bytes


def test_write_pdf_document_is_byte_stable(
    tmp_path: Path,
) -> None:
    case = good_digital_input_case()
    document = case.project.documents[0]

    first_path = write_pdf_document(
        document,
        tmp_path / "first",
    )
    second_path = write_pdf_document(
        document,
        tmp_path / "second",
    )

    assert first_path.read_bytes() == second_path.read_bytes()


def test_write_pdf_document_supports_multiple_pages(
    tmp_path: Path,
) -> None:
    document = SyntheticDocument(
        id="multi-page",
        filename="multi_page.pdf",
        pages=(
            SyntheticPage(
                page_number=1,
                width=842.0,
                height=595.0,
                texts=(
                    SyntheticText(
                        id="page-one-text",
                        text="PAGE_ONE",
                        position=SyntheticPoint(100.0, 100.0),
                    ),
                ),
            ),
            SyntheticPage(
                page_number=2,
                width=842.0,
                height=595.0,
                texts=(
                    SyntheticText(
                        id="page-two-text",
                        text="PAGE_TWO",
                        position=SyntheticPoint(100.0, 100.0),
                    ),
                ),
            ),
        ),
    )

    output_path = write_pdf_document(
        document,
        tmp_path,
    )

    pdf_bytes = output_path.read_bytes()

    assert b"PAGE_ONE" in pdf_bytes
    assert b"PAGE_TWO" in pdf_bytes


def test_write_pdf_document_preserves_wire_colour(
    tmp_path: Path,
) -> None:
    document = SyntheticDocument(
        id="coloured-wire",
        filename="coloured_wire.pdf",
        pages=(
            SyntheticPage(
                page_number=1,
                width=842.0,
                height=595.0,
                wires=(
                    SyntheticWire(
                        id="blue-wire",
                        start=SyntheticPoint(100.0, 200.0),
                        end=SyntheticPoint(300.0, 200.0),
                        stroke_rgb=(0.0, 0.0, 1.0),
                    ),
                ),
            ),
        ),
    )

    output_path = write_pdf_document(
        document,
        tmp_path,
    )

    pdf_bytes = output_path.read_bytes()

    assert b"0 0 1 RG" in pdf_bytes


def test_good_project_documents_can_all_be_rendered(
    tmp_path: Path,
) -> None:
    case = good_digital_input_case()

    output_paths = [
        write_pdf_document(
            document,
            tmp_path,
        )
        for document in case.project.documents
    ]

    assert {path.name for path in output_paths} == {
        "control.pdf",
        "plc_io.pdf",
    }

    assert all(path.is_file() for path in output_paths)
