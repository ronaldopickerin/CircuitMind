import pytest

from circuitmind.model.geometry import BoundingBox
from circuitmind.model.source import SourceReference


def test_source_reference_accepts_document_and_page() -> None:
    source = SourceReference(
        document_id="schematic.pdf",
        page_number=2,
    )

    assert source.document_id == "schematic.pdf"
    assert source.page_number == 2
    assert source.bounding_box is None


def test_source_reference_accepts_bounding_box() -> None:
    box = BoundingBox(
        x_min=10.0,
        y_min=20.0,
        x_max=30.0,
        y_max=40.0,
    )

    source = SourceReference(
        document_id="schematic.pdf",
        page_number=1,
        bounding_box=box,
    )

    assert source.bounding_box == box


def test_source_reference_rejects_empty_document_id() -> None:
    with pytest.raises(ValueError, match="document_id"):
        SourceReference(
            document_id="   ",
            page_number=1,
        )


def test_source_reference_rejects_page_zero() -> None:
    with pytest.raises(ValueError, match="page_number"):
        SourceReference(
            document_id="schematic.pdf",
            page_number=0,
        )
