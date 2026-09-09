import pytest

from circuitmind.model.connection import (
    ConnectionPoint,
    ConnectionPointOccurrence,
    Terminal,
)
from circuitmind.model.geometry import Point2D
from circuitmind.model.source import SourceReference


def make_source() -> SourceReference:
    return SourceReference(
        document_id="schematic.pdf",
        page_number=1,
    )


def test_connection_point_accepts_valid_data() -> None:
    point = ConnectionPoint(
        id="terminal-X1-1",
        device_id="device-X1",
        label="1",
    )

    assert point.id == "terminal-X1-1"
    assert point.device_id == "device-X1"
    assert point.label == "1"


def test_connection_point_rejects_empty_id() -> None:
    with pytest.raises(ValueError, match="id"):
        ConnectionPoint(
            id=" ",
            device_id="device-X1",
            label="1",
        )


def test_connection_point_rejects_empty_device_id() -> None:
    with pytest.raises(ValueError, match="device_id"):
        ConnectionPoint(
            id="terminal-X1-1",
            device_id=" ",
            label="1",
        )


def test_connection_point_rejects_empty_label() -> None:
    with pytest.raises(ValueError, match="label"):
        ConnectionPoint(
            id="terminal-X1-1",
            device_id="device-X1",
            label=" ",
        )


def test_connection_point_occurrence_accepts_valid_data() -> None:
    occurrence = ConnectionPointOccurrence(
        id="occurrence-X1-1-page-1",
        connection_point_id="terminal-X1-1",
        position=Point2D(x=100.0, y=200.0),
        source=make_source(),
    )

    assert occurrence.connection_point_id == "terminal-X1-1"
    assert occurrence.position == Point2D(x=100.0, y=200.0)


def test_connection_point_occurrence_rejects_empty_id() -> None:
    with pytest.raises(ValueError, match="occurrence id"):
        ConnectionPointOccurrence(
            id=" ",
            connection_point_id="terminal-X1-1",
            position=Point2D(x=100.0, y=200.0),
            source=make_source(),
        )


def test_connection_point_occurrence_rejects_empty_connection_point_id() -> None:
    with pytest.raises(ValueError, match="connection_point_id"):
        ConnectionPointOccurrence(
            id="occurrence-X1-1-page-1",
            connection_point_id=" ",
            position=Point2D(x=100.0, y=200.0),
            source=make_source(),
        )


def test_terminal_is_a_connection_point() -> None:
    terminal = Terminal(
        id="terminal-X1-4",
        device_id="device-X1",
        label="4",
    )

    assert isinstance(terminal, ConnectionPoint)
    assert terminal.device_id == "device-X1"
    assert terminal.label == "4"


def test_terminal_inherits_connection_point_validation() -> None:
    with pytest.raises(ValueError, match="label"):
        Terminal(
            id="terminal-X1-4",
            device_id="device-X1",
            label=" ",
        )
