# CircuitMind

CircuitMind is an AI-assisted electrical engineering design-review platform aimed at industrial electrical and controls engineering.

The long-term goal is to analyse electrical schematic and drawing sets, construct a machine-readable electrical model, run deterministic engineering validation rules, and present clear, traceable findings to engineers.

## V0.1

CircuitMind V0.1 is intentionally narrow.

The first version will focus on:

- machine-generated vector PDF schematics
- a constrained synthetic drawing format
- extraction of electrical entities and connectivity
- a typed internal electrical domain model
- deterministic design-review rules
- structured findings with source traceability

Initial validation rules will include:

- duplicate PLC addresses
- unresolved or dangling connections
- mismatches between schematic PLC I/O and an external I/O schedule

AI and LLM functionality is not part of the deterministic V0.1 validation path.

## Engineering principles

CircuitMind is being developed around the following principles:

- deterministic engineering logic where possible
- AI used to assist interpretation and explanation, not replace connectivity logic
- traceable findings linked back to source drawing data
- reproducible synthetic test data
- automated testing and static analysis
- incremental development through issues, branches and pull requests
- no confidential employer or customer material

## Development

Requirements:

- Python 3.12+
- `uv`

Install the development environment:

```bash
uv sync