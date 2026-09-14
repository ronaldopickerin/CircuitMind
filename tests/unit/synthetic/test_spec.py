"""Tests for synthetic electrical project source specifications."""

from math import inf, nan

import pytest

from circuitmind.synthetic.spec import (
    ExpectedFinding,
    IOSchedule,
    IOScheduleRow,
    SyntheticDocument,
    SyntheticPage,
    SyntheticPoint,
    SyntheticProject,
    SyntheticProjectCase,
    SyntheticSymbol,
    SyntheticText,
    SyntheticWire,
)


def make_page(page_number: int = 1) -> SyntheticPage:
    """Create a minimal valid synthetic page for tests."""

    return SyntheticPage(
        page_number=page_number,
        width=842.0,
        height=595.0,
    )


def make_document(
    document_id: str = "control",
    filename: str = "control.pdf",
    page_number: int = 1,
) -> SyntheticDocument:
    """Create a minimal valid synthetic document for tests."""

    return SyntheticDocument(
        id=document_id,
        filename=filename,
        pages=(make_page(page_number),),
    )


def test_point_accepts_finite_coordinates() -> None:
    point = SyntheticPoint(x=10.5, y=-2.0)

    assert point.x == 10.5
    assert point.y == -2.0


@pytest.mark.parametrize(
    ("x", "y"),
    [
        (nan, 0.0),
        (0.0, nan),
        (inf, 0.0),
        (0.0, -inf),
    ],
)
def test_point_rejects_non_finite_coordinates(x: float, y: float) -> None:
    with pytest.raises(ValueError, match="coordinates must be finite"):
        SyntheticPoint(x=x, y=y)


def test_symbol_accepts_valid_source_geometry() -> None:
    symbol = SyntheticSymbol(
        id="sensor-1",
        kind="sensor",
        label="-B101",
        position=SyntheticPoint(100.0, 200.0),
        width=40.0,
        height=20.0,
    )

    assert symbol.label == "-B101"


@pytest.mark.parametrize("width", [0.0, -1.0, inf, nan])
def test_symbol_rejects_invalid_width(width: float) -> None:
    with pytest.raises(ValueError, match="width must be positive and finite"):
        SyntheticSymbol(
            id="sensor-1",
            kind="sensor",
            label="-B101",
            position=SyntheticPoint(100.0, 200.0),
            width=width,
            height=20.0,
        )


@pytest.mark.parametrize("height", [0.0, -1.0, inf, nan])
def test_symbol_rejects_invalid_height(height: float) -> None:
    with pytest.raises(ValueError, match="height must be positive and finite"):
        SyntheticSymbol(
            id="sensor-1",
            kind="sensor",
            label="-B101",
            position=SyntheticPoint(100.0, 200.0),
            width=40.0,
            height=height,
        )


def test_wire_rejects_zero_length_segment() -> None:
    point = SyntheticPoint(100.0, 200.0)

    with pytest.raises(ValueError, match="non-zero length"):
        SyntheticWire(
            id="wire-1",
            start=point,
            end=point,
        )


def test_page_rejects_duplicate_primitive_ids() -> None:
    page_point = SyntheticPoint(100.0, 200.0)

    with pytest.raises(ValueError, match="primitive ids must be unique"):
        SyntheticPage(
            page_number=1,
            width=842.0,
            height=595.0,
            symbols=(
                SyntheticSymbol(
                    id="source-1",
                    kind="sensor",
                    label="-B101",
                    position=page_point,
                    width=40.0,
                    height=20.0,
                ),
            ),
            texts=(
                SyntheticText(
                    id="source-1",
                    text="I2.3",
                    position=SyntheticPoint(200.0, 200.0),
                ),
            ),
        )


def test_document_rejects_duplicate_page_numbers() -> None:
    with pytest.raises(ValueError, match="page numbers must be unique"):
        SyntheticDocument(
            id="control",
            filename="control.pdf",
            pages=(make_page(1), make_page(1)),
        )


def test_document_requires_pdf_filename() -> None:
    with pytest.raises(ValueError, match=r"must end with \.pdf"):
        make_document(filename="control.dwg")


def test_schedule_requires_csv_filename() -> None:
    with pytest.raises(ValueError, match=r"must end with \.csv"):
        IOSchedule(
            id="io",
            filename="io_schedule.xlsx",
            rows=(),
        )


def test_project_supports_multiple_documents_and_schedule() -> None:
    project = SyntheticProject(
        id="good-digital-input",
        documents=(
            make_document("control", "control.pdf"),
            make_document("plc-io", "plc_io.pdf"),
        ),
        schedules=(
            IOSchedule(
                id="io",
                filename="io_schedule.csv",
                rows=(
                    IOScheduleRow(
                        signal="B101_HOME",
                        plc_address="I2.3",
                        description="Conveyor home sensor",
                    ),
                ),
            ),
        ),
    )

    assert len(project.documents) == 2
    assert len(project.schedules) == 1


def test_project_rejects_duplicate_document_ids() -> None:
    with pytest.raises(ValueError, match="document ids must be unique"):
        SyntheticProject(
            id="project",
            documents=(
                make_document("drawing", "control.pdf"),
                make_document("drawing", "plc_io.pdf"),
            ),
        )


def test_project_rejects_duplicate_document_filenames() -> None:
    with pytest.raises(ValueError, match="document filenames must be unique"):
        SyntheticProject(
            id="project",
            documents=(
                make_document("control", "drawing.pdf"),
                make_document("plc-io", "drawing.pdf"),
            ),
        )


def test_project_rejects_duplicate_schedule_ids() -> None:
    with pytest.raises(ValueError, match="schedule ids must be unique"):
        SyntheticProject(
            id="project",
            documents=(make_document(),),
            schedules=(
                IOSchedule(id="io", filename="inputs.csv", rows=()),
                IOSchedule(id="io", filename="outputs.csv", rows=()),
            ),
        )


def test_duplicate_engineering_labels_remain_representable() -> None:
    page = SyntheticPage(
        page_number=1,
        width=842.0,
        height=595.0,
        symbols=(
            SyntheticSymbol(
                id="sensor-1",
                kind="sensor",
                label="-B101",
                position=SyntheticPoint(100.0, 200.0),
                width=40.0,
                height=20.0,
            ),
            SyntheticSymbol(
                id="sensor-2",
                kind="sensor",
                label="-B101",
                position=SyntheticPoint(300.0, 200.0),
                width=40.0,
                height=20.0,
            ),
        ),
    )

    assert page.symbols[0].label == page.symbols[1].label


def test_duplicate_plc_addresses_remain_representable() -> None:
    schedule = IOSchedule(
        id="io",
        filename="io_schedule.csv",
        rows=(
            IOScheduleRow(
                signal="B101_HOME",
                plc_address="I2.3",
                description="Conveyor home sensor",
            ),
            IOScheduleRow(
                signal="B102_HOME",
                plc_address="I2.3",
                description="Second conveyor home sensor",
            ),
        ),
    )

    assert schedule.rows[0].plc_address == schedule.rows[1].plc_address


def test_dangling_wire_remains_representable() -> None:
    wire = SyntheticWire(
        id="wire-1",
        start=SyntheticPoint(100.0, 200.0),
        end=SyntheticPoint(250.0, 200.0),
    )

    page = SyntheticPage(
        page_number=1,
        width=842.0,
        height=595.0,
        wires=(wire,),
    )

    assert page.wires == (wire,)


def test_schedule_mismatch_remains_representable() -> None:
    page = SyntheticPage(
        page_number=1,
        width=842.0,
        height=595.0,
        texts=(
            SyntheticText(
                id="plc-address",
                text="I2.3",
                position=SyntheticPoint(400.0, 200.0),
            ),
        ),
    )

    project = SyntheticProject(
        id="schedule-mismatch",
        documents=(
            SyntheticDocument(
                id="plc-io",
                filename="plc_io.pdf",
                pages=(page,),
            ),
        ),
        schedules=(
            IOSchedule(
                id="io",
                filename="io_schedule.csv",
                rows=(
                    IOScheduleRow(
                        signal="B101_HOME",
                        plc_address="I2.4",
                        description="Conveyor home sensor",
                    ),
                ),
            ),
        ),
    )

    case = SyntheticProjectCase(
        project=project,
        expected_findings=(ExpectedFinding(rule_id="CM-R003"),),
    )

    assert project.schedules[0].rows[0].plc_address == "I2.4"
    assert page.texts[0].text == "I2.3"
    assert case.expected_findings == (ExpectedFinding(rule_id="CM-R003"),)
