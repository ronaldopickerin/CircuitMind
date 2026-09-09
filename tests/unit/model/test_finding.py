import pytest

from circuitmind.model.finding import Finding, Severity
from circuitmind.model.geometry import BoundingBox
from circuitmind.model.source import SourceReference


def make_page_source(page_number: int = 1) -> SourceReference:
    return SourceReference(
        document_id="schematic.pdf",
        page_number=page_number,
        bounding_box=BoundingBox(
            x_min=100.0,
            y_min=200.0,
            x_max=150.0,
            y_max=250.0,
        ),
    )


def make_row_source(row_number: int = 2) -> SourceReference:
    return SourceReference(
        document_id="io-schedule.csv",
        row_number=row_number,
    )


def test_finding_accepts_valid_data() -> None:
    finding = Finding(
        rule_id="CM-R001",
        severity=Severity.ERROR,
        title="Duplicate PLC address",
        message="I0.2 is assigned to two logical PLC channels.",
        evidence=(
            make_page_source(page_number=2),
            make_page_source(page_number=7),
        ),
    )

    assert finding.rule_id == "CM-R001"
    assert finding.severity is Severity.ERROR
    assert finding.title == "Duplicate PLC address"
    assert len(finding.evidence) == 2


def test_finding_supports_evidence_from_different_source_types() -> None:
    finding = Finding(
        rule_id="CM-R003",
        severity=Severity.WARNING,
        title="I/O schedule mismatch",
        message="I0.2 differs between the schematic and I/O schedule.",
        evidence=(
            make_page_source(page_number=4),
            make_row_source(row_number=14),
        ),
    )

    assert finding.evidence[0].page_number == 4
    assert finding.evidence[1].row_number == 14


def test_finding_rejects_empty_rule_id() -> None:
    with pytest.raises(ValueError, match="rule_id"):
        Finding(
            rule_id=" ",
            severity=Severity.ERROR,
            title="Duplicate PLC address",
            message="I0.2 is assigned twice.",
            evidence=(make_page_source(),),
        )


def test_finding_rejects_empty_title() -> None:
    with pytest.raises(ValueError, match="title"):
        Finding(
            rule_id="CM-R001",
            severity=Severity.ERROR,
            title=" ",
            message="I0.2 is assigned twice.",
            evidence=(make_page_source(),),
        )


def test_finding_rejects_empty_message() -> None:
    with pytest.raises(ValueError, match="message"):
        Finding(
            rule_id="CM-R001",
            severity=Severity.ERROR,
            title="Duplicate PLC address",
            message=" ",
            evidence=(make_page_source(),),
        )


def test_finding_requires_evidence() -> None:
    with pytest.raises(ValueError, match="at least one"):
        Finding(
            rule_id="CM-R001",
            severity=Severity.ERROR,
            title="Duplicate PLC address",
            message="I0.2 is assigned twice.",
            evidence=(),
        )


def test_finding_rejects_duplicate_evidence() -> None:
    source = make_page_source()

    with pytest.raises(ValueError, match="duplicate evidence"):
        Finding(
            rule_id="CM-R001",
            severity=Severity.ERROR,
            title="Duplicate PLC address",
            message="I0.2 is assigned twice.",
            evidence=(
                source,
                source,
            ),
        )


def test_severity_has_expected_values() -> None:
    assert Severity.INFO.value == "info"
    assert Severity.WARNING.value == "warning"
    assert Severity.ERROR.value == "error"
