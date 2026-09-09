"""PLC-specific domain models for CircuitMind."""

from dataclasses import dataclass
from enum import Enum

from circuitmind.model.connection import ConnectionPoint


class PLCArea(Enum):
    """Supported PLC digital address areas."""

    INPUT = "I"
    OUTPUT = "Q"


@dataclass(frozen=True, slots=True)
class DigitalPLCAddress:
    """Structured byte/bit address for a digital PLC channel."""

    area: PLCArea
    byte: int
    bit: int

    def __post_init__(self) -> None:
        if self.byte < 0:
            raise ValueError("PLC address byte must not be negative")

        if not 0 <= self.bit <= 7:
            raise ValueError("PLC address bit must be between 0 and 7")

    def __str__(self) -> str:
        return f"{self.area.value}{self.byte}.{self.bit}"


@dataclass(frozen=True, slots=True)
class PLCChannel(ConnectionPoint):
    """A physical PLC channel associated with a structured address."""

    address: DigitalPLCAddress

    def __post_init__(self) -> None:
        ConnectionPoint.__post_init__(self)

        if self.label != str(self.address):
            raise ValueError("PLC channel label must match its address")
