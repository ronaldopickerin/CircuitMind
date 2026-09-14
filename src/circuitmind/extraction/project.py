"""Deterministic discovery of source files within an electrical project."""

from dataclasses import dataclass
from pathlib import Path

from circuitmind.extraction.spec import _require_relative_source_path


@dataclass(frozen=True, slots=True)
class DiscoveredProjectSources:
    """Project-relative source files supported by the extraction layer."""

    pdf_paths: tuple[str, ...] = ()
    csv_paths: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for path in self.pdf_paths:
            _require_relative_source_path(path)

        for path in self.csv_paths:
            _require_relative_source_path(path)

        if any(not path.lower().endswith(".pdf") for path in self.pdf_paths):
            raise ValueError("Discovered PDF paths must end with .pdf")

        if any(not path.lower().endswith(".csv") for path in self.csv_paths):
            raise ValueError("Discovered CSV paths must end with .csv")

        all_paths = (*self.pdf_paths, *self.csv_paths)

        if len(all_paths) != len(set(all_paths)):
            raise ValueError("Discovered project source paths must be unique")

    @property
    def source_paths(self) -> tuple[str, ...]:
        """Return every discovered source path in deterministic type order."""
        return (*self.pdf_paths, *self.csv_paths)


def discover_project_sources(
    project_directory: Path,
) -> DiscoveredProjectSources:
    """Discover supported files beneath one project input directory.

    Returned paths are relative to ``project_directory`` and always use
    forward slashes. Discovery never traverses the project's parent
    directory, keeping case-level test oracles outside the input boundary.
    """

    if not project_directory.exists():
        raise FileNotFoundError(f"Project directory does not exist: {project_directory}")

    if not project_directory.is_dir():
        raise NotADirectoryError(f"Project path is not a directory: {project_directory}")

    pdf_paths: list[str] = []
    csv_paths: list[str] = []

    for source_path in project_directory.rglob("*"):
        if source_path.is_symlink() or not source_path.is_file():
            continue

        relative_path = source_path.relative_to(project_directory).as_posix()
        suffix = source_path.suffix.casefold()

        if suffix == ".pdf":
            pdf_paths.append(relative_path)
        elif suffix == ".csv":
            csv_paths.append(relative_path)

    return DiscoveredProjectSources(
        pdf_paths=tuple(sorted(pdf_paths, key=_path_sort_key)),
        csv_paths=tuple(sorted(csv_paths, key=_path_sort_key)),
    )


def _path_sort_key(source_path: str) -> tuple[str, str]:
    """Provide deterministic case-insensitive ordering with a stable tie-break."""

    return (source_path.casefold(), source_path)
