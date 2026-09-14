"""Source specifications for deterministic synthetic electrical projects."""

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True, slots=True)
class SyntheticPoint:
    """A two-dimensional point in a synthetic source document."""

    x: float
    y: float

    def __post_init__(self) -> None:
        if not isfinite(self.x) or not isfinite(self.y):
            raise ValueError("Synthetic point coordinates must be finite")


@dataclass(frozen=True, slots=True)
class SyntheticSymbol:
    """A symbol intentionally drawn into a synthetic source document."""

    id: str
    kind: str
    label: str
    position: SyntheticPoint
    width: float
    height: float

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Synthetic symbol id must not be empty")

        if not self.kind.strip():
            raise ValueError("Synthetic symbol kind must not be empty")

        if not self.label.strip():
            raise ValueError("Synthetic symbol label must not be empty")

        if not isfinite(self.width) or self.width <= 0:
            raise ValueError("Synthetic symbol width must be positive and finite")

        if not isfinite(self.height) or self.height <= 0:
            raise ValueError("Synthetic symbol height must be positive and finite")


@dataclass(frozen=True, slots=True)
class SyntheticWire:
    """A straight wire segment intentionally drawn on a synthetic page."""

    id: str
    start: SyntheticPoint
    end: SyntheticPoint

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Synthetic wire id must not be empty")

        if self.start == self.end:
            raise ValueError("Synthetic wire must have non-zero length")


@dataclass(frozen=True, slots=True)
class SyntheticText:
    """Standalone visible text intentionally placed on a synthetic page."""

    id: str
    text: str
    position: SyntheticPoint

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Synthetic text id must not be empty")

        if not self.text.strip():
            raise ValueError("Synthetic text must not be empty")


@dataclass(frozen=True, slots=True)
class SyntheticPage:
    """One page within a synthetic electrical drawing document."""

    page_number: int
    width: float
    height: float
    symbols: tuple[SyntheticSymbol, ...] = ()
    wires: tuple[SyntheticWire, ...] = ()
    texts: tuple[SyntheticText, ...] = ()

    def __post_init__(self) -> None:
        if self.page_number < 1:
            raise ValueError("Page number must be greater than or equal to 1")

        if not isfinite(self.width) or self.width <= 0:
            raise ValueError("Page width must be positive and finite")

        if not isfinite(self.height) or self.height <= 0:
            raise ValueError("Page height must be positive and finite")

        primitive_ids = [
            *(symbol.id for symbol in self.symbols),
            *(wire.id for wire in self.wires),
            *(text.id for text in self.texts),
        ]

        if len(primitive_ids) != len(set(primitive_ids)):
            raise ValueError("Synthetic page primitive ids must be unique")


@dataclass(frozen=True, slots=True)
class SyntheticDocument:
    """A synthetic PDF document belonging to an electrical project."""

    id: str
    filename: str
    pages: tuple[SyntheticPage, ...]

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Synthetic document id must not be empty")

        if not self.filename.strip():
            raise ValueError("Synthetic document filename must not be empty")

        if not self.filename.lower().endswith(".pdf"):
            raise ValueError("Synthetic document filename must end with .pdf")

        if not self.pages:
            raise ValueError("Synthetic document must contain at least one page")

        page_numbers = [page.page_number for page in self.pages]

        if len(page_numbers) != len(set(page_numbers)):
            raise ValueError("Synthetic document page numbers must be unique")


@dataclass(frozen=True, slots=True)
class IOScheduleRow:
    """One intentionally authored row in a synthetic I/O schedule."""

    signal: str
    plc_address: str
    description: str

    def __post_init__(self) -> None:
        if not self.signal.strip():
            raise ValueError("I/O schedule signal must not be empty")

        if not self.plc_address.strip():
            raise ValueError("I/O schedule PLC address must not be empty")


@dataclass(frozen=True, slots=True)
class IOSchedule:
    """A structured I/O schedule included in a synthetic project."""

    id: str
    filename: str
    rows: tuple[IOScheduleRow, ...]

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("I/O schedule id must not be empty")

        if not self.filename.strip():
            raise ValueError("I/O schedule filename must not be empty")

        if not self.filename.lower().endswith(".csv"):
            raise ValueError("I/O schedule filename must end with .csv")


@dataclass(frozen=True, slots=True)
class ExpectedFinding:
    """A deterministic rule result expected from a synthetic project."""

    rule_id: str

    def __post_init__(self) -> None:
        if not self.rule_id.strip():
            raise ValueError("Expected finding rule_id must not be empty")


@dataclass(frozen=True, slots=True)
class SyntheticProject:
    """A complete synthetic electrical project used as controlled test input."""

    id: str
    documents: tuple[SyntheticDocument, ...]
    schedules: tuple[IOSchedule, ...] = ()
    expected_findings: tuple[ExpectedFinding, ...] = ()

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Synthetic project id must not be empty")

        if not self.documents:
            raise ValueError("Synthetic project must contain at least one document")

        document_ids = [document.id for document in self.documents]
        document_filenames = [document.filename for document in self.documents]
        schedule_ids = [schedule.id for schedule in self.schedules]
        schedule_filenames = [schedule.filename for schedule in self.schedules]

        if len(document_ids) != len(set(document_ids)):
            raise ValueError("Synthetic project document ids must be unique")

        if len(document_filenames) != len(set(document_filenames)):
            raise ValueError("Synthetic project document filenames must be unique")

        if len(schedule_ids) != len(set(schedule_ids)):
            raise ValueError("Synthetic project schedule ids must be unique")

        if len(schedule_filenames) != len(set(schedule_filenames)):
            raise ValueError("Synthetic project schedule filenames must be unique")
