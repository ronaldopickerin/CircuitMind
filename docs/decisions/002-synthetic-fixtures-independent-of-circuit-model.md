# 002 — Keep Synthetic Fixtures Independent of CircuitModel

## Status

Accepted.

## Context

CircuitMind needs deterministic, non-confidential electrical project fixtures so future extraction and validation can be tested against known ground truth.

If synthetic drawings were generated directly from `CircuitModel`, the test input and the system under test would share the same interpretation. That would make extraction tests circular and could hide modelling errors.

The expected validation result is also test-harness information, not part of the electrical project that CircuitMind should ingest.

## Decision

Synthetic source specifications remain independent of `CircuitModel` and future extraction code.

The synthetic layer describes only external source artifacts such as:

- PDF documents and pages;
- drawn symbols;
- wire geometry;
- visible text;
- CSV schedule rows.

It must not embed interpreted electrical truth such as `same_device`, resolved nets, canonical devices, or connectivity relationships that future CircuitMind stages are expected to infer.

Expected findings are stored separately in `SyntheticProjectCase` and emitted to a case-level `manifest.json` outside the generated `project/` directory.

The generated layout therefore separates source data from the oracle:

```text
case/
├── project/
│   ├── drawings/
│   └── schedules / project files
└── manifest.json
```

Only `project/` represents the future CircuitMind input.

## Consequences

Benefits:

- extraction tests are non-circular;
- source artifacts resemble ordinary engineering inputs;
- faulty engineering states can be represented without structural rejection;
- the oracle cannot accidentally leak expected answers into the project input;
- generated fixtures remain useful if the internal domain model evolves.

Trade-offs:

- some concepts are represented twice at different abstraction levels;
- fixture construction requires explicit source-level geometry and text rather than reusing canonical model objects.

## Alternatives Considered

Generating PDFs from `CircuitModel` was rejected because it would test whether CircuitMind can recover assumptions that CircuitMind itself supplied.

Embedding expected rule IDs inside the generated project directory was rejected because the validator must not be able to observe its expected answer.
