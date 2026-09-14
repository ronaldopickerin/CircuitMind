"""Tests for synthetic I/O schedule CSV rendering."""

import csv
from pathlib import Path

from circuitmind.synthetic.cases import good_digital_input_case
from circuitmind.synthetic.schedule import IO_SCHEDULE_COLUMNS, write_io_schedule
from circuitmind.synthetic.spec import IOSchedule, IOScheduleRow


def test_write_io_schedule_creates_expected_file(tmp_path: Path) -> None:
    case = good_digital_input_case()
    schedule = case.project.schedules[0]

    output_path = write_io_schedule(schedule, tmp_path)

    assert output_path == tmp_path / "io_schedule.csv"
    assert output_path.is_file()


def test_write_io_schedule_uses_stable_column_order(tmp_path: Path) -> None:
    case = good_digital_input_case()
    schedule = case.project.schedules[0]

    output_path = write_io_schedule(schedule, tmp_path)

    with output_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)

    assert tuple(header) == IO_SCHEDULE_COLUMNS


def test_write_io_schedule_renders_expected_good_project_row(
    tmp_path: Path,
) -> None:
    case = good_digital_input_case()
    schedule = case.project.schedules[0]

    output_path = write_io_schedule(schedule, tmp_path)

    with output_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    assert rows == [
        {
            "signal": "B101_HOME",
            "plc_address": "I2.3",
            "description": "Conveyor home sensor",
        }
    ]


def test_write_io_schedule_preserves_source_row_order(tmp_path: Path) -> None:
    schedule = IOSchedule(
        id="io",
        filename="io_schedule.csv",
        rows=(
            IOScheduleRow(
                signal="SIGNAL_B",
                plc_address="I1.1",
                description="Second source row",
            ),
            IOScheduleRow(
                signal="SIGNAL_A",
                plc_address="I1.0",
                description="First alphabetically",
            ),
        ),
    )

    output_path = write_io_schedule(schedule, tmp_path)

    with output_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as csv_file:
        rows = list(csv.DictReader(csv_file))

    assert [row["signal"] for row in rows] == [
        "SIGNAL_B",
        "SIGNAL_A",
    ]


def test_write_io_schedule_handles_csv_escaping(tmp_path: Path) -> None:
    schedule = IOSchedule(
        id="io",
        filename="io_schedule.csv",
        rows=(
            IOScheduleRow(
                signal="B101_HOME",
                plc_address="I2.3",
                description="Sensor, conveyor home position",
            ),
        ),
    )

    output_path = write_io_schedule(schedule, tmp_path)

    with output_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as csv_file:
        rows = list(csv.DictReader(csv_file))

    assert rows[0]["description"] == "Sensor, conveyor home position"


def test_write_io_schedule_empty_schedule_contains_header_only(
    tmp_path: Path,
) -> None:
    schedule = IOSchedule(
        id="empty",
        filename="empty.csv",
        rows=(),
    )

    output_path = write_io_schedule(schedule, tmp_path)

    assert output_path.read_text(encoding="utf-8") == ("signal,plc_address,description\n")


def test_write_io_schedule_is_byte_stable_for_same_schedule(
    tmp_path: Path,
) -> None:
    case = good_digital_input_case()
    schedule = case.project.schedules[0]

    first_directory = tmp_path / "first"
    second_directory = tmp_path / "second"

    first_path = write_io_schedule(schedule, first_directory)
    second_path = write_io_schedule(schedule, second_directory)

    assert first_path.read_bytes() == second_path.read_bytes()
