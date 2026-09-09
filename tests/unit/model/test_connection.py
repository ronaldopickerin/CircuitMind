import pytest

from circuitmind.model.connection import ConnectionPoint, Terminal
from circuitmind.model.geometry import Point2D
from circuitmind.model.source import SourceReference


def make_source() -> SourceReference:
    return SourceReference(
        document_id="schematic.pdf",
        page_number=1,
    )


def test_connection_point_accepts_valid_data() -> None:
    point = ConnectionPoint(
        id="X1:1",
        device_id="X1",
        label="1",
        position=Point2D(x=100.0, y=200.0),
        source=make_source(),
    )

    assert point.id == "X1:1"
    assert point.device_id == "X1"
    assert point.label == "1"


def test_connection_point_rejects_empty_id() -> None:
    with pytest.raises(ValueError, match="id"):
        ConnectionPoint(
            id=" ",
            device_id="X1",
            label="1",
            position=Point2D(x=100.0, y=200.0),
            source=make_source(),
        )


def test_connection_point_rejects_empty_device_id() -> None:
    with pytest.raises(ValueError, match="device_id"):
        ConnectionPoint(
            id="X1:1",
            device_id=" ",
            label="1",
            position=Point2D(x=100.0, y=200.0),
            source=make_source(),
        )


def test_connection_point_rejects_empty_label() -> None:
    with pytest.raises(ValueError, match="label"):
        ConnectionPoint(
            id="X1:1",
            device_id="X1",
            label=" ",
            position=Point2D(x=100.0, y=200.0),
            source=make_source(),
        )


def test_terminal_is_a_connection_point() -> None:
    terminal = Terminal(
        id="X1:4",
        device_id="X1",
        label="4",
        position=Point2D(x=100.0, y=200.0),
        source=make_source(),
    )

    assert isinstance(terminal, ConnectionPoint)
    assert terminal.device_id == "X1"
    assert terminal.label == "4"


def test_terminal_inherits_connection_point_validation() -> None:
    with pytest.raises(ValueError, match="label"):
        Terminal(
            id="X1:4",
            device_id="X1",
            label=" ",
            position=Point2D(x=100.0, y=200.0),
            source=make_source(),
        )
