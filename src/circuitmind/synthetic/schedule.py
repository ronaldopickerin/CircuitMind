"""CSV rendering for synthetic electrical project I/O schedules."""

import csv
from pathlib import Path

from circuitmind.synthetic.spec import IOSchedule

IO_SCHEDULE_COLUMNS = (
    "signal",
    "plc_address",
    "description",
)


def write_io_schedule(
    schedule: IOSchedule,
    output_directory: Path,
) -> Path:
    """Render an I/O schedule as a deterministic UTF-8 CSV file."""

    output_directory.mkdir(parents=True, exist_ok=True)

    output_path = output_directory / schedule.filename

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=IO_SCHEDULE_COLUMNS,
            lineterminator="\n",
        )

        writer.writeheader()

        for row in schedule.rows:
            writer.writerow(
                {
                    "signal": row.signal,
                    "plc_address": row.plc_address,
                    "description": row.description,
                }
            )

    return output_path
