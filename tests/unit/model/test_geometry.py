import pytest

from circuitmind.model.geometry import BoundingBox, Point2D


def test_point_accepts_finite_coordinates() -> None:
    point = Point2D(x=10.5, y=20.25)

    assert point.x == 10.5
    assert point.y == 20.25


def test_point_rejects_non_finite_coordinates() -> None:
    with pytest.raises(ValueError, match="finite"):
        Point2D(x=float("nan"), y=10.0)


def test_bounding_box_accepts_valid_coordinates() -> None:
    box = BoundingBox(
        x_min=10.0,
        y_min=20.0,
        x_max=30.0,
        y_max=40.0,
    )

    assert box.x_min == 10.0
    assert box.y_max == 40.0


def test_bounding_box_rejects_reversed_x_coordinates() -> None:
    with pytest.raises(ValueError, match="x_min"):
        BoundingBox(
            x_min=30.0,
            y_min=20.0,
            x_max=10.0,
            y_max=40.0,
        )


def test_bounding_box_rejects_reversed_y_coordinates() -> None:
    with pytest.raises(ValueError, match="y_min"):
        BoundingBox(
            x_min=10.0,
            y_min=40.0,
            x_max=30.0,
            y_max=20.0,
        )
