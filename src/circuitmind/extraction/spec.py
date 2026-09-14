"""Typed source-level evidence extracted from external engineering files.

PDF geometry uses points with the origin at the bottom-left of the page.

These types intentionally represent objective source evidence rather than
interpreted CircuitMind electrical-domain entities.
"""

from dataclasses import dataclass
from math import isfinite
from pathlib import PurePosixPath

RGB = tuple[float, float, float]


@dataclass(frozen=True, slots=True)
class ExtractedPoint:
    """A point in canonical extracted PDF coordinates."""

    x: float
    y: float

    def __post_init__(self) -> None:
        if not isfinite(self.x) or not isfinite(self.y):
            raise ValueError("Extracted point coordinates must be finite")


@dataclass(frozen=True, slots=True)
class ExtractedBoundingBox:
    """An axis-aligned region in canonical extracted PDF coordinates."""

    x_min: float
    y_min: float
    x_max: float
    y_max: float

    def __post_init__(self) -> None:
        coordinates = (
            self.x_min,
            self.y_min,
            self.x_max,
            self.y_max,
        )

        if not all(isfinite(value) for value in coordinates):
            raise ValueError("Extracted bounding box coordinates must be finite")

        if self.x_min > self.x_max:
            raise ValueError("x_min must not be greater than x_max")

        if self.y_min > self.y_max:
            raise ValueError("y_min must not be greater than y_max")


@dataclass(frozen=True, slots=True)
class PDFSourceReference:
    """Location of extracted evidence within a PDF source file."""

    source_path: str
    page_number: int

    def __post_init__(self) -> None:
        _require_relative_source_path(self.source_path)

        if not self.source_path.lower().endswith(".pdf"):
            raise ValueError("PDF source path must end with .pdf")

        if self.page_number < 1:
            raise ValueError("PDF page number must be greater than or equal to 1")


@dataclass(frozen=True, slots=True)
class CSVSourceReference:
    """Location of extracted evidence within a CSV source file."""

    source_path: str
    row_number: int

    def __post_init__(self) -> None:
        _require_relative_source_path(self.source_path)

        if not self.source_path.lower().endswith(".csv"):
            raise ValueError("CSV source path must end with .csv")

        if self.row_number < 1:
            raise ValueError("CSV row number must be greater than or equal to 1")


@dataclass(frozen=True, slots=True)
class ExtractedText:
    """Visible text recovered from a PDF page."""

    text: str
    bounding_box: ExtractedBoundingBox
    source: PDFSourceReference

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("Extracted text must not be empty")


@dataclass(frozen=True, slots=True)
class ExtractedLine:
    """A vector line recovered from a PDF page."""

    start: ExtractedPoint
    end: ExtractedPoint
    source: PDFSourceReference
    stroke_rgb: RGB | None = None
    stroke_width: float | None = None

    def __post_init__(self) -> None:
        _require_optional_rgb(self.stroke_rgb, "line stroke_rgb")
        _require_optional_stroke_width(self.stroke_width)


@dataclass(frozen=True, slots=True)
class ExtractedRectangle:
    """A vector rectangle recovered from a PDF page."""

    bounding_box: ExtractedBoundingBox
    source: PDFSourceReference
    stroke_rgb: RGB | None = None
    fill_rgb: RGB | None = None
    stroke_width: float | None = None

    def __post_init__(self) -> None:
        _require_optional_rgb(self.stroke_rgb, "rectangle stroke_rgb")
        _require_optional_rgb(self.fill_rgb, "rectangle fill_rgb")
        _require_optional_stroke_width(self.stroke_width)


@dataclass(frozen=True, slots=True)
class ExtractedPage:
    """Objective evidence recovered from one PDF page."""

    page_number: int
    width: float
    height: float
    texts: tuple[ExtractedText, ...] = ()
    lines: tuple[ExtractedLine, ...] = ()
    rectangles: tuple[ExtractedRectangle, ...] = ()

    def __post_init__(self) -> None:
        if self.page_number < 1:
            raise ValueError("Extracted page number must be greater than or equal to 1")

        if not isfinite(self.width) or self.width <= 0:
            raise ValueError("Extracted page width must be positive and finite")

        if not isfinite(self.height) or self.height <= 0:
            raise ValueError("Extracted page height must be positive and finite")

        for source in self._primitive_sources():
            if source.page_number != self.page_number:
                raise ValueError("Extracted primitive page number must match its containing page")

    def _primitive_sources(self) -> tuple[PDFSourceReference, ...]:
        return (
            *(text.source for text in self.texts),
            *(line.source for line in self.lines),
            *(rectangle.source for rectangle in self.rectangles),
        )


@dataclass(frozen=True, slots=True)
class ExtractedPDFDocument:
    """One PDF document after objective source extraction."""

    source_path: str
    pages: tuple[ExtractedPage, ...]

    def __post_init__(self) -> None:
        _require_relative_source_path(self.source_path)

        if not self.source_path.lower().endswith(".pdf"):
            raise ValueError("Extracted PDF document source path must end with .pdf")

        if not self.pages:
            raise ValueError("Extracted PDF document must contain at least one page")

        page_numbers = tuple(page.page_number for page in self.pages)

        if len(page_numbers) != len(set(page_numbers)):
            raise ValueError("Extracted PDF document page numbers must be unique")

        for page in self.pages:
            for source in page._primitive_sources():
                if source.source_path != self.source_path:
                    raise ValueError(
                        "Extracted primitive source path must match its containing document"
                    )


@dataclass(frozen=True, slots=True)
class ExtractedIOScheduleRow:
    """One raw row recovered from an I/O schedule."""

    signal: str
    plc_address: str
    description: str
    source: CSVSourceReference


@dataclass(frozen=True, slots=True)
class ExtractedIOSchedule:
    """One extracted CSV I/O schedule."""

    source_path: str
    rows: tuple[ExtractedIOScheduleRow, ...]

    def __post_init__(self) -> None:
        _require_relative_source_path(self.source_path)

        if not self.source_path.lower().endswith(".csv"):
            raise ValueError("Extracted I/O schedule source path must end with .csv")

        row_numbers = tuple(row.source.row_number for row in self.rows)

        if len(row_numbers) != len(set(row_numbers)):
            raise ValueError("Extracted I/O schedule row numbers must be unique")

        for row in self.rows:
            if row.source.source_path != self.source_path:
                raise ValueError(
                    "Extracted schedule-row source path must match its containing schedule"
                )


@dataclass(frozen=True, slots=True)
class ExtractedProject:
    """A complete project represented only as extracted source evidence."""

    documents: tuple[ExtractedPDFDocument, ...] = ()
    schedules: tuple[ExtractedIOSchedule, ...] = ()

    def __post_init__(self) -> None:
        if not self.documents and not self.schedules:
            raise ValueError("Extracted project must contain at least one source file")

        source_paths = (
            *(document.source_path for document in self.documents),
            *(schedule.source_path for schedule in self.schedules),
        )

        if len(source_paths) != len(set(source_paths)):
            raise ValueError("Extracted project source paths must be unique")


def _require_relative_source_path(source_path: str) -> None:
    """Require a normalised project-relative POSIX source path."""

    if not source_path.strip():
        raise ValueError("Source path must not be empty")

    if "\\" in source_path:
        raise ValueError("Source path must use forward slashes")

    path = PurePosixPath(source_path)

    if path.is_absolute():
        raise ValueError("Source path must be relative to the project directory")

    if ".." in path.parts:
        raise ValueError("Source path must not contain parent traversal")

    if source_path in {".", ".."} or source_path != path.as_posix():
        raise ValueError("Source path must be normalised")


def _require_optional_rgb(
    rgb: RGB | None,
    field_name: str,
) -> None:
    """Validate optional normalised RGB metadata."""

    if rgb is None:
        return

    if len(rgb) != 3:
        raise ValueError(f"{field_name} must contain three channels")

    if any(not isfinite(channel) or channel < 0.0 or channel > 1.0 for channel in rgb):
        raise ValueError(f"{field_name} channels must be finite values between 0 and 1")


def _require_optional_stroke_width(stroke_width: float | None) -> None:
    """Validate optional objective PDF stroke-width metadata."""

    if stroke_width is None:
        return

    if not isfinite(stroke_width) or stroke_width < 0:
        raise ValueError("Stroke width must be finite and non-negative")
