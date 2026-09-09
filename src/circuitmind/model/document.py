"""Source document models for CircuitMind."""

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True, slots=True)
class Document:
    """A source engineering document analysed by CircuitMind."""

    id: str
    name: str

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Document id must not be empty")

        if not self.name.strip():
            raise ValueError("Document name must not be empty")


@dataclass(frozen=True, slots=True)
class DrawingPage:
    """A page belonging to a source engineering document."""

    document_id: str
    page_number: int
    width: float
    height: float

    def __post_init__(self) -> None:
        if not self.document_id.strip():
            raise ValueError("document_id must not be empty")

        if self.page_number < 1:
            raise ValueError("page_number must be greater than or equal to 1")

        if not isfinite(self.width) or self.width <= 0:
            raise ValueError("Page width must be finite and greater than zero")

        if not isfinite(self.height) or self.height <= 0:
            raise ValueError("Page height must be finite and greater than zero")
