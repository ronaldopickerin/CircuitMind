# Project Drawing Convention Profiles

## Status

Future concept — not part of the current implementation milestone.

## Problem

Electrical drawing conventions vary between companies, customers, projects, CAD systems, and plotting standards.

CircuitMind should not globally hard-code assumptions such as:

- blue wires always mean internal panel wiring;
- orange wires always mean external wiring associated with the panel;
- white wires always represent interconnection cables;
- one device-tag, terminal, cable/core, or PLC-address syntax applies everywhere.

A convention that is correct for one organisation or project may be wrong for another.

## Proposed Direction

CircuitMind projects should eventually support configurable drawing-convention profiles.

A profile could define or assist interpretation of:

- wire colour meanings;
- device-tag conventions;
- terminal naming conventions;
- cable and core numbering conventions;
- PLC address formats;
- drawing/document classifications;
- cross-reference conventions;
- safety-circuit conventions;
- project-specific exceptions.

## Possible Hierarchy

```text
Company profile
      ↓
Customer / standard profile
      ↓
Project profile
      ↓
Project-specific overrides
```

This would allow a reusable company standard to provide defaults while still permitting one customer or project to override an unusual convention.

## Extraction Principle

The extraction layer should preserve objective source information before interpreting it.

For example:

```text
PDF stroke colour = blue
```

A selected project profile may then interpret that evidence as:

```text
blue → internal panel wiring
```

The generic extractor should not directly encode:

```text
blue = internal panel wiring
```

This distinction allows the same extraction pipeline to support different organisations and drawing styles.

## Future GUI Concept

When creating a new CircuitMind project, an engineer could eventually:

1. upload the project drawing set and schedules;
2. select an existing company or drawing profile;
3. create or edit project-specific conventions;
4. override individual conventions where necessary;
5. save useful profiles for reuse on future projects.

## Evidence and Robustness

Colour and styling should be treated as supporting evidence rather than mandatory truth.

Real drawings may be:

- plotted in monochrome;
- scanned;
- exported using a different plot style;
- produced by another CAD system;
- authored under a different company standard.

CircuitMind should therefore preserve colour and other visual properties when available, but core connectivity and validation should not depend exclusively on them.

## Architectural Fit

The intended long-term flow is:

```text
project files
      ↓
generic extraction
      ↓
objective source facts
      ↓
company / drawing / project profile
      ↓
canonical CircuitModel
      ↓
deterministic engineering validation
```

This keeps project-specific interpretation separate from the canonical electrical model and from deterministic validation rules.
