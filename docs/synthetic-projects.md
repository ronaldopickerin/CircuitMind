# Synthetic Electrical Projects

CircuitMind includes a deterministic synthetic-project generator used as controlled test infrastructure for future extraction, entity-resolution, connectivity, and validation work.

The synthetic projects model complete electrical project inputs rather than isolated PDF files. A case may contain multiple drawing documents together with structured schedules, allowing CircuitMind to test reasoning across project sources.

## Purpose

The synthetic benchmark provides known, non-confidential electrical source artifacts with controlled engineering faults.

The intended future verification flow is:

```text
Synthetic source specification
        ↓
PDF drawings + CSV schedules
        ↓
CircuitMind extraction
        ↓
cross-document entity resolution
        ↓
connectivity reconstruction
        ↓
CircuitModel
        ↓
deterministic engineering rules
        ↓
actual findings
        ↓
compare with manifest oracle
```

The PDF generator itself is test infrastructure and is not part of CircuitMind's product functionality.

## Architectural Boundary

The synthetic package is intentionally independent of `circuitmind.model`.

Synthetic specifications describe only information that could exist in external project files, including:

- PDF documents and pages
- symbol geometry and visible labels
- wire geometry and source visual metadata
- visible text such as signal names and PLC addresses
- CSV I/O schedule rows

They do not embed CircuitMind's interpreted electrical truth.

For example, synthetic source objects must not directly encode concepts such as:

- resolved electrical nets
- canonical devices
- `same_device`
- inferred connectivity
- `dangling=True`
- expected parser results

Those are conclusions that future CircuitMind stages must derive from the generated artifacts.

Expected validation results are stored separately in `SyntheticProjectCase`.

## Source Specification

The principal relationship is:

```text
SyntheticProjectCase
├── SyntheticProject
│   ├── SyntheticDocument
│   │   └── SyntheticPage
│   │       ├── SyntheticSymbol
│   │       ├── SyntheticWire
│   │       └── SyntheticText
│   └── IOSchedule
│       └── IOScheduleRow
│
└── expected_findings
```

`SyntheticProject` represents the external engineering project.

`expected_findings` represents test-oracle information and is deliberately kept outside the project that CircuitMind will eventually ingest.

## Generated Layout

Generated fixtures are written beneath `build/synthetic/`.

For example:

```text
build/synthetic/
├── good_digital_input_project/
│   ├── project/
│   │   ├── drawings/
│   │   │   ├── control.pdf
│   │   │   └── plc_io.pdf
│   │   └── io_schedule.csv
│   └── manifest.json
│
├── duplicate_plc_address_project/
│   └── ...
│
├── dangling_connection_project/
│   └── ...
│
└── schedule_mismatch_project/
    └── ...
```

Only the `project/` directory represents future CircuitMind input.

`manifest.json` is intentionally stored outside that directory so the expected result cannot leak into the system under test.

Generated files are build artifacts and are not committed as the primary source of truth.

## Initial Benchmark Cases

CircuitMind V0.1 defines four synthetic project cases.

### `good_digital_input_project`

A consistent digital-input project containing:

- `control.pdf`
- `plc_io.pdf`
- `io_schedule.csv`

The same signal and PLC address agree across the relevant sources.

Expected findings: none.

### `duplicate_plc_address_project`

Two distinct logical signals deliberately use the same PLC address while the drawing set and schedule remain mutually consistent.

Expected finding: `CM-R001`.

This isolates a duplicate-address engineering fault rather than a cross-document mismatch.

### `dangling_connection_project`

A control-drawing wire deliberately stops before its intended terminal.

The fault is represented only through source geometry. The specification does not contain a semantic `dangling` flag.

Expected finding: `CM-R002`.

### `schedule_mismatch_project`

The PLC drawing represents `B101_HOME → I2.3` while the CSV I/O schedule represents `B101_HOME → I2.4`.

The drawing documents themselves remain unchanged from the known-good case.

Expected finding: `CM-R003`.

This isolates a cross-document disagreement.

## Generating the Benchmark

All built-in cases are available in deterministic order through:

```python
from circuitmind.synthetic.cases import all_synthetic_cases
```

The complete benchmark can be generated with:

```python
from pathlib import Path

from circuitmind.synthetic.generator import generate_all_project_cases

generate_all_project_cases(Path("build/synthetic"))
```

From PowerShell:

```powershell
uv run python -c "from pathlib import Path; from circuitmind.synthetic.generator import generate_all_project_cases; generate_all_project_cases(Path('build/synthetic'))"
```

Individual cases can also be generated using `generate_project_case`.

## Determinism

Synthetic generation avoids randomness in V0.1.

The generator uses:

- fixed page dimensions
- fixed geometry
- deterministic object ordering
- built-in PDF fonts
- stable CSV column ordering
- stable manifest serialization
- deterministic case ordering

Regenerating a case removes the previous case directory first so stale generated artifacts cannot survive into a new run.

Tests verify reproducibility across different output directories, including byte-stable generated artifacts where practical.

## PDF and CSV Format

Synthetic PDFs use vector primitives and selectable text rather than rasterised schematic images.

The drawing vocabulary is intentionally constrained. It exists to exercise extraction and reasoning boundaries without attempting to reproduce a complete CAD or ECAD package.

The V0.1 I/O schedule uses a stable CSV schema:

```text
signal,plc_address,description
```

## Visual Metadata

Synthetic wires may preserve objective source metadata such as stroke RGB colour.

Colour does not have a globally hard-coded engineering meaning.

A future company or project drawing profile may interpret source colour according to the conventions used by a particular drawing set, while the generic extraction layer should preserve the raw visual evidence.

## Future Use

Once the CircuitMind extraction and validation pipeline exists, the generated `project/` directories will be processed without access to their manifests.

The resulting findings can then be compared against each case's oracle:

```text
good_digital_input_project       → []
duplicate_plc_address_project    → [CM-R001]
dangling_connection_project      → [CM-R002]
schedule_mismatch_project        → [CM-R003]
```

This will allow end-to-end regression tests to prove that CircuitMind can recover known engineering truth from independently generated source artifacts.

## Confidentiality

Synthetic fixtures must remain generic and non-confidential.

They must not contain copied employer drawings, customer data, proprietary project content, or customer-specific conventions taken from confidential engineering material.
