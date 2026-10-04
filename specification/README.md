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

Every formal Requirement also declares `Automated enforcement: Advisory`,
`Warning`, or `Blocking`. This level controls machine action and remains
independent from BCP 14 strength, maturity, and the mechanical, review, or
hybrid enforcement class. New Requirements start at Advisory. See the
[Automated Enforcement Lifecycle](../governance/enforcement-lifecycle.md) for
promotion evidence, override, and observation contracts.

`core/semantic-naming`, `core/data-boundaries`, `languages/go`,
`languages/go/performance`, `languages/go/functional-options`, and
`languages/go/factory-delegation` publish stable Requirement IDs.
The two documentation Specs below add eight `DOC-*` IDs in the Unreleased
working Catalog; they are not present in earlier release tags.

## Authoring

Start new normative documents from the
[Formal Specification Template](0000-template.md). The template is optimized
for Harness Engineering: it connects task applicability, stable Requirement
IDs, bounded activation cards, exact context dependencies, enforcement
classes, automated enforcement levels, verification mechanisms,
implementation evidence, and an Agent handoff.

The template is an authoring resource, not a published specification. A
document becomes published only after it has its own path and stable Catalog
entry. `catalog.json` remains authoritative for version, dependencies, scopes,
detection evidence, and digest.

Selection and task activation are separate. Required means the Specification
is installed and locally available. `applies_to` produces file candidates; the
Catalog description and the document's Applicability section determine whether
the Specification applies. Requirement activation summaries then select exact
IDs, code resolves their declared dependency closure, and the consumer compiles
an exact bounded context capsule. Whole-Spec reading is an explicit fallback
for legacy, migration, or repository-wide audit work.

## Core

- [Semantic naming](core/semantic-naming.md)
- [Data boundaries](core/data-boundaries.md)

## Languages

- [Go implementation](languages/go.md)
- [Go performance engineering](languages/go/performance.md)
- [Go functional options](languages/go/functional-options.md)
- [Go capability factory delegation](languages/go/factory-delegation.md)

## Documentation (Unreleased)

- [Technical documentation](documentation/technical-documentation.md)
- [Derived engineering explanations](documentation/derived-explanations.md)

Both are explicit optional Development Specs. The
[documentation-layer guide](../docs/documentation-contracts.md)
([简体中文](../docs/documentation-contracts.zh-CN.md)) explains composition,
producer-path candidacy, verification limits and release/adoption boundaries.

The Markdown files are the normative sources. `catalog.json` supplies stable
IDs, versions, dependencies, scopes, detection evidence, and content digests
for machine consumers.

This index lists cataloged specifications, with unreleased additions marked.
The [Specification Model](../docs/specification-model.md) and documentation-layer
guide define how Core, language, framework, database, testing, protocol and
documentation specifications compose without making every category required.

The [Governance Model](../governance/README.md) defines the Proposal, maturity,
automated enforcement, versioning, compliance, and quality contracts used to
evolve this index.
