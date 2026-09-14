# 001 — Separate Logical and Graphical Electrical Entities

## Status

Accepted.

## Context

Electrical drawings contain both engineering concepts and their graphical representations. A device, terminal, connection point, or electrical net may appear multiple times across pages and documents, while each occurrence has its own page position and source provenance.

Treating a drawn occurrence as the electrical object itself makes cross-references, repeated representations, multi-page projects, and source provenance difficult to model correctly.

## Decision

CircuitMind separates logical electrical entities from graphical occurrences.

Examples include:

- `Device` versus `DeviceOccurrence`;
- logical `ConnectionPoint` versus graphical occurrences;
- logical `ElectricalNet` versus drawn `WireSegment` geometry;
- project-level engineering identity versus page-local representation.

Graphical occurrences retain document/page/location provenance. Logical entities represent the canonical engineering concept inferred from one or more source occurrences.

## Consequences

Benefits:

- repeated representations can resolve to one logical entity;
- project-wide consistency checks are possible across pages and documents;
- findings can reference precise source locations without coupling identity to geometry;
- future entity-resolution logic has a clear target model.

Trade-offs:

- the model is more explicit than a simple page-object graph;
- entity resolution is required before some engineering checks can operate reliably.

## Alternatives Considered

A single object type containing both engineering identity and page geometry was rejected because it would couple logical identity to one graphical occurrence and would not scale cleanly to real multi-document drawing sets.
