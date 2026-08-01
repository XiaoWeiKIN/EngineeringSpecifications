# Changelog

All notable Catalog and normative specification changes are recorded here.

## Unreleased

### Added

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
