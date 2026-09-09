import pytest

from circuitmind.model.plc import DigitalPLCAddress, PLCArea, PLCChannel


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
        id="plc1-input-0-2",
        device_id="device-PLC1",
        label="I0.2",
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
            id="plc1-input-0-2",
            device_id="device-PLC1",
            label="I0.3",
            address=address,
        )
