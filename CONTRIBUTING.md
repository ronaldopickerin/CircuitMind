# Contributing to CircuitMind

CircuitMind is in early development and is being built incrementally through focused issues, feature branches, and pull requests.

## Development Setup

Requirements:

- Python 3.12+
- `uv`

Install dependencies with:

```bash
uv sync --locked --dev
```

## Workflow

1. Start from an up-to-date `main` branch.
2. Create a focused branch for one issue or coherent change.
3. Keep implementation, tests, and documentation aligned.
4. Run the full quality gate before opening a pull request.
5. Link the pull request to the relevant GitHub issue.

## Quality Gate

Run:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

All checks should pass before merge.

## Engineering Boundaries

Changes should preserve the project's current architectural principles:

- prefer deterministic engineering logic where practical
- analyse complete project/drawing sets rather than isolated files
- preserve source provenance
- keep logical electrical entities separate from graphical occurrences
- keep raw source evidence separate from interpreted semantics
- keep synthetic fixtures independent of `CircuitModel` and extraction code
- avoid circular tests where the implementation supplies its own expected answer

Significant architecture changes should be documented under `docs/decisions/`.

## Confidentiality

Do not commit confidential employer or customer material.

This includes real customer drawings, proprietary project files, confidential schedules, internal documents, or copied drawing conventions that are not suitable for public release. Use generic synthetic fixtures for tests and examples.
