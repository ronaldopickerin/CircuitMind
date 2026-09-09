"""Source provenance for CircuitMind domain entities."""

from dataclasses import dataclass

from circuitmind.model.geometry import BoundingBox


@dataclass(frozen=True, slots=True)
class SourceReference:
    """Location of an entity or finding within a source document."""

    document_id: str
    page_number: int
    bounding_box: BoundingBox | None = None

    def __post_init__(self) -> None:
        if not self.document_id.strip():
            raise ValueError("document_id must not be empty")

        if self.page_number < 1:
            raise ValueError("page_number must be greater than or equal to 1")
