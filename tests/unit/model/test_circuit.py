import pytest

from circuitmind.model.circuit import CircuitModel
from circuitmind.model.connection import (
    ConnectionPoint,
    ConnectionPointOccurrence,
)
from circuitmind.model.device import (
    Device,
    DeviceKind,
    DeviceOccurrence,
    DeviceOccurrenceRole,
)
from circuitmind.model.document import Document, DrawingPage
from circuitmind.model.geometry import BoundingBox, Point2D
from circuitmind.model.net import ElectricalNet, WireSegment
from circuitmind.model.plc import DigitalPLCAddress, PLCArea, PLCChannel
from circuitmind.model.source import SourceReference


def make_document() -> Document:
    return Document(
        id="document-main",
        name="synthetic_schematic.pdf",
    )


def make_page(page_number: int = 1) -> DrawingPage:
    return DrawingPage(
        document_id="document-main",
        page_number=page_number,
        width=595.0,
        height=842.0,
    )


def make_page_source(page_number: int = 1) -> SourceReference:
    return SourceReference(
        document_id="document-main",
        page_number=page_number,
    )


def make_bounded_page_source(page_number: int = 1) -> SourceReference:
    return SourceReference(
        document_id="document-main",
        page_number=page_number,
        bounding_box=BoundingBox(
            x_min=100.0,
            y_min=200.0,
            x_max=150.0,
            y_max=250.0,
        ),
    )


def test_circuit_model_accepts_consistent_references() -> None:
    device = Device(
        id="device-B1",
        tag="B1",
        kind=DeviceKind.SENSOR,
    )

    device_occurrence = DeviceOccurrence(
        id="occurrence-B1-page-1",
        device_id="device-B1",
        role=DeviceOccurrenceRole.PRIMARY,
        source=make_bounded_page_source(),
    )

    connection_point = ConnectionPoint(
        id="connection-B1-1",
        device_id="device-B1",
        label="1",
    )

    connection_point_occurrence = ConnectionPointOccurrence(
        id="occurrence-B1-1-page-1",
        connection_point_id="connection-B1-1",
        position=Point2D(x=150.0, y=225.0),
        source=make_page_source(),
    )

    wire_segment = WireSegment(
        id="wire-page1-001",
        start=Point2D(x=150.0, y=225.0),
        end=Point2D(x=300.0, y=225.0),
        source=make_page_source(),
    )

    net = ElectricalNet(
        id="net-001",
        connection_point_ids=("connection-B1-1",),
        wire_segment_ids=("wire-page1-001",),
    )

    model = CircuitModel(
        documents=(make_document(),),
        pages=(make_page(),),
        devices=(device,),
        device_occurrences=(device_occurrence,),
        connection_points=(connection_point,),
        connection_point_occurrences=(connection_point_occurrence,),
        wire_segments=(wire_segment,),
        electrical_nets=(net,),
    )

    assert model.devices == (device,)
    assert model.electrical_nets == (net,)


def test_circuit_model_rejects_duplicate_document_ids() -> None:
    with pytest.raises(ValueError, match="Duplicate document ids"):
        CircuitModel(
            documents=(
                Document(
                    id="document-main",
                    name="schematic-a.pdf",
                ),
                Document(
                    id="document-main",
                    name="schematic-b.pdf",
                ),
            ),
        )


def test_circuit_model_rejects_page_with_unknown_document() -> None:
    with pytest.raises(ValueError, match="unknown document_id"):
        CircuitModel(
            documents=(make_document(),),
            pages=(
                DrawingPage(
                    document_id="missing-document",
                    page_number=1,
                    width=595.0,
                    height=842.0,
                ),
            ),
        )


def test_circuit_model_rejects_duplicate_drawing_page() -> None:
    with pytest.raises(ValueError, match="Duplicate drawing page"):
        CircuitModel(
            documents=(make_document(),),
            pages=(
                make_page(),
                make_page(),
            ),
        )


def test_circuit_model_rejects_device_occurrence_with_unknown_device() -> None:
    occurrence = DeviceOccurrence(
        id="occurrence-K1-page-1",
        device_id="missing-device",
        role=DeviceOccurrenceRole.COIL,
        source=make_bounded_page_source(),
    )

    with pytest.raises(ValueError, match="unknown device_id"):
        CircuitModel(
            documents=(make_document(),),
            pages=(make_page(),),
            device_occurrences=(occurrence,),
        )


def test_circuit_model_rejects_connection_point_with_unknown_device() -> None:
    point = ConnectionPoint(
        id="connection-B1-1",
        device_id="missing-device",
        label="1",
    )

    with pytest.raises(ValueError, match="unknown device_id"):
        CircuitModel(
            connection_points=(point,),
        )


def test_circuit_model_rejects_occurrence_with_unknown_connection_point() -> None:
    occurrence = ConnectionPointOccurrence(
        id="occurrence-B1-1-page-1",
        connection_point_id="missing-connection-point",
        position=Point2D(x=100.0, y=200.0),
        source=make_page_source(),
    )

    with pytest.raises(ValueError, match="unknown connection_point_id"):
        CircuitModel(
            documents=(make_document(),),
            pages=(make_page(),),
            connection_point_occurrences=(occurrence,),
        )


def test_connection_point_occurrence_requires_drawing_page_source() -> None:
    device = Device(
        id="device-B1",
        tag="B1",
        kind=DeviceKind.SENSOR,
    )

    point = ConnectionPoint(
        id="connection-B1-1",
        device_id="device-B1",
        label="1",
    )

    occurrence = ConnectionPointOccurrence(
        id="occurrence-B1-1",
        connection_point_id="connection-B1-1",
        position=Point2D(x=100.0, y=200.0),
        source=SourceReference(
            document_id="document-main",
        ),
    )

    with pytest.raises(ValueError, match="must reference a drawing page"):
        CircuitModel(
            documents=(make_document(),),
            devices=(device,),
            connection_points=(point,),
            connection_point_occurrences=(occurrence,),
        )


def test_circuit_model_rejects_connection_occurrence_on_unknown_page() -> None:
    device = Device(
        id="device-B1",
        tag="B1",
        kind=DeviceKind.SENSOR,
    )

    point = ConnectionPoint(
        id="connection-B1-1",
        device_id="device-B1",
        label="1",
    )

    occurrence = ConnectionPointOccurrence(
        id="occurrence-B1-1-page-2",
        connection_point_id="connection-B1-1",
        position=Point2D(x=100.0, y=200.0),
        source=make_page_source(page_number=2),
    )

    with pytest.raises(ValueError, match="unknown drawing page"):
        CircuitModel(
            documents=(make_document(),),
            pages=(make_page(page_number=1),),
            devices=(device,),
            connection_points=(point,),
            connection_point_occurrences=(occurrence,),
        )


def test_circuit_model_rejects_wire_segment_on_unknown_page() -> None:
    segment = WireSegment(
        id="wire-page2-001",
        start=Point2D(x=100.0, y=200.0),
        end=Point2D(x=300.0, y=200.0),
        source=make_page_source(page_number=2),
    )

    with pytest.raises(ValueError, match="unknown drawing page"):
        CircuitModel(
            documents=(make_document(),),
            pages=(make_page(page_number=1),),
            wire_segments=(segment,),
        )


def test_circuit_model_rejects_net_with_unknown_connection_point() -> None:
    net = ElectricalNet(
        id="net-001",
        connection_point_ids=("missing-connection-point",),
    )

    with pytest.raises(ValueError, match="unknown connection_point_id"):
        CircuitModel(
            electrical_nets=(net,),
        )


def test_circuit_model_rejects_net_with_unknown_wire_segment() -> None:
    device = Device(
        id="device-B1",
        tag="B1",
        kind=DeviceKind.SENSOR,
    )

    point = ConnectionPoint(
        id="connection-B1-1",
        device_id="device-B1",
        label="1",
    )

    net = ElectricalNet(
        id="net-001",
        connection_point_ids=("connection-B1-1",),
        wire_segment_ids=("missing-wire",),
    )

    with pytest.raises(ValueError, match="unknown wire_segment_id"):
        CircuitModel(
            devices=(device,),
            connection_points=(point,),
            electrical_nets=(net,),
        )


def test_connection_point_cannot_belong_to_multiple_nets() -> None:
    device = Device(
        id="device-B1",
        tag="B1",
        kind=DeviceKind.SENSOR,
    )

    point = ConnectionPoint(
        id="connection-B1-1",
        device_id="device-B1",
        label="1",
    )

    with pytest.raises(ValueError, match="multiple electrical nets"):
        CircuitModel(
            devices=(device,),
            connection_points=(point,),
            electrical_nets=(
                ElectricalNet(
                    id="net-001",
                    connection_point_ids=("connection-B1-1",),
                ),
                ElectricalNet(
                    id="net-002",
                    connection_point_ids=("connection-B1-1",),
                ),
            ),
        )


def test_wire_segment_cannot_belong_to_multiple_nets() -> None:
    device = Device(
        id="device-B1",
        tag="B1",
        kind=DeviceKind.SENSOR,
    )

    point_one = ConnectionPoint(
        id="connection-B1-1",
        device_id="device-B1",
        label="1",
    )

    point_two = ConnectionPoint(
        id="connection-B1-2",
        device_id="device-B1",
        label="2",
    )

    segment = WireSegment(
        id="wire-page1-001",
        start=Point2D(x=100.0, y=200.0),
        end=Point2D(x=300.0, y=200.0),
        source=make_page_source(),
    )

    with pytest.raises(ValueError, match="multiple electrical nets"):
        CircuitModel(
            documents=(make_document(),),
            pages=(make_page(),),
            devices=(device,),
            connection_points=(point_one, point_two),
            wire_segments=(segment,),
            electrical_nets=(
                ElectricalNet(
                    id="net-001",
                    connection_point_ids=("connection-B1-1",),
                    wire_segment_ids=("wire-page1-001",),
                ),
                ElectricalNet(
                    id="net-002",
                    connection_point_ids=("connection-B1-2",),
                    wire_segment_ids=("wire-page1-001",),
                ),
            ),
        )


def test_duplicate_device_tags_are_structurally_valid() -> None:
    model = CircuitModel(
        devices=(
            Device(
                id="device-K1-a",
                tag="K1",
                kind=DeviceKind.RELAY,
            ),
            Device(
                id="device-K1-b",
                tag="K1",
                kind=DeviceKind.RELAY,
            ),
        ),
    )

    assert len(model.devices) == 2
    assert model.devices[0].tag == model.devices[1].tag


def test_duplicate_plc_addresses_are_structurally_valid() -> None:
    plc = Device(
        id="device-PLC1",
        tag="PLC1",
        kind=DeviceKind.PLC,
    )

    address = DigitalPLCAddress(
        area=PLCArea.INPUT,
        byte=0,
        bit=2,
    )

    channel_one = PLCChannel(
        id="plc1-channel-a",
        device_id="device-PLC1",
        label="I0.2",
        address=address,
    )

    channel_two = PLCChannel(
        id="plc1-channel-b",
        device_id="device-PLC1",
        label="I0.2",
        address=address,
    )

    model = CircuitModel(
        devices=(plc,),
        connection_points=(channel_one, channel_two),
    )

    assert len(model.connection_points) == 2
