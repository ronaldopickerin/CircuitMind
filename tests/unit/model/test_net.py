import pytest

from circuitmind.model.geometry import Point2D
from circuitmind.model.net import ElectricalNet, WireSegment
from circuitmind.model.source import SourceReference


def make_source(page_number: int = 1) -> SourceReference:
    return SourceReference(
        document_id="schematic.pdf",
        page_number=page_number,
    )


def test_wire_segment_accepts_valid_data() -> None:
    segment = WireSegment(
        id="wire-page1-001",
        start=Point2D(x=100.0, y=200.0),
        end=Point2D(x=300.0, y=200.0),
        source=make_source(),
    )

    assert segment.start == Point2D(x=100.0, y=200.0)
    assert segment.end == Point2D(x=300.0, y=200.0)


def test_wire_segment_rejects_empty_id() -> None:
    with pytest.raises(ValueError, match="id"):
        WireSegment(
            id=" ",
            start=Point2D(x=100.0, y=200.0),
            end=Point2D(x=300.0, y=200.0),
            source=make_source(),
        )


def test_wire_segment_rejects_zero_length() -> None:
    point = Point2D(x=100.0, y=200.0)

    with pytest.raises(ValueError, match="non-zero"):
        WireSegment(
            id="wire-page1-001",
            start=point,
            end=point,
            source=make_source(),
        )


def test_electrical_net_accepts_connected_points_and_segments() -> None:
    net = ElectricalNet(
        id="net-001",
        connection_point_ids=(
            "sensor-B1-1",
            "terminal-X1-4",
            "plc1-input-0-2",
        ),
        wire_segment_ids=(
            "wire-page1-001",
            "wire-page1-002",
        ),
    )

    assert len(net.connection_point_ids) == 3
    assert len(net.wire_segment_ids) == 2


def test_electrical_net_allows_single_connection_point() -> None:
    net = ElectricalNet(
        id="net-dangling-001",
        connection_point_ids=("sensor-B1-1",),
        wire_segment_ids=("wire-page1-001",),
    )

    assert net.connection_point_ids == ("sensor-B1-1",)


def test_electrical_net_rejects_empty_id() -> None:
    with pytest.raises(ValueError, match="id"):
        ElectricalNet(
            id=" ",
            connection_point_ids=("sensor-B1-1",),
        )


def test_electrical_net_requires_connection_point() -> None:
    with pytest.raises(ValueError, match="at least one"):
        ElectricalNet(
            id="net-001",
            connection_point_ids=(),
        )


def test_electrical_net_rejects_duplicate_connection_points() -> None:
    with pytest.raises(ValueError, match="duplicate connection point"):
        ElectricalNet(
            id="net-001",
            connection_point_ids=(
                "terminal-X1-4",
                "terminal-X1-4",
            ),
        )


def test_electrical_net_rejects_duplicate_wire_segments() -> None:
    with pytest.raises(ValueError, match="duplicate wire segment"):
        ElectricalNet(
            id="net-001",
            connection_point_ids=("terminal-X1-4",),
            wire_segment_ids=(
                "wire-page1-001",
                "wire-page1-001",
            ),
        )
