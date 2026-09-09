import pytest

from circuitmind.model.geometry import BoundingBox
from circuitmind.model.source import SourceReference


def test_source_reference_accepts_page_reference() -> None:
    source = SourceReference(
        document_id="schematic.pdf",
        page_number=2,
    )

    assert source.document_id == "schematic.pdf"
    assert source.page_number == 2
    assert source.row_number is None


def test_source_reference_accepts_page_with_bounding_box() -> None:
    bounding_box = BoundingBox(
        x_min=10.0,
        y_min=20.0,
        x_max=30.0,
        y_max=40.0,
    )

    source = SourceReference(
        document_id="schematic.pdf",
        page_number=2,
        bounding_box=bounding_box,
    )

    assert source.bounding_box == bounding_box


def test_source_reference_accepts_row_reference() -> None:
    source = SourceReference(
        document_id="io-schedule.csv",
        row_number=14,
    )

    assert source.document_id == "io-schedule.csv"
    assert source.row_number == 14
    assert source.page_number is None


def test_source_reference_accepts_document_only_reference() -> None:
    source = SourceReference(
        document_id="io-schedule.csv",
    )

    assert source.document_id == "io-schedule.csv"
    assert source.page_number is None
    assert source.row_number is None


def test_source_reference_rejects_empty_document_id() -> None:
    with pytest.raises(ValueError, match="document_id"):
        SourceReference(
            document_id=" ",
            page_number=1,
        )


@pytest.mark.parametrize("page_number", [0, -1])
def test_source_reference_rejects_invalid_page_number(page_number: int) -> None:
    with pytest.raises(ValueError, match="page_number"):
        SourceReference(
            document_id="schematic.pdf",
            page_number=page_number,
        )


@pytest.mark.parametrize("row_number", [0, -1])
def test_source_reference_rejects_invalid_row_number(row_number: int) -> None:
    with pytest.raises(ValueError, match="row_number"):
        SourceReference(
            document_id="io-schedule.csv",
            row_number=row_number,
        )


def test_source_reference_rejects_bounding_box_without_page() -> None:
    bounding_box = BoundingBox(
        x_min=10.0,
        y_min=20.0,
        x_max=30.0,
        y_max=40.0,
    )

    with pytest.raises(ValueError, match="page_number"):
        SourceReference(
            document_id="io-schedule.csv",
            bounding_box=bounding_box,
        )
