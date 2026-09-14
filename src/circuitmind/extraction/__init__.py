"""Objective source extraction interfaces for CircuitMind."""

from circuitmind.extraction.project import (
    DiscoveredProjectSources,
    discover_project_sources,
)
from circuitmind.extraction.spec import (
    RGB,
    CSVSourceReference,
    ExtractedBoundingBox,
    ExtractedIOSchedule,
    ExtractedIOScheduleRow,
    ExtractedLine,
    ExtractedPage,
    ExtractedPDFDocument,
    ExtractedPoint,
    ExtractedProject,
    ExtractedRectangle,
    ExtractedText,
    PDFSourceReference,
)

__all__ = [
    "CSVSourceReference",
    "ExtractedBoundingBox",
    "ExtractedIOSchedule",
    "ExtractedIOScheduleRow",
    "ExtractedLine",
    "ExtractedPDFDocument",
    "ExtractedPage",
    "ExtractedPoint",
    "ExtractedProject",
    "ExtractedRectangle",
    "ExtractedText",
    "PDFSourceReference",
    "RGB",
    "DiscoveredProjectSources",
    "discover_project_sources",
]
