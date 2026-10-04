# Changelog

All notable Catalog and normative specification changes are recorded here.

## Unreleased

### Changed

- Prepare development Catalog `1.7.1` for an editorial review of existing Spec
  prose and examples; no release tag is created or moved by this change.
- Advance `core/data-boundaries` and `languages/go/functional-options` to
  `0.2.1`. Replace the parser-only no-effects illustration with an executable
  boundary-entry fixture and positive control; name the API and constructor
  explicitly in two functional-option sentences. Conformance duties,
  Requirement IDs, scopes, dependencies, exceptions, enforcement levels, and
  Verification mappings remain unchanged.
- Add local non-normative Specification authoring guidance and route AGENTS,
  CONTRIBUTING, and the formal template to it. Correct the old consumer name
  and include documentation in the repository guide's taxonomy.
- Record a bounded semantic review and add preservation and example regression
  tests. Existing `core/semantic-naming` prose remains unchanged after review.
- Continue the bounded editorial review with `languages/go` at `0.5.1` and
  `documentation/derived-explanations` at `0.1.1`. Clarify optional Go selection
  and the exported-identifier subject; align provenance examples with the
  unchanged source-identity/currentness contract. Keep other reviewed Specs
  unchanged and preserve the prepared `1.7.0` release.
- Extend preservation tests with a separate follow-up delta and exercise the
  unchanged Go implementation snippet with valid and invalid inputs. This is
  example evidence, not a production conformance or accessibility claim.

## [1.7.0] - 2026-10-04

### Added

- Approved ESP-0014 and added the optional `documentation/` Catalog layer for
  reusable documentation-integrity contracts without making Google-informed or
  STE-inspired editorial guidance normative.
- Added Development `documentation/technical-documentation` version `0.1.0`
  with five Advisory Requirements covering engineering state, evidence-backed
  claims, procedure semantics, owning terminology, and current-versus-historical
  freshness.
- Added Development `documentation/derived-explanations` version `0.1.0` with
  three Advisory Requirements covering derived authority, source provenance,
  and equivalent access to engineering information across diagrams,
  interactive views, presentations, simulations, and video.

### Changed

- Advanced the Catalog to `1.7.0`. Both documentation Specifications are
  explicitly selected, the technical-documentation Spec depends on
  `core/semantic-naming`, and the derived-explanations Spec depends on
  `documentation/technical-documentation`. Catalog schema version 1 and all
  previously published Requirement behavior remain unchanged.

## [1.6.0] - 2026-08-10

### Added

- Approved the Requirement-level automated enforcement ESP and added the
  independent `Advisory`, `Warning`, and `Blocking` lifecycle, evidence-gated
  promotion, expiring gate overrides, and append-only finding observations.
- Added `Automated enforcement: Advisory` to all 32 published Requirement
  blocks and the formal Specification template.
- Added canonical validation for missing, duplicated, unknown, and ineligible
  Warning or Blocking metadata. Warning requires a `SHOULD`/`SHOULD NOT` or
  stronger obligation; Blocking requires a `MUST` or `MUST NOT` obligation.
- Added Development `languages/go/performance` version `0.1.0` with five
  Advisory Requirements for explicit performance targets, representative
  diagnosis, bounded hotspot hypotheses, repeated comparative verification,
  and stricter admission of `unsafe`, assembly, and architecture-specific
  implementations.
- Added R-001/RR-002 evidence that separates the reusable Go performance loop
  from fixed phase order, hotspot percentages, and VictoriaMetrics-specific
  product claims.

### Changed

- Advanced the Catalog to `1.6.0`; advanced `core/semantic-naming` to `1.2.0`,
  `core/data-boundaries` and both narrow Go pattern Specifications to `0.2.0`,
  and `languages/go` to `0.5.0`. Existing normative behavior, Requirement IDs,
  routing metadata, enforcement classes, and Verification rows are preserved.
- Separated machine action from BCP 14 strength, document maturity, and
  enforcement class. Existing Requirements begin at Advisory; no Warning or
  Blocking claim exists until a consumer supplies versioned observation
  evidence.
- Kept Go performance guidance explicitly selected and dependent on
  `languages/go`; cross-language `testing/performance` extraction remains
  deferred until a materially different language/runtime supplies evidence
  through an ESP.

## [1.5.0] - 2026-08-05

### Added

- Approved the Requirement-level context activation ESP and added compact
  `Activation` plus exact `Context dependencies` metadata to all 32 published
  Requirement blocks.
- Added canonical validation for Requirement activation length, 8 KiB block
  budgets, exact reference coverage, Catalog-scoped dependency edges, and
  acyclic Requirement context closure.
- Added Development `languages/go/functional-options` version `0.1.1` to
  constrain when functional options fit, keep required inputs explicit, define
  target and extension ownership, make application and validation
  deterministic, preserve exported compatibility, and require composition
  tests.
- Added Development `languages/go/factory-delegation` version `0.1.1` for
  capability-specific named delegates, extensible factory surfaces, immutable
  construction, explicit unsupported behavior, and capability-matrix evidence.

### Changed

- Advanced the Catalog to `1.5.0`; advanced `core/semantic-naming` to `1.1.1`,
  `core/data-boundaries` to `0.1.1`, `languages/go` to `0.4.1`, and both narrow
  Go pattern Specifications to `0.1.1`. These patch revisions add routing
  metadata without changing existing Requirement behavior.
- Defined two-stage Spec/Requirement routing, exact digest-verified context
  capsules, explicit whole-Spec fallback, bounded card/capsule budgets, and
  context-epoch rehydration for RepoFoundry consumers.
- Kept file-extension detection owned by `languages/go`; a Go file alone does
  not recommend the narrower functional-options or factory-delegation pattern.

## [1.3.0] - 2026-08-04

### Added

- Approved ESP-0010 to adapt task-time activation to Codex with one generated
  Router Skill, a mandatory AGENTS route, trusted Hook gating, and an explicit
  activation evidence handoff while keeping normative Specs Agent-neutral.
- Approved ESP-0009 to make deterministic detection advisory and require an
  explicit project choice before installing optional Specifications.
- Approved ESP-0008 and documented immutable `vMAJOR.MINOR.PATCH` Catalog
  releases, release validation, fixed-version consumption, and explicit
  upgrades.
- Added `scripts/check_release.py` to verify Catalog SemVer, Changelog release
  identity, and published tag content.

### Changed

- Advanced Catalog to `1.3.0` and `core/semantic-naming` to `1.1.0`.
  `SEM-VERB-001` now requires idempotent, equivalence-preserving `Normalize`
  operations; gives `Extract` a narrow selection contract; and prohibits both
  verbs from hiding parsing, validation, defaulting, enrichment, computation,
  I/O, mutation, or material side effects.
- Clarified the selection model: required Specifications remain automatic,
  detected optional Specifications are recommendations, explicit project IDs
  determine optional installation, and dependencies remain automatic.

## [1.2.0] - 2026-08-02

### Added

- Added `GO-MODULE-001` to require reproducible, no-diff module and committed
  vendor state across the declared module inventory.
- Added `GO-GENERATE-001` to require authoritative inputs, reproducible
  generation, and clean-diff evidence for committed generated artifacts.
- Approved ESP-0007 to separate Specification selection, file candidacy, and
  task activation without changing Catalog schema version 1.
- Added Development `core/data-boundaries` version `0.1.0` for untrusted
  shapes, domain parsing, effect gating, boundary errors, and protocol-owned
  normalization.
- Added Agent workflow and handoff sections to the formal template and current
  published Specifications.
- Added canonical checks for document metadata, Requirement block structure,
  enforcement classes, and exact Verification coverage.

### Removed

- Removed the Development `languages/python` and `languages/typescript`
  specifications from the Catalog and deleted their normative sources.
  Consumers selecting either ID must remove it from their manifest and
  regenerate the lock before updating to Catalog `1.0.0`.

### Changed

- Advanced Catalog to `1.2.0` and `languages/go` to `0.4.0`. The Go
  Specification now routes module metadata and committed vendor state, adds
  single-method interface and canonical method naming to `GO-NAME-002`,
  requires scoped race evidence in `GO-LIFECYCLE-001`, and requires a
  risk-based toolchain/platform/architecture/build-tag matrix in
  `GO-TEST-001`.
- Advanced Catalog to `1.1.0` with activation-oriented descriptions and the
  new required Data Boundaries Specification; the JSON shape remains schema
  version 1.
- Advanced `core/semantic-naming` to `1.0.0`, moved boundary parsing into the
  dedicated Core contract, and published the Requirement-ID migration from
  `SEM-BOUNDARY-001`.
- Advanced `languages/go` to `0.3.0` without changing existing `GO-*`
  Requirement meanings; Go now depends explicitly on both Core contracts.
- Defined Required as installation and local availability. File scopes produce
  candidates; Catalog descriptions and Applicability decide task activation.
- Clarified the multi-layer specification model for Core, languages,
  frameworks, databases, testing, protocols, and project-owned rules.
- Documented the separation between specification selection, dependency
  resolution, locking, and task-time reading.
- Added BCP 14 notation conventions, specification principles, maturity
  lifecycle, and impact-based contribution lanes.
- Added the non-normative Engineering Specification Proposal process and
  template.
- Added a Harness-oriented formal Specification template that connects
  applicability, stable Requirement IDs, enforcement, and evidence.
- Formalized Core semantic naming and Go implementation guidance as version
  `0.2.0` contracts with stable Requirement IDs, applicability, enforcement,
  evidence, patterns, exceptions, and migration guidance.
- Added canonical validation for Requirement ID format and Catalog-wide
  uniqueness.
- Defined the evidence-first compliance model without claiming implementation
  conformance.
- Released Catalog `1.0.0` to identify the breaking removal while leaving the
  independently versioned Core and Go specifications at `0.2.0` and
  Development maturity.

## [0.1.0] - 2026-07-31

### Added

- The versioned Catalog schema and SHA-256 content contract.
- Required semantic naming guidance.
- Go, Python, and TypeScript implementation guidance.
- Deterministic language detection, dependency, and file-scope metadata.
- Bilingual repository documentation and a canonical validation command.
