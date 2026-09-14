"""Tests for deterministic synthetic electrical project cases."""

from circuitmind.synthetic.cases import good_digital_input_case


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
