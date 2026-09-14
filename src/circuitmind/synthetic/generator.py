"""Whole-project generation for deterministic synthetic electrical cases."""

import shutil
from dataclasses import dataclass
from pathlib import Path

from circuitmind.synthetic.manifest import write_case_manifest
from circuitmind.synthetic.pdf import write_pdf_document
from circuitmind.synthetic.schedule import write_io_schedule
from circuitmind.synthetic.spec import SyntheticProjectCase

PROJECT_DIRECTORY_NAME = "project"
DRAWINGS_DIRECTORY_NAME = "drawings"


@dataclass(frozen=True, slots=True)
class GeneratedSyntheticCase:
    """Paths produced when one synthetic project case is generated."""

    case_directory: Path
    project_directory: Path
    drawings_directory: Path
    document_paths: tuple[Path, ...]
    schedule_paths: tuple[Path, ...]
    manifest_path: Path


def generate_project_case(
    case: SyntheticProjectCase,
    output_root: Path,
) -> GeneratedSyntheticCase:
    """Generate all source artifacts and oracle data for one synthetic case."""

    _require_safe_directory_name(case.project.id)

    for document in case.project.documents:
        _require_safe_filename(document.filename)

    for schedule in case.project.schedules:
        _require_safe_filename(schedule.filename)

    case_directory = output_root / case.project.id

    if case_directory.exists():
        shutil.rmtree(case_directory)

    project_directory = case_directory / PROJECT_DIRECTORY_NAME
    drawings_directory = project_directory / DRAWINGS_DIRECTORY_NAME

    document_paths = tuple(
        write_pdf_document(
            document,
            drawings_directory,
        )
        for document in case.project.documents
    )

    schedule_paths = tuple(
        write_io_schedule(
            schedule,
            project_directory,
        )
        for schedule in case.project.schedules
    )

    manifest_path = write_case_manifest(
        case,
        case_directory,
    )

    return GeneratedSyntheticCase(
        case_directory=case_directory,
        project_directory=project_directory,
        drawings_directory=drawings_directory,
        document_paths=document_paths,
        schedule_paths=schedule_paths,
        manifest_path=manifest_path,
    )


def _require_safe_directory_name(name: str) -> None:
    """Reject names that could escape the requested output directory."""

    if name in {".", ".."} or "/" in name or "\\" in name:
        raise ValueError("Synthetic project id must be a safe directory name")


def _require_safe_filename(filename: str) -> None:
    """Reject filenames containing directory traversal or path separators."""

    if filename in {".", ".."} or "/" in filename or "\\" in filename:
        raise ValueError("Synthetic artifact filename must not contain a path")
