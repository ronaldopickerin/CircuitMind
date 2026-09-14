# CircuitMind Roadmap

This document tracks high-level direction rather than detailed task management. Concrete implementation work should be represented by GitHub Issues and pull requests.

## Current Foundation

CircuitMind is being built as a deterministic electrical engineering design-review platform that analyses complete drawing sets and related schedules rather than isolated PDFs.

Completed foundation work includes:

- typed electrical domain model
- separation of logical entities from graphical occurrences
- source provenance
- document and drawing-page modelling
- PLC address/channel modelling
- electrical nets and wire segments
- structured findings
- aggregate `CircuitModel` validation

## Current Milestone

### Synthetic electrical project test bench

Build deterministic, non-confidential project fixtures that can later be passed through the real CircuitMind extraction and validation pipeline.

Target flow:

```text
Synthetic project specification
        ↓
PDF drawings + CSV schedules
        ↓
future extraction
        ↓
entity resolution + connectivity
        ↓
CircuitModel
        ↓
deterministic engineering rules
        ↓
Findings
        ↓
compare against fixture manifest
```

Initial controlled cases include:

- valid digital-input project
- duplicate PLC address (`CM-R001`)
- dangling/unresolved connection (`CM-R002`)
- schematic versus I/O schedule mismatch (`CM-R003`)

## Near-Term Direction

After the synthetic test bench is stable:

- extract structured information from vector PDFs and schedules
- preserve source provenance and uncertainty
- resolve entities across documents and pages
- construct canonical project-level connectivity
- implement deterministic validation rules
- expose structured findings through CLI/JSON interfaces

## Longer-Term Direction

Potential later capabilities include:

- configurable company and project drawing-convention profiles
- support for varying CAD/drawing standards
- reusable extraction adapters
- engineer-facing review UI
- report generation and assisted explanation of findings
- selective ML/AI assistance for ambiguous source interpretation

AI should assist uncertain interpretation and explanation, while deterministic engineering checks remain authoritative wherever possible.
