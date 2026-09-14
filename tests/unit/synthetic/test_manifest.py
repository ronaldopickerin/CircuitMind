"""Tests for synthetic project expected-results manifests."""

import json
from pathlib import Path

from circuitmind.synthetic.cases import good_digital_input_case
from circuitmind.synthetic.manifest import (
    MANIFEST_FILENAME,
    MANIFEST_SCHEMA_VERSION,
    write_case_manifest,
)
from circuitmind.synthetic.spec import (
    ExpectedFinding,
    SyntheticProjectCase,
)


def test_write_case_manifest_creates_expected_file(tmp_path: Path) -> None:
    case = good_digital_input_case()

    output_path = write_case_manifest(
        case,
        tmp_path,
    )

    assert output_path == tmp_path / MANIFEST_FILENAME
    assert output_path.is_file()


def test_good_case_manifest_contains_no_expected_findings(
    tmp_path: Path,
) -> None:
    case = good_digital_input_case()

    output_path = write_case_manifest(
        case,
        tmp_path,
    )

    payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert payload == {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "project_id": "good_digital_input_project",
        "expected_findings": [],
    }


def test_manifest_serializes_expected_rule_ids(tmp_path: Path) -> None:
    good_case = good_digital_input_case()

    faulty_case = SyntheticProjectCase(
        project=good_case.project,
        expected_findings=(
            ExpectedFinding(rule_id="CM-R001"),
            ExpectedFinding(rule_id="CM-R003"),
        ),
    )

    output_path = write_case_manifest(
        faulty_case,
        tmp_path,
    )

    payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert payload["expected_findings"] == [
        {"rule_id": "CM-R001"},
        {"rule_id": "CM-R003"},
    ]


def test_manifest_is_byte_stable(tmp_path: Path) -> None:
    case = good_digital_input_case()

    first_path = write_case_manifest(
        case,
        tmp_path / "first",
    )

    second_path = write_case_manifest(
        case,
        tmp_path / "second",
    )

    assert first_path.read_bytes() == second_path.read_bytes()
