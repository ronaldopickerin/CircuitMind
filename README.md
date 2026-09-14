# CircuitMind

[![CI](https://github.com/ronaldopickerin/CircuitMind/actions/workflows/ci.yml/badge.svg)](https://github.com/ronaldopickerin/CircuitMind/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![Status](https://img.shields.io/badge/status-early%20development-orange)

CircuitMind is a deterministic electrical engineering design-review platform for industrial electrical and controls projects.

The project is being built to analyse complete drawing sets and related schedules, reconstruct a machine-readable electrical model, run engineering validation rules, and return traceable findings linked back to the source documents. AI may later assist with ambiguous interpretation and explanation, but deterministic engineering logic remains authoritative wherever possible.

## Why CircuitMind

Electrical design review often requires engineers to compare information spread across schematics, PLC I/O pages, terminal information, cable schedules, and other project documents. Many errors are not visible in one drawing alone.

CircuitMind is intended to reason across the project as a whole:

```text
Project files
    ↓
document classification
    ↓
source extraction
    ↓
entity resolution + connectivity reconstruction
    ↓
CircuitModel
    ↓
deterministic validation rules
    ↓
traceable findings
```

## V0.1 Scope

V0.1 is intentionally narrow and focuses on building a rigorous deterministic foundation before adding broader CAD support or AI-assisted interpretation.

Current and planned V0.1 capabilities include:

- typed electrical domain modelling
- separation of logical electrical objects from graphical occurrences
- source provenance and drawing-page references
- structured PLC addresses and channels
- electrical nets and wire segments
- deterministic synthetic electrical project fixtures
- vector-PDF and CSV test artifacts
- future extraction from machine-generated vector PDFs
- future cross-document entity resolution and connectivity reconstruction
- deterministic engineering validation rules
- structured findings suitable for CLI or JSON output

Initial rule targets are:

| Rule | Purpose |
| --- | --- |
| `CM-R001` | Duplicate PLC address |
| `CM-R002` | Dangling or unresolved connection |
| `CM-R003` | Schematic vs I/O schedule mismatch |

## Current Development Status

The core electrical domain model is implemented and the current milestone is the deterministic synthetic project test bench.

The benchmark contains four controlled project cases:

| Synthetic project | Expected finding |
| --- | --- |
| `good_digital_input_project` | none |
| `duplicate_plc_address_project` | `CM-R001` |
| `dangling_connection_project` | `CM-R002` |
| `schedule_mismatch_project` | `CM-R003` |

These fixtures will later be passed through the real extraction and validation pipeline so detected findings can be compared against known expected results.

## Synthetic Verification Bench

The synthetic generator is deliberately independent of `CircuitModel` and the future parser. It describes external source artifacts rather than rendering CircuitMind's internal interpretation back into PDFs.

```text
Synthetic source specification
        ↓
PDF drawings + CSV schedules
        ↓
future CircuitMind extraction
        ↓
entity resolution + connectivity
        ↓
CircuitModel
        ↓
validation rules
        ↓
actual findings
        ↓
compare with manifest oracle
```

The generated project input and the expected-result manifest are kept separate so the expected answer cannot leak into the system under test.

See [`docs/synthetic-projects.md`](docs/synthetic-projects.md) for the fixture architecture and generated layout.

## Engineering Principles

CircuitMind is developed around a few explicit principles:

- deterministic engineering logic where possible
- project-level analysis rather than isolated-PDF checking
- traceable findings with source provenance
- logical electrical entities separated from graphical occurrences
- raw source evidence separated from interpreted semantics
- independent synthetic fixtures to avoid circular testing
- reproducible outputs and regression tests
- strict typing, linting, formatting, and automated CI
- no confidential employer or customer material

## Repository Structure

```text
src/circuitmind/
├── model/          # canonical electrical domain model
└── synthetic/      # independent synthetic source-fixture system

tests/
└── unit/

docs/
├── domain-model.md
├── synthetic-projects.md
├── roadmap.md
├── decisions/
└── ideas/
```

## Development

Requirements:

- Python 3.12+
- [`uv`](https://docs.astral.sh/uv/)

Clone and install the development environment:

```bash
git clone https://github.com/ronaldopickerin/CircuitMind.git
cd CircuitMind
uv sync --locked --dev
```

Run the full quality gate:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

The same checks run in GitHub Actions for pull requests.

## Documentation

The repository documentation acts as the long-term project knowledge base:

- [`docs/domain-model.md`](docs/domain-model.md) — electrical domain model and modelling boundaries
- [`docs/synthetic-projects.md`](docs/synthetic-projects.md) — deterministic benchmark architecture and fixture format
- [`docs/roadmap.md`](docs/roadmap.md) — high-level development direction
- [`docs/decisions/`](docs/decisions/) — architecture decisions and rationale
- [`docs/ideas/`](docs/ideas/) — promising concepts not yet scheduled for implementation

## Roadmap

Near-term work after the synthetic benchmark is stable:

1. extract structured information from vector PDFs and schedules
2. preserve provenance and uncertainty during extraction
3. resolve entities across documents and pages
4. reconstruct canonical project-level connectivity
5. implement deterministic validation rules
6. expose findings through CLI/JSON interfaces

Longer-term directions include configurable company/project drawing profiles, broader CAD conventions, engineer-facing review tooling, and selective AI assistance for ambiguous source interpretation.

## Confidentiality

CircuitMind's public fixtures and tests use generic synthetic data only. Employer drawings, customer material, proprietary project content, and confidential drawing conventions must not be committed to this repository.
