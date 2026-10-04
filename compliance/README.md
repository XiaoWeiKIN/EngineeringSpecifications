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
DOC-STATE-001
DOC-DERIVED-PROV-001
```

Wording and document paths may evolve without changing an ID's meaning. A
semantic change creates a new requirement ID or follows an explicitly
documented compatibility transition.

Every current Catalog Specification publishes stable Requirement IDs. Use the
[Specification index](../specification/README.md) and the selected Catalog
revision to identify the available set, rather than a second hand-maintained
list. No implementation matrix should claim coverage for a requirement that
lacks a stable ID in its selected source.

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

## Enforcement observations measure the evaluator, not conformance alone

Every formal Requirement declares an Automated enforcement level. The level
controls machine action and remains independent from implementation compliance.
An Advisory finding can identify a real violation. A Blocking finding can be
overridden while the underlying implementation remains non-conforming.

A consumer claiming Warning or Blocking operation retains the append-only
observation fields defined by the
[Automated Enforcement Lifecycle](../governance/enforcement-lifecycle.md).
Stable Requirement IDs join findings to the normative contract. Stable finding
IDs join one issue across repeated reviews, remediation, dismissal, override,
and expiry events.

Evidence reports distinguish at least:

- event count, unique finding count, and unique affected-change count;
- confirmed, remediated, false-positive, and escaped findings;
- conforming `SHOULD` exceptions and non-conforming gate overrides;
- time to disposition and time to remediation;
- active, expired, and repeatedly renewed overrides.

Finding volume and blocked-workflow count do not prove engineering impact on
their own. Promotion evidence links these measurements to an executor version,
configuration digest, observation window, repository revision, and durable
evidence reference. Aggregate telemetry excludes source text, secrets, and
personal content unless a separately governed policy authorizes collection.

## Generated views must not drift

When compliance data is introduced:

1. implementation repositories own their evidence;
2. this repository may aggregate versioned evidence records;
3. a deterministic generator produces the human-readable matrix;
4. the canonical check fails when generated output differs from its sources.

Enforcement observations remain implementation-owned evidence. This repository
may later aggregate privacy-reviewed records, but a generated dashboard never
becomes the source of conformance or promotion authority.

This follows the useful separation in OpenTelemetry's
[implementation compliance matrix](https://github.com/open-telemetry/opentelemetry-specification/blob/main/spec-compliance-matrix.md)
while using stable requirement IDs instead of display text as the primary key.
