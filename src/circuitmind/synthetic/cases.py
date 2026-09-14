"""Deterministic synthetic electrical project definitions."""

from circuitmind.synthetic.spec import (
    IOSchedule,
    IOScheduleRow,
    SyntheticDocument,
    SyntheticPage,
    SyntheticPoint,
    SyntheticProject,
    SyntheticProjectCase,
    SyntheticSymbol,
    SyntheticText,
    SyntheticWire,
)

PAGE_WIDTH = 842.0
PAGE_HEIGHT = 595.0


def good_digital_input_case() -> SyntheticProjectCase:
    """Build a small internally consistent digital-input project."""

    control_document = SyntheticDocument(
        id="control",
        filename="control.pdf",
        pages=(
            SyntheticPage(
                page_number=1,
                width=PAGE_WIDTH,
                height=PAGE_HEIGHT,
                symbols=(
                    SyntheticSymbol(
                        id="sensor-b101",
                        kind="sensor",
                        label="-B101",
                        position=SyntheticPoint(120.0, 280.0),
                        width=80.0,
                        height=40.0,
                    ),
                    SyntheticSymbol(
                        id="terminal-x1-1",
                        kind="terminal",
                        label="-X1:1",
                        position=SyntheticPoint(340.0, 285.0),
                        width=60.0,
                        height=30.0,
                    ),
                ),
                wires=(
                    SyntheticWire(
                        id="wire-b101-x1-1",
                        start=SyntheticPoint(200.0, 300.0),
                        end=SyntheticPoint(340.0, 300.0),
                    ),
                ),
                texts=(
                    SyntheticText(
                        id="signal-name",
                        text="B101_HOME",
                        position=SyntheticPoint(220.0, 315.0),
                    ),
                    SyntheticText(
                        id="description",
                        text="Conveyor home sensor",
                        position=SyntheticPoint(120.0, 350.0),
                    ),
                ),
            ),
        ),
    )

    plc_io_document = SyntheticDocument(
        id="plc-io",
        filename="plc_io.pdf",
        pages=(
            SyntheticPage(
                page_number=1,
                width=PAGE_WIDTH,
                height=PAGE_HEIGHT,
                symbols=(
                    SyntheticSymbol(
                        id="terminal-x1-1",
                        kind="terminal",
                        label="-X1:1",
                        position=SyntheticPoint(120.0, 285.0),
                        width=60.0,
                        height=30.0,
                    ),
                    SyntheticSymbol(
                        id="plc-input",
                        kind="plc_input",
                        label="-A1",
                        position=SyntheticPoint(340.0, 280.0),
                        width=100.0,
                        height=40.0,
                    ),
                ),
                wires=(
                    SyntheticWire(
                        id="wire-x1-1-plc",
                        start=SyntheticPoint(180.0, 300.0),
                        end=SyntheticPoint(340.0, 300.0),
                    ),
                ),
                texts=(
                    SyntheticText(
                        id="signal-name",
                        text="B101_HOME",
                        position=SyntheticPoint(220.0, 315.0),
                    ),
                    SyntheticText(
                        id="plc-address",
                        text="I2.3",
                        position=SyntheticPoint(370.0, 315.0),
                    ),
                    SyntheticText(
                        id="description",
                        text="Conveyor home sensor",
                        position=SyntheticPoint(340.0, 350.0),
                    ),
                ),
            ),
        ),
    )

    io_schedule = IOSchedule(
        id="io",
        filename="io_schedule.csv",
        rows=(
            IOScheduleRow(
                signal="B101_HOME",
                plc_address="I2.3",
                description="Conveyor home sensor",
            ),
        ),
    )

    project = SyntheticProject(
        id="good_digital_input_project",
        documents=(control_document, plc_io_document),
        schedules=(io_schedule,),
    )

    return SyntheticProjectCase(
        project=project,
        expected_findings=(),
    )
