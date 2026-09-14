# 003 — Treat the Electrical Project as the Analysis Boundary

## Status

Accepted.

## Context

Real controls projects distribute engineering information across multiple PDFs, pages, and schedules. A terminal may appear on one drawing, the connected PLC channel on another, and a matching I/O row in a CSV or spreadsheet.

Analysing each PDF independently would miss many of the consistency checks CircuitMind is intended to perform.

## Decision

CircuitMind treats the complete electrical project or drawing set as the primary analysis boundary.

Individual documents are inputs within a project, not isolated analysis units.

The long-term pipeline is therefore project-oriented:

```text
project files
    ↓
document classification
    ↓
source extraction
    ↓
cross-document entity resolution and connectivity
    ↓
canonical CircuitModel
    ↓
deterministic engineering validation
    ↓
findings with source provenance
```

The architecture must support relationships that cross:

- PDF documents;
- pages within a PDF;
- drawing types;
- I/O schedules;
- terminal schedules;
- cable/core schedules;
- other structured project artifacts.

## Consequences

Benefits:

- enables project-wide consistency checks rather than document-local linting;
- supports comparisons between drawings and schedules;
- provides a natural place for cross-document entity resolution;
- matches how controls engineers review complete design packages.

Trade-offs:

- ingestion and entity resolution are more complex than single-document parsing;
- document type and authority may need to be modelled explicitly;
- conflicting source information must be represented rather than silently collapsed.

## Alternatives Considered

A PDF-by-PDF analysis model was rejected because it would not support the core use case of checking whether a complete drawing package agrees with itself.
