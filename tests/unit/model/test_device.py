import pytest

from circuitmind.model.device import (
    Device,
    DeviceKind,
    DeviceOccurrence,
    DeviceOccurrenceRole,
)
from circuitmind.model.geometry import BoundingBox
from circuitmind.model.source import SourceReference


def make_source(page_number: int = 1) -> SourceReference:
    return SourceReference(
        document_id="schematic.pdf",
        page_number=page_number,
        bounding_box=BoundingBox(
            x_min=100.0,
            y_min=200.0,
            x_max=150.0,
            y_max=250.0,
        ),
    )


def test_device_accepts_valid_data() -> None:
    device = Device(
        id="device-K1",
        tag="K1",
        kind=DeviceKind.RELAY,
    )

    assert device.id == "device-K1"
    assert device.tag == "K1"
    assert device.kind is DeviceKind.RELAY


def test_device_rejects_empty_id() -> None:
    with pytest.raises(ValueError, match="id"):
        Device(
            id=" ",
            tag="K1",
            kind=DeviceKind.RELAY,
        )


def test_device_rejects_empty_tag() -> None:
    with pytest.raises(ValueError, match="tag"):
        Device(
            id="device-K1",
            tag=" ",
            kind=DeviceKind.RELAY,
        )


def test_device_occurrence_accepts_valid_data() -> None:
    occurrence = DeviceOccurrence(
        id="occurrence-K1-coil-page-1",
        device_id="device-K1",
        role=DeviceOccurrenceRole.COIL,
        source=make_source(),
    )

    assert occurrence.device_id == "device-K1"
    assert occurrence.role is DeviceOccurrenceRole.COIL


def test_device_occurrence_rejects_empty_id() -> None:
    with pytest.raises(ValueError, match="occurrence id"):
        DeviceOccurrence(
            id=" ",
            device_id="device-K1",
            role=DeviceOccurrenceRole.COIL,
            source=make_source(),
        )


def test_device_occurrence_rejects_empty_device_id() -> None:
    with pytest.raises(ValueError, match="device_id"):
        DeviceOccurrence(
            id="occurrence-K1-coil-page-1",
            device_id=" ",
            role=DeviceOccurrenceRole.COIL,
            source=make_source(),
        )


def test_device_occurrence_requires_bounding_box() -> None:
    source = SourceReference(
        document_id="schematic.pdf",
        page_number=1,
    )

    with pytest.raises(ValueError, match="bounding box"):
        DeviceOccurrence(
            id="occurrence-K1-coil-page-1",
            device_id="device-K1",
            role=DeviceOccurrenceRole.COIL,
            source=source,
        )


def test_same_logical_device_can_have_multiple_occurrences() -> None:
    coil = DeviceOccurrence(
        id="occurrence-K1-coil-page-1",
        device_id="device-K1",
        role=DeviceOccurrenceRole.COIL,
        source=make_source(page_number=1),
    )

    contact = DeviceOccurrence(
        id="occurrence-K1-contact-page-4",
        device_id="device-K1",
        role=DeviceOccurrenceRole.CONTACT,
        source=make_source(page_number=4),
    )

    assert coil.device_id == contact.device_id
    assert coil.source.page_number == 1
    assert contact.source.page_number == 4
