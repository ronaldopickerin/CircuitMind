"""Objective source extraction interfaces for CircuitMind."""

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
]
