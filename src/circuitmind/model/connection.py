"""Electrical connectivity primitives for CircuitMind."""

from dataclasses import dataclass

from circuitmind.model.geometry import Point2D
from circuitmind.model.source import SourceReference


@dataclass(frozen=True, slots=True)
class ConnectionPoint:
    """A physical electrical endpoint that can participate in a net."""

    id: str
    device_id: str
    label: str
    position: Point2D
    source: SourceReference

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Connection point id must not be empty")

        if not self.device_id.strip():
            raise ValueError("device_id must not be empty")

        if not self.label.strip():
            raise ValueError("Connection point label must not be empty")


@dataclass(frozen=True, slots=True)
class Terminal(ConnectionPoint):
    """A connection point belonging to a terminal block."""

    def __post_init__(self) -> None:
        ConnectionPoint.__post_init__(self)
