"""Tests for whole synthetic electrical project generation."""

from pathlib import Path

import pytest

from circuitmind.synthetic.cases import good_digital_input_case
from circuitmind.synthetic.generator import generate_project_case
from circuitmind.synthetic.spec import (
    SyntheticDocument,
    SyntheticPage,
    SyntheticProject,
    SyntheticProjectCase,
)


def test_generate_project_case_creates_expected_layout(
    tmp_path: Path,
) -> None:
    case = good_digital_input_case()

    generated = generate_project_case(
        case,
        tmp_path,
    )

    assert generated.case_directory == (tmp_path / "good_digital_input_project")

    assert generated.project_directory == (tmp_path / "good_digital_input_project" / "project")

    assert generated.drawings_directory == (
        tmp_path / "good_digital_input_project" / "project" / "drawings"
    )

    assert {path.name for path in generated.document_paths} == {
        "control.pdf",
        "plc_io.pdf",
    }

    assert {path.name for path in generated.schedule_paths} == {
        "io_schedule.csv",
    }

    assert generated.manifest_path.name == "manifest.json"


def test_generate_project_case_creates_all_files(
    tmp_path: Path,
) -> None:
    case = good_digital_input_case()

    generated = generate_project_case(
        case,
        tmp_path,
    )

    assert all(path.is_file() for path in generated.document_paths)
    assert all(path.is_file() for path in generated.schedule_paths)
    assert generated.manifest_path.is_file()


def test_manifest_is_outside_ingested_project_directory(
    tmp_path: Path,
) -> None:
    case = good_digital_input_case()

    generated = generate_project_case(
        case,
        tmp_path,
    )

    assert generated.manifest_path.parent == generated.case_directory
    assert generated.manifest_path.parent != generated.project_directory

    project_files = {path.name for path in generated.project_directory.rglob("*") if path.is_file()}

    assert "manifest.json" not in project_files


def test_regeneration_removes_stale_artifacts(
    tmp_path: Path,
) -> None:
    case = good_digital_input_case()

    generated = generate_project_case(
        case,
        tmp_path,
    )

    stale_file = generated.project_directory / "obsolete.pdf"
    stale_file.write_bytes(b"old synthetic artifact")

    assert stale_file.exists()

    regenerated = generate_project_case(
        case,
        tmp_path,
    )

    assert not stale_file.exists()
    assert regenerated.manifest_path.is_file()


@pytest.mark.parametrize(
    "project_id",
    [
        "../outside",
        "..\\outside",
        ".",
        "..",
    ],
)
def test_generator_rejects_unsafe_project_ids(
    tmp_path: Path,
    project_id: str,
) -> None:
    case = SyntheticProjectCase(
        project=SyntheticProject(
            id=project_id,
            documents=(
                SyntheticDocument(
                    id="drawing",
                    filename="drawing.pdf",
                    pages=(
                        SyntheticPage(
                            page_number=1,
                            width=842.0,
                            height=595.0,
                        ),
                    ),
                ),
            ),
        ),
    )

    with pytest.raises(
        ValueError,
        match="safe directory name",
    ):
        generate_project_case(
            case,
            tmp_path,
        )


def test_generated_case_is_reproducible_across_output_directories(
    tmp_path: Path,
) -> None:
    case = good_digital_input_case()

    first = generate_project_case(
        case,
        tmp_path / "first",
    )

    second = generate_project_case(
        case,
        tmp_path / "second",
    )

    first_files = {
        path.relative_to(first.case_directory): path.read_bytes()
        for path in first.case_directory.rglob("*")
        if path.is_file()
    }

    second_files = {
        path.relative_to(second.case_directory): path.read_bytes()
        for path in second.case_directory.rglob("*")
        if path.is_file()
    }

    assert first_files == second_files
