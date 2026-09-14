"""Deterministic synthetic electrical project definitions."""

from dataclasses import replace

from circuitmind.synthetic.spec import (
    ExpectedFinding,
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
                        position=SyntheticPoint(370.0, 330.0),
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


def duplicate_plc_address_case() -> SyntheticProjectCase:
    """Build a project where two signals intentionally share one PLC address."""

    good_case = good_digital_input_case()
    project = good_case.project

    control_document = project.documents[0]
    plc_io_document = project.documents[1]
    io_schedule = project.schedules[0]

    control_page = control_document.pages[0]

    duplicate_control_page = replace(
        control_page,
        symbols=control_page.symbols
        + (
            SyntheticSymbol(
                id="sensor-b102",
                kind="sensor",
                label="-B102",
                position=SyntheticPoint(120.0, 160.0),
                width=80.0,
                height=40.0,
            ),
            SyntheticSymbol(
                id="terminal-x1-2",
                kind="terminal",
                label="-X1:2",
                position=SyntheticPoint(340.0, 165.0),
                width=60.0,
                height=30.0,
            ),
        ),
        wires=control_page.wires
        + (
            SyntheticWire(
                id="wire-b102-x1-2",
                start=SyntheticPoint(200.0, 180.0),
                end=SyntheticPoint(340.0, 180.0),
            ),
        ),
        texts=control_page.texts
        + (
            SyntheticText(
                id="signal-name-b102",
                text="B102_GUARD_CLOSED",
                position=SyntheticPoint(220.0, 195.0),
            ),
            SyntheticText(
                id="description-b102",
                text="Guard closed sensor",
                position=SyntheticPoint(120.0, 230.0),
            ),
        ),
    )

    plc_page = plc_io_document.pages[0]

    duplicate_plc_page = replace(
        plc_page,
        symbols=plc_page.symbols
        + (
            SyntheticSymbol(
                id="terminal-x1-2",
                kind="terminal",
                label="-X1:2",
                position=SyntheticPoint(120.0, 165.0),
                width=60.0,
                height=30.0,
            ),
            SyntheticSymbol(
                id="plc-input-b102",
                kind="plc_input",
                label="-A2",
                position=SyntheticPoint(340.0, 160.0),
                width=100.0,
                height=40.0,
            ),
        ),
        wires=plc_page.wires
        + (
            SyntheticWire(
                id="wire-x1-2-plc",
                start=SyntheticPoint(180.0, 180.0),
                end=SyntheticPoint(340.0, 180.0),
            ),
        ),
        texts=plc_page.texts
        + (
            SyntheticText(
                id="signal-name-b102",
                text="B102_GUARD_CLOSED",
                position=SyntheticPoint(220.0, 195.0),
            ),
            SyntheticText(
                id="plc-address-b102",
                text="I2.3",
                position=SyntheticPoint(370.0, 210.0),
            ),
            SyntheticText(
                id="description-b102",
                text="Guard closed sensor",
                position=SyntheticPoint(340.0, 230.0),
            ),
        ),
    )

    duplicate_schedule = replace(
        io_schedule,
        rows=io_schedule.rows
        + (
            IOScheduleRow(
                signal="B102_GUARD_CLOSED",
                plc_address="I2.3",
                description="Guard closed sensor",
            ),
        ),
    )

    duplicate_project = replace(
        project,
        id="duplicate_plc_address_project",
        documents=(
            replace(
                control_document,
                pages=(duplicate_control_page,),
            ),
            replace(
                plc_io_document,
                pages=(duplicate_plc_page,),
            ),
        ),
        schedules=(duplicate_schedule,),
    )

    return SyntheticProjectCase(
        project=duplicate_project,
        expected_findings=(
            ExpectedFinding(
                rule_id="CM-R001",
            ),
        ),
    )


def dangling_connection_case() -> SyntheticProjectCase:
    """Build a project containing one visually disconnected wire endpoint."""

    good_case = good_digital_input_case()
    project = good_case.project

    control_document = project.documents[0]
    plc_io_document = project.documents[1]

    control_page = control_document.pages[0]
    source_wire = control_page.wires[0]

    dangling_wire = replace(
        source_wire,
        end=SyntheticPoint(315.0, 300.0),
    )

    dangling_control_page = replace(
        control_page,
        wires=(dangling_wire,),
    )

    dangling_project = replace(
        project,
        id="dangling_connection_project",
        documents=(
            replace(
                control_document,
                pages=(dangling_control_page,),
            ),
            plc_io_document,
        ),
    )

    return SyntheticProjectCase(
        project=dangling_project,
        expected_findings=(
            ExpectedFinding(
                rule_id="CM-R002",
            ),
        ),
    )


def schedule_mismatch_case() -> SyntheticProjectCase:
    """Build a project where the I/O schedule disagrees with the PLC drawing."""

    good_case = good_digital_input_case()
    project = good_case.project

    io_schedule = project.schedules[0]
    source_row = io_schedule.rows[0]

    mismatched_schedule = replace(
        io_schedule,
        rows=(
            replace(
                source_row,
                plc_address="I2.4",
            ),
        ),
    )

    mismatched_project = replace(
        project,
        id="schedule_mismatch_project",
        schedules=(mismatched_schedule,),
    )

    return SyntheticProjectCase(
        project=mismatched_project,
        expected_findings=(
            ExpectedFinding(
                rule_id="CM-R003",
            ),
        ),
    )


def all_synthetic_cases() -> tuple[SyntheticProjectCase, ...]:
    """Return every built-in synthetic project case in deterministic order."""

    return (
        good_digital_input_case(),
        duplicate_plc_address_case(),
        dangling_connection_case(),
        schedule_mismatch_case(),
    )
