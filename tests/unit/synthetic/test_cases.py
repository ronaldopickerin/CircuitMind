"""Tests for deterministic synthetic electrical project cases."""

from circuitmind.synthetic.cases import (
    duplicate_plc_address_case,
    good_digital_input_case,
)


def test_good_digital_input_project_contains_multiple_documents() -> None:
    case = good_digital_input_case()
    project = case.project

    assert project.id == "good_digital_input_project"
    assert len(project.documents) == 2
    assert {document.filename for document in project.documents} == {
        "control.pdf",
        "plc_io.pdf",
    }


def test_good_digital_input_project_contains_io_schedule() -> None:
    case = good_digital_input_case()
    project = case.project

    assert len(project.schedules) == 1

    schedule = project.schedules[0]

    assert schedule.filename == "io_schedule.csv"
    assert len(schedule.rows) == 1
    assert schedule.rows[0].signal == "B101_HOME"
    assert schedule.rows[0].plc_address == "I2.3"
    assert schedule.rows[0].description == "Conveyor home sensor"


def test_good_digital_input_project_has_no_expected_findings() -> None:
    case = good_digital_input_case()

    assert case.expected_findings == ()


def test_good_digital_input_project_repeats_terminal_across_drawings() -> None:
    case = good_digital_input_case()
    project = case.project

    control_page = project.documents[0].pages[0]
    plc_page = project.documents[1].pages[0]

    control_labels = {symbol.label for symbol in control_page.symbols}
    plc_labels = {symbol.label for symbol in plc_page.symbols}

    assert "-X1:1" in control_labels
    assert "-X1:1" in plc_labels


def test_good_digital_input_project_repeats_signal_across_sources() -> None:
    case = good_digital_input_case()
    project = case.project

    control_page = project.documents[0].pages[0]
    plc_page = project.documents[1].pages[0]
    schedule = project.schedules[0]

    control_text = {text.text for text in control_page.texts}
    plc_text = {text.text for text in plc_page.texts}

    assert "B101_HOME" in control_text
    assert "B101_HOME" in plc_text
    assert schedule.rows[0].signal == "B101_HOME"


def test_good_digital_input_project_aligns_plc_address_with_schedule() -> None:
    case = good_digital_input_case()
    project = case.project

    plc_page = project.documents[1].pages[0]
    schedule = project.schedules[0]

    plc_text = {text.text for text in plc_page.texts}

    assert schedule.rows[0].plc_address == "I2.3"
    assert "I2.3" in plc_text


def test_duplicate_plc_address_case_expects_cm_r001() -> None:
    case = duplicate_plc_address_case()

    assert tuple(finding.rule_id for finding in case.expected_findings) == ("CM-R001",)


def test_duplicate_plc_address_case_contains_two_distinct_signals() -> None:
    case = duplicate_plc_address_case()
    schedule = case.project.schedules[0]

    assert [row.signal for row in schedule.rows] == [
        "B101_HOME",
        "B102_GUARD_CLOSED",
    ]


def test_duplicate_plc_address_case_duplicates_schedule_address() -> None:
    case = duplicate_plc_address_case()
    schedule = case.project.schedules[0]

    assert [row.plc_address for row in schedule.rows] == [
        "I2.3",
        "I2.3",
    ]


def test_duplicate_plc_address_case_duplicates_address_on_drawing() -> None:
    case = duplicate_plc_address_case()
    plc_page = case.project.documents[1].pages[0]

    addresses = [text.text for text in plc_page.texts if text.text == "I2.3"]

    assert addresses == [
        "I2.3",
        "I2.3",
    ]


def test_duplicate_plc_address_case_keeps_cross_document_signals_aligned() -> None:
    case = duplicate_plc_address_case()
    project = case.project

    control_text = {text.text for text in project.documents[0].pages[0].texts}

    plc_text = {text.text for text in project.documents[1].pages[0].texts}

    schedule_signals = {row.signal for row in project.schedules[0].rows}

    expected_signals = {
        "B101_HOME",
        "B102_GUARD_CLOSED",
    }

    assert expected_signals <= control_text
    assert expected_signals <= plc_text
    assert schedule_signals == expected_signals
