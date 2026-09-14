"""Tests for deterministic project source discovery."""

from pathlib import Path

import pytest

from circuitmind.extraction.project import (
    DiscoveredProjectSources,
    discover_project_sources,
)
from circuitmind.synthetic.cases import good_digital_input_case
from circuitmind.synthetic.generator import generate_project_case


def test_discover_generated_synthetic_project_sources(tmp_path: Path) -> None:
    generated = generate_project_case(
        good_digital_input_case(),
        tmp_path,
    )

    discovered = discover_project_sources(
        generated.project_directory,
    )

    assert discovered.pdf_paths == (
        "drawings/control.pdf",
        "drawings/plc_io.pdf",
    )
    assert discovered.csv_paths == ("io_schedule.csv",)


def test_discovery_does_not_escape_project_directory(tmp_path: Path) -> None:
    generated = generate_project_case(
        good_digital_input_case(),
        tmp_path,
    )

    outside_pdf = generated.case_directory / "oracle.pdf"
    outside_pdf.write_bytes(b"not part of the project")

    discovered = discover_project_sources(
        generated.project_directory,
    )

    assert "oracle.pdf" not in discovered.source_paths


def test_discovery_does_not_include_manifest_oracle(tmp_path: Path) -> None:
    generated = generate_project_case(
        good_digital_input_case(),
        tmp_path,
    )

    assert generated.manifest_path.is_file()

    discovered = discover_project_sources(
        generated.project_directory,
    )

    assert "manifest.json" not in discovered.source_paths


def test_discovery_returns_project_relative_posix_paths(
    tmp_path: Path,
) -> None:
    drawings_directory = tmp_path / "nested" / "drawings"
    drawings_directory.mkdir(parents=True)

    source_file = drawings_directory / "control.pdf"
    source_file.write_bytes(b"pdf")

    discovered = discover_project_sources(tmp_path)

    assert discovered.pdf_paths == ("nested/drawings/control.pdf",)
    assert "\\" not in discovered.pdf_paths[0]


def test_discovery_uses_deterministic_order(tmp_path: Path) -> None:
    drawings_directory = tmp_path / "drawings"
    drawings_directory.mkdir()

    (drawings_directory / "zeta.pdf").write_bytes(b"pdf")
    (drawings_directory / "Beta.PDF").write_bytes(b"pdf")
    (drawings_directory / "alpha.pdf").write_bytes(b"pdf")

    (tmp_path / "z_schedule.csv").write_text("", encoding="utf-8")
    (tmp_path / "A_schedule.CSV").write_text("", encoding="utf-8")

    discovered = discover_project_sources(tmp_path)

    assert discovered.pdf_paths == (
        "drawings/alpha.pdf",
        "drawings/Beta.PDF",
        "drawings/zeta.pdf",
    )
    assert discovered.csv_paths == (
        "A_schedule.CSV",
        "z_schedule.csv",
    )


def test_discovery_ignores_unsupported_files(tmp_path: Path) -> None:
    (tmp_path / "notes.txt").write_text("notes", encoding="utf-8")
    (tmp_path / "manifest.json").write_text("{}", encoding="utf-8")
    (tmp_path / "image.png").write_bytes(b"png")
    (tmp_path / "drawing.pdf").write_bytes(b"pdf")

    discovered = discover_project_sources(tmp_path)

    assert discovered.pdf_paths == ("drawing.pdf",)
    assert discovered.csv_paths == ()


def test_discovery_allows_project_with_no_supported_sources(
    tmp_path: Path,
) -> None:
    (tmp_path / "notes.txt").write_text("notes", encoding="utf-8")

    discovered = discover_project_sources(tmp_path)

    assert discovered == DiscoveredProjectSources()


def test_discovery_rejects_missing_project_directory(
    tmp_path: Path,
) -> None:
    missing_directory = tmp_path / "missing"

    with pytest.raises(FileNotFoundError, match="does not exist"):
        discover_project_sources(missing_directory)


def test_discovery_rejects_file_as_project_directory(
    tmp_path: Path,
) -> None:
    project_file = tmp_path / "project"
    project_file.write_text("not a directory", encoding="utf-8")

    with pytest.raises(NotADirectoryError, match="not a directory"):
        discover_project_sources(project_file)


def test_discovered_sources_reject_wrong_file_types() -> None:
    with pytest.raises(ValueError, match=r"\.pdf"):
        DiscoveredProjectSources(
            pdf_paths=("drawings/control.txt",),
        )


def test_discovered_sources_exposes_all_source_paths() -> None:
    sources = DiscoveredProjectSources(
        pdf_paths=(
            "drawings/control.pdf",
            "drawings/plc_io.pdf",
        ),
        csv_paths=("io_schedule.csv",),
    )

    assert sources.source_paths == (
        "drawings/control.pdf",
        "drawings/plc_io.pdf",
        "io_schedule.csv",
    )


@pytest.mark.parametrize(
    "source_path",
    [
        "/drawings/control.pdf",
        "../control.pdf",
        "drawings/../control.pdf",
        "C:/drawings/control.pdf",
    ],
)
def test_discovered_sources_reject_invalid_source_paths(
    source_path: str,
) -> None:
    with pytest.raises(ValueError):
        DiscoveredProjectSources(
            pdf_paths=(source_path,),
        )
