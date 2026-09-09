"""Geometry primitives used by CircuitMind domain models."""

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True, slots=True)
class Point2D:
    """A two-dimensional point in drawing coordinates."""

    x: float
    y: float

    def __post_init__(self) -> None:
        if not isfinite(self.x) or not isfinite(self.y):
            raise ValueError("Point coordinates must be finite")


@dataclass(frozen=True, slots=True)
class BoundingBox:
    """Axis-aligned rectangular region in drawing coordinates."""

    x_min: float
    y_min: float
    x_max: float
    y_max: float

    def __post_init__(self) -> None:
        coordinates = (self.x_min, self.y_min, self.x_max, self.y_max)

        if not all(isfinite(value) for value in coordinates):
            raise ValueError("Bounding box coordinates must be finite")

        if self.x_min > self.x_max:
            raise ValueError("x_min must not be greater than x_max")

        if self.y_min > self.y_max:
            raise ValueError("y_min must not be greater than y_max")
