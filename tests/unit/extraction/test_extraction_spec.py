"""Tests for CircuitMind's objective extracted-source model."""

import pytest

from circuitmind.extraction import (
    CSVSourceReference,
    ExtractedBoundingBox,
    ExtractedIOSchedule,
    ExtractedIOScheduleRow,
    ExtractedLine,
    ExtractedPage,
    ExtractedPDFDocument,
    ExtractedPoint,
    ExtractedProject,
    ExtractedRectangle,
    ExtractedText,
    PDFSourceReference,
)


def test_extracted_point_requires_finite_coordinates() -> None:
    with pytest.raises(ValueError, match="finite"):
        ExtractedPoint(float("inf"), 1.0)


def test_extracted_bounding_box_requires_ordered_coordinates() -> None:
    with pytest.raises(ValueError, match="x_min"):
        ExtractedBoundingBox(
            x_min=20.0,
            y_min=10.0,
            x_max=5.0,
            y_max=30.0,
        )


@pytest.mark.parametrize(
    "source_path",
    [
        "",
        "C:\\drawings\\control.pdf",
        "/drawings/control.pdf",
        "../control.pdf",
        "drawings/../control.pdf",
        "drawings//control.pdf",
        "drawings/./control.pdf",
    ],
)
def test_pdf_source_reference_rejects_invalid_source_paths(
    source_path: str,
) -> None:
    with pytest.raises(ValueError):
        PDFSourceReference(
            source_path=source_path,
            page_number=1,
        )


def test_pdf_source_reference_requires_pdf_extension() -> None:
    with pytest.raises(ValueError, match=r"\.pdf"):
        PDFSourceReference(
            source_path="drawings/control.txt",
            page_number=1,
        )


def test_csv_source_reference_requires_valid_row_number() -> None:
    with pytest.raises(ValueError, match="row number"):
        CSVSourceReference(
            source_path="io_schedule.csv",
            row_number=0,
        )


def test_extracted_line_preserves_objective_visual_metadata() -> None:
    line = ExtractedLine(
        start=ExtractedPoint(10.0, 20.0),
        end=ExtractedPoint(30.0, 40.0),
        source=PDFSourceReference(
            source_path="drawings/control.pdf",
            page_number=1,
        ),
        stroke_rgb=(0.0, 0.0, 1.0),
        stroke_width=1.5,
    )

    assert line.stroke_rgb == (0.0, 0.0, 1.0)
    assert line.stroke_width == 1.5


def test_extracted_line_allows_degenerate_source_geometry() -> None:
    point = ExtractedPoint(10.0, 20.0)

    line = ExtractedLine(
        start=point,
        end=point,
        source=PDFSourceReference(
            source_path="drawings/control.pdf",
            page_number=1,
        ),
    )

    assert line.start == line.end


def test_extracted_rectangle_preserves_stroke_and_fill_metadata() -> None:
    rectangle = ExtractedRectangle(
        bounding_box=ExtractedBoundingBox(
            x_min=10.0,
            y_min=20.0,
            x_max=30.0,
            y_max=40.0,
        ),
        source=PDFSourceReference(
            source_path="drawings/control.pdf",
            page_number=1,
        ),
        stroke_rgb=(0.0, 0.0, 0.0),
        fill_rgb=(1.0, 1.0, 1.0),
    )

    assert rectangle.stroke_rgb == (0.0, 0.0, 0.0)
    assert rectangle.fill_rgb == (1.0, 1.0, 1.0)


def test_extracted_page_rejects_primitive_from_different_page() -> None:
    text = ExtractedText(
        text="B101_HOME",
        bounding_box=ExtractedBoundingBox(
            x_min=10.0,
            y_min=20.0,
            x_max=60.0,
            y_max=30.0,
        ),
        source=PDFSourceReference(
            source_path="drawings/control.pdf",
            page_number=2,
        ),
    )

    with pytest.raises(ValueError, match="containing page"):
        ExtractedPage(
            page_number=1,
            width=842.0,
            height=595.0,
            texts=(text,),
        )


def test_extracted_document_rejects_primitive_from_different_document() -> None:
    text = ExtractedText(
        text="B101_HOME",
        bounding_box=ExtractedBoundingBox(
            x_min=10.0,
            y_min=20.0,
            x_max=60.0,
            y_max=30.0,
        ),
        source=PDFSourceReference(
            source_path="drawings/plc_io.pdf",
            page_number=1,
        ),
    )

    page = ExtractedPage(
        page_number=1,
        width=842.0,
        height=595.0,
        texts=(text,),
    )

    with pytest.raises(ValueError, match="containing document"):
        ExtractedPDFDocument(
            source_path="drawings/control.pdf",
            pages=(page,),
        )


def test_extracted_document_requires_unique_page_numbers() -> None:
    first_page = ExtractedPage(
        page_number=1,
        width=842.0,
        height=595.0,
    )

    second_page = ExtractedPage(
        page_number=1,
        width=842.0,
        height=595.0,
    )

    with pytest.raises(ValueError, match="page numbers"):
        ExtractedPDFDocument(
            source_path="drawings/control.pdf",
            pages=(first_page, second_page),
        )


def test_schedule_rows_preserve_raw_values() -> None:
    row = ExtractedIOScheduleRow(
        signal="B101_HOME",
        plc_address="I2.3",
        description="Conveyor home sensor",
        source=CSVSourceReference(
            source_path="io_schedule.csv",
            row_number=2,
        ),
    )

    assert row.signal == "B101_HOME"
    assert row.plc_address == "I2.3"
    assert row.description == "Conveyor home sensor"
    assert row.source.row_number == 2


def test_schedule_rejects_duplicate_source_row_numbers() -> None:
    first_row = ExtractedIOScheduleRow(
        signal="B101_HOME",
        plc_address="I2.3",
        description="Conveyor home sensor",
        source=CSVSourceReference(
            source_path="io_schedule.csv",
            row_number=2,
        ),
    )

    second_row = ExtractedIOScheduleRow(
        signal="B102_GUARD_CLOSED",
        plc_address="I2.4",
        description="Guard closed sensor",
        source=CSVSourceReference(
            source_path="io_schedule.csv",
            row_number=2,
        ),
    )

    with pytest.raises(ValueError, match="row numbers"):
        ExtractedIOSchedule(
            source_path="io_schedule.csv",
            rows=(first_row, second_row),
        )


def test_schedule_rejects_row_from_different_source_file() -> None:
    row = ExtractedIOScheduleRow(
        signal="B101_HOME",
        plc_address="I2.3",
        description="Conveyor home sensor",
        source=CSVSourceReference(
            source_path="other_schedule.csv",
            row_number=2,
        ),
    )

    with pytest.raises(ValueError, match="containing schedule"):
        ExtractedIOSchedule(
            source_path="io_schedule.csv",
            rows=(row,),
        )


def test_extracted_project_requires_at_least_one_source() -> None:
    with pytest.raises(ValueError, match="at least one source"):
        ExtractedProject()


def test_extracted_project_rejects_duplicate_source_paths() -> None:
    document = ExtractedPDFDocument(
        source_path="drawings/control.pdf",
        pages=(
            ExtractedPage(
                page_number=1,
                width=842.0,
                height=595.0,
            ),
        ),
    )

    with pytest.raises(ValueError, match="source paths"):
        ExtractedProject(
            documents=(document, document),
        )


def test_extracted_project_represents_raw_evidence_without_domain_semantics() -> None:
    source = PDFSourceReference(
        source_path="drawings/control.pdf",
        page_number=1,
    )

    page = ExtractedPage(
        page_number=1,
        width=842.0,
        height=595.0,
        texts=(
            ExtractedText(
                text="-B101",
                bounding_box=ExtractedBoundingBox(
                    x_min=120.0,
                    y_min=280.0,
                    x_max=160.0,
                    y_max=292.0,
                ),
                source=source,
            ),
        ),
        lines=(
            ExtractedLine(
                start=ExtractedPoint(200.0, 300.0),
                end=ExtractedPoint(340.0, 300.0),
                source=source,
            ),
        ),
    )

    project = ExtractedProject(
        documents=(
            ExtractedPDFDocument(
                source_path="drawings/control.pdf",
                pages=(page,),
            ),
        ),
    )

    assert project.documents[0].pages[0].texts[0].text == "-B101"
    assert project.documents[0].pages[0].lines[0].end == ExtractedPoint(
        340.0,
        300.0,
    )
