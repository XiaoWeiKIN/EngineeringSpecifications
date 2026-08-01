# Specification Index

## Notation Conventions and Compliance

The keywords `MUST`, `MUST NOT`, `REQUIRED`, `SHOULD`, `SHOULD NOT`,
`RECOMMENDED`, `NOT RECOMMENDED`, `MAY`, and `OPTIONAL` are interpreted as
described by
[BCP 14](https://www.rfc-editor.org/info/bcp14),
[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119), and
[RFC 8174](https://www.rfc-editor.org/rfc/rfc8174) only when they appear in
uppercase.

Existing `0.x` specifications also use direct imperative sentences as
normative requirements. New and substantially rewritten text should use BCP 14
terms when requirement strength affects compliance. Rationale, examples, and
implementation suggestions should be identified as non-normative.

Current documents without an explicit status are Development. See the
[Specification Lifecycle](../governance/lifecycle.md) for compatibility
expectations. Development requirements remain normative within a pinned
version; the status permits a later version to change incompatibly.

`core/semantic-naming`, `core/data-boundaries`, and `languages/go` publish
stable Requirement IDs.

## Authoring

Start new normative documents from the
[Formal Specification Template](0000-template.md). The template is optimized
for Harness Engineering: it connects task applicability, stable Requirement
IDs, enforcement classes, verification mechanisms, implementation evidence,
and an Agent handoff.

The template is an authoring resource, not a published specification. A
document becomes published only after it has its own path and stable Catalog
entry. `catalog.json` remains authoritative for version, dependencies, scopes,
detection evidence, and digest.

Selection and task activation are separate. Required means the Specification
is installed and locally available. `applies_to` produces file candidates; the
Catalog description and the document's Applicability section determine whether
the full text enters a task's context.

## Core

- [Semantic naming](core/semantic-naming.md)
- [Data boundaries](core/data-boundaries.md)

## Languages

- [Go implementation](languages/go.md)

The Markdown files are the normative sources. `catalog.json` supplies stable
IDs, versions, dependencies, scopes, detection evidence, and content digests
for machine consumers.

This index lists only published specifications. The
[Specification Model](../docs/specification-model.md) defines how future Core,
language, framework, database, testing, and protocol specifications compose
without turning planned categories into published contracts.

The [Governance Model](../governance/README.md) defines the Proposal, maturity,
versioning, compliance, and quality contracts used to evolve this index.
