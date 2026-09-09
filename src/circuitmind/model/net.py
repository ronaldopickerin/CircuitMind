"""Electrical net and drawn wire models for CircuitMind."""

from dataclasses import dataclass

from circuitmind.model.geometry import Point2D
from circuitmind.model.source import SourceReference


@dataclass(frozen=True, slots=True)
class WireSegment:
    """A straight graphical wire segment within a source drawing."""

    id: str
    start: Point2D
    end: Point2D
    source: SourceReference

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Wire segment id must not be empty")

        if self.start == self.end:
            raise ValueError("Wire segment must have non-zero length")


@dataclass(frozen=True, slots=True)
class ElectricalNet:
    """A logical set of electrically connected connection points."""

    id: str
    connection_point_ids: tuple[str, ...]
    wire_segment_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Electrical net id must not be empty")

        if not self.connection_point_ids:
            raise ValueError("Electrical net must contain at least one connection point")

        if any(not point_id.strip() for point_id in self.connection_point_ids):
            raise ValueError("Connection point ids must not be empty")

        if len(set(self.connection_point_ids)) != len(self.connection_point_ids):
            raise ValueError("Electrical net contains duplicate connection point ids")

        if any(not segment_id.strip() for segment_id in self.wire_segment_ids):
            raise ValueError("Wire segment ids must not be empty")

        if len(set(self.wire_segment_ids)) != len(self.wire_segment_ids):
            raise ValueError("Electrical net contains duplicate wire segment ids")
