"""Electrical device models for CircuitMind."""

from dataclasses import dataclass
from enum import Enum

from circuitmind.model.source import SourceReference


class DeviceKind(Enum):
    """Supported high-level logical device categories for CircuitMind V0.1."""

    GENERIC = "generic"
    SENSOR = "sensor"
    TERMINAL_BLOCK = "terminal_block"
    PLC = "plc"
    RELAY = "relay"


class DeviceOccurrenceRole(Enum):
    """Graphical role played by one occurrence of a logical device."""

    PRIMARY = "primary"
    COIL = "coil"
    CONTACT = "contact"
    MODULE = "module"


@dataclass(frozen=True, slots=True)
class Device:
    """A logical electrical device independent of where it is drawn."""

    id: str
    tag: str
    kind: DeviceKind

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Device id must not be empty")

        if not self.tag.strip():
            raise ValueError("Device tag must not be empty")


@dataclass(frozen=True, slots=True)
class DeviceOccurrence:
    """One graphical occurrence of a logical electrical device."""

    id: str
    device_id: str
    role: DeviceOccurrenceRole
    source: SourceReference

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Device occurrence id must not be empty")

        if not self.device_id.strip():
            raise ValueError("device_id must not be empty")

        if self.source.bounding_box is None:
            raise ValueError("Device occurrence must have a bounding box")
