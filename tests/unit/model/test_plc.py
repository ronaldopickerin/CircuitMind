import pytest

from circuitmind.model.geometry import Point2D
from circuitmind.model.plc import DigitalPLCAddress, PLCArea, PLCChannel
from circuitmind.model.source import SourceReference


def make_source() -> SourceReference:
    return SourceReference(
        document_id="schematic.pdf",
        page_number=1,
    )


def test_digital_plc_address_formats_input_address() -> None:
    address = DigitalPLCAddress(
        area=PLCArea.INPUT,
        byte=0,
        bit=2,
    )

    assert str(address) == "I0.2"


def test_digital_plc_address_formats_output_address() -> None:
    address = DigitalPLCAddress(
        area=PLCArea.OUTPUT,
        byte=3,
        bit=7,
    )

    assert str(address) == "Q3.7"


def test_digital_plc_address_rejects_negative_byte() -> None:
    with pytest.raises(ValueError, match="byte"):
        DigitalPLCAddress(
            area=PLCArea.INPUT,
            byte=-1,
            bit=0,
        )


@pytest.mark.parametrize("bit", [-1, 8])
def test_digital_plc_address_rejects_invalid_bit(bit: int) -> None:
    with pytest.raises(ValueError, match="bit"):
        DigitalPLCAddress(
            area=PLCArea.INPUT,
            byte=0,
            bit=bit,
        )


def test_plc_channel_accepts_matching_address_and_label() -> None:
    address = DigitalPLCAddress(
        area=PLCArea.INPUT,
        byte=0,
        bit=2,
    )

    channel = PLCChannel(
        id="PLC1:I0.2",
        device_id="PLC1",
        label="I0.2",
        position=Point2D(x=300.0, y=200.0),
        source=make_source(),
        address=address,
    )

    assert channel.address == address
    assert str(channel.address) == "I0.2"


def test_plc_channel_rejects_mismatched_label() -> None:
    address = DigitalPLCAddress(
        area=PLCArea.INPUT,
        byte=0,
        bit=2,
    )

    with pytest.raises(ValueError, match="label"):
        PLCChannel(
            id="PLC1:I0.2",
            device_id="PLC1",
            label="I0.3",
            position=Point2D(x=300.0, y=200.0),
            source=make_source(),
            address=address,
        )
