"""Public electrical domain model interfaces for CircuitMind."""

from circuitmind.model.circuit import CircuitModel
from circuitmind.model.connection import (
    ConnectionPoint,
    ConnectionPointOccurrence,
    Terminal,
)
from circuitmind.model.device import (
    Device,
    DeviceKind,
    DeviceOccurrence,
    DeviceOccurrenceRole,
)
from circuitmind.model.document import Document, DrawingPage
from circuitmind.model.finding import Finding, Severity
from circuitmind.model.geometry import BoundingBox, Point2D
from circuitmind.model.net import ElectricalNet, WireSegment
from circuitmind.model.plc import DigitalPLCAddress, PLCArea, PLCChannel
from circuitmind.model.source import SourceReference

__all__ = [
    "BoundingBox",
    "CircuitModel",
    "ConnectionPoint",
    "ConnectionPointOccurrence",
    "Device",
    "DeviceKind",
    "DeviceOccurrence",
    "DeviceOccurrenceRole",
    "DigitalPLCAddress",
    "Document",
    "DrawingPage",
    "ElectricalNet",
    "Finding",
    "PLCArea",
    "PLCChannel",
    "Point2D",
    "Severity",
    "SourceReference",
    "Terminal",
    "WireSegment",
]
