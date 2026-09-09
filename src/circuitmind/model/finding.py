"""Validation findings produced by CircuitMind rules."""

from dataclasses import dataclass
from enum import Enum

from circuitmind.model.source import SourceReference


class Severity(Enum):
    """Severity assigned to a CircuitMind validation finding."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class Finding:
    """A structured engineering issue reported by a validation rule."""

    rule_id: str
    severity: Severity
    title: str
    message: str
    evidence: tuple[SourceReference, ...]

    def __post_init__(self) -> None:
        if not self.rule_id.strip():
            raise ValueError("Finding rule_id must not be empty")

        if not self.title.strip():
            raise ValueError("Finding title must not be empty")

        if not self.message.strip():
            raise ValueError("Finding message must not be empty")

        if not self.evidence:
            raise ValueError("Finding must contain at least one evidence reference")

        if len(set(self.evidence)) != len(self.evidence):
            raise ValueError("Finding contains duplicate evidence references")
