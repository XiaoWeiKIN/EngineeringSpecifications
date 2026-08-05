# Compliance Model

Compliance connects normative requirements to implementation evidence. This
directory currently defines the contract only; it does not claim conformance
for any language, framework, database, or project.

## Stable requirement IDs are the join key

A specification intended for compliance reporting assigns stable IDs to its
load-bearing requirements, for example:

```text
SEM-NAME-001
DATA-PARSE-001
GO-BOUNDARY-001
MYSQL-SCHEMA-001
GIN-HANDLER-001
TEST-CONTRACT-001
```

Wording and document paths may evolve without changing an ID's meaning. A
semantic change creates a new requirement ID or follows an explicitly
documented compatibility transition.

`core/semantic-naming`, `core/data-boundaries`, `languages/go`,
`languages/go/functional-options`, and `languages/go/factory-delegation`
publish Requirement IDs. No implementation matrix should claim coverage for a
requirement that lacks a published stable ID.

New documents use the
[Formal Specification Template](../specification/0000-template.md) to connect
each load-bearing Requirement ID to bounded activation metadata, exact context
dependencies, enforcement, and expected evidence. Routing metadata identifies
what enters a task context; it does not weaken or replace normative wording.

## Evidence carries more weight than a status symbol

Each implementation record should identify:

- specification ID and version;
- requirement ID;
- implementation repository and immutable revision;
- test, source, generated report, or reviewed documentation evidence;
- status such as implemented, partial, not implemented, not applicable, or
  unknown;
- last verified date and responsible owner.

A generated summary can use compact symbols, but the underlying evidence
record remains the source of truth.

An Agent handoff is a compact evidence index for one task. It identifies the
activated Requirement IDs, verification results, exceptions, and compatibility
effects. It does not become conformance evidence until its referenced tests,
revision, report, or reviewed artifact is durable and reproducible.

## Generated views must not drift

When compliance data is introduced:

1. implementation repositories own their evidence;
2. this repository may aggregate versioned evidence records;
3. a deterministic generator produces the human-readable matrix;
4. the canonical check fails when generated output differs from its sources.

This follows the useful separation in OpenTelemetry's
[implementation compliance matrix](https://github.com/open-telemetry/opentelemetry-specification/blob/main/spec-compliance-matrix.md)
while using stable requirement IDs instead of display text as the primary key.
