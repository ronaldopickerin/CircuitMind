# CircuitMind Domain Model

CircuitMind uses a typed electrical intermediate representation as the primary
source of truth for engineering analysis.

The model is intentionally independent of PDF parsing and graph libraries.
Input adapters populate the domain model, deterministic validation rules inspect
it, and graph or reporting representations are derived from it.

## Logical entities and drawing occurrences

CircuitMind distinguishes between an electrical object and each graphical place
where that object appears on a drawing.

For example, a relay may be represented by one logical `Device` and several
`DeviceOccurrence` objects:

- relay coil on one page
- normally open contact on another page
- auxiliary contact elsewhere in the drawing set

Likewise, a logical `ConnectionPoint` may have multiple
`ConnectionPointOccurrence` objects.

This prevents repeated drawing representations from being mistaken for duplicate
engineering objects.

## Connectivity

`WireSegment` represents drawn wire geometry.

`ElectricalNet` represents logical electrical connectivity and groups connection
points and wire segments that are electrically common.

A net may contain unresolved or dangling connectivity. These states remain
representable so deterministic validation rules can report them rather than the
domain model rejecting them.

## Structural validation vs engineering validation

`CircuitModel` validates structural integrity, including:

- entity ID uniqueness
- references to existing devices
- references to existing documents and drawing pages
- valid connection-point references
- valid wire-segment references
- membership of a connection point or wire segment in at most one electrical net

Engineering faults are deliberately not rejected during model construction.

For example:

- duplicate PLC addresses
- duplicate engineering tags
- dangling connections
- schematic/schedule inconsistencies

remain valid model states and are evaluated later by dedicated validation rules.

## Source provenance

Drawing-derived objects retain source traceability through `SourceReference`.

References can identify:

- a document
- a PDF page
- a drawing bounding box
- a structured-data row such as an I/O schedule row

This allows findings to identify the evidence that caused a rule to fail.

## Findings

Validation rules produce structured `Finding` objects rather than directly
printing messages.

Each finding contains:

- rule ID
- severity
- title
- explanatory message
- one or more source evidence references

This allows the same deterministic result to be consumed by CLI, JSON, future UI,
reporting, or AI-assisted explanation layers.

## Design boundary

The domain model is the authoritative electrical representation.

PDF parsers, synthetic-data generators, NetworkX graphs, reporting code, and
future LLM features sit outside the model and consume or populate its public
interfaces.