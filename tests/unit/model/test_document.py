import pytest

from circuitmind.model.document import Document, DrawingPage


def test_document_accepts_valid_data() -> None:
    document = Document(
        id="document-main",
        name="synthetic_schematic.pdf",
    )

    assert document.id == "document-main"
    assert document.name == "synthetic_schematic.pdf"


def test_document_rejects_empty_id() -> None:
    with pytest.raises(ValueError, match="id"):
        Document(
            id=" ",
            name="synthetic_schematic.pdf",
        )


def test_document_rejects_empty_name() -> None:
    with pytest.raises(ValueError, match="name"):
        Document(
            id="document-main",
            name=" ",
        )


def test_drawing_page_accepts_valid_data() -> None:
    page = DrawingPage(
        document_id="document-main",
        page_number=1,
        width=595.0,
        height=842.0,
    )

    assert page.document_id == "document-main"
    assert page.page_number == 1
    assert page.width == 595.0
    assert page.height == 842.0


def test_drawing_page_rejects_empty_document_id() -> None:
    with pytest.raises(ValueError, match="document_id"):
        DrawingPage(
            document_id=" ",
            page_number=1,
            width=595.0,
            height=842.0,
        )


def test_drawing_page_rejects_invalid_page_number() -> None:
    with pytest.raises(ValueError, match="page_number"):
        DrawingPage(
            document_id="document-main",
            page_number=0,
            width=595.0,
            height=842.0,
        )


@pytest.mark.parametrize("width", [0.0, -1.0, float("inf"), float("nan")])
def test_drawing_page_rejects_invalid_width(width: float) -> None:
    with pytest.raises(ValueError, match="width"):
        DrawingPage(
            document_id="document-main",
            page_number=1,
            width=width,
            height=842.0,
        )


@pytest.mark.parametrize("height", [0.0, -1.0, float("inf"), float("nan")])
def test_drawing_page_rejects_invalid_height(height: float) -> None:
    with pytest.raises(ValueError, match="height"):
        DrawingPage(
            document_id="document-main",
            page_number=1,
            width=595.0,
            height=height,
        )
