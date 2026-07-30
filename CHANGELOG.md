# Changelog

All notable Catalog and normative specification changes are recorded here.

## Unreleased

### Removed

- Removed the Development `languages/python` and `languages/typescript`
  specifications from the Catalog and deleted their normative sources.
  Consumers selecting either ID must remove it from their manifest and
  regenerate the lock before updating to Catalog `1.0.0`.

### Changed

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
