# Specification Title

> **Status:** Development
>
> **Catalog ID:** `category/spec-name`
>
> **Selection:** Required | Detected | Explicit
>
> **Catalog metadata:** `catalog.json` is the source of truth for version,
> dependencies, file scopes, detection evidence, and content digest.

Replace the title and metadata before review. Delete all authoring instructions
that do not belong in the published specification.

## Purpose

State the reusable engineering outcome in one paragraph. Identify the recurring
failure, inconsistency, safety risk, or review cost this specification
prevents. Keep project-specific architecture outside this repository.

List explicit non-goals when adjacent behavior could otherwise be mistaken for
part of this contract.

## Applicability

### Load this specification when

- Name the tasks, technologies, or repository evidence that make this
  specification relevant.
- Describe how a coding agent can recognize those conditions before editing.
- Keep exact file globs and deterministic detection metadata in `catalog.json`.

### Do not apply this specification when

- Identify generated, vendored, migration-only, legacy, or other excluded
  contexts.
- State when a project-owned specification has authority over a local decision.

## Terminology

Define only terms that carry a specific meaning in this contract. Reuse terms
from required upstream specifications instead of creating synonyms.

## Requirements

Assign stable IDs to load-bearing requirements. Use a globally recognizable
uppercase prefix followed by a topic and number, such as `GO-BOUNDARY-001` or
`MYSQL-SCHEMA-001`. Never reuse an ID for a different semantic requirement.

### AREA-TOPIC-001 — Requirement title

[The implementation or agent] **MUST** [state one observable behavior].

**Rationale (non-normative):** Explain why the requirement exists and which
failure it prevents. Do not introduce additional requirements here.

**Enforcement:** Identify at least one plausible enforcement path:

- schema, type system, lint, or static analysis;
- focused unit, integration, structural, or contract test;
- deterministic review procedure when mechanical enforcement is impractical.

**Evidence:** Describe the immutable source revision, test result, generated
report, or reviewed artifact that can demonstrate compliance.

Repeat this subsection only for requirements that need an independent stable
ID. Use `SHOULD` for strong defaults with legitimate exceptions and `MAY` for
optional behavior.

## Approved patterns

Provide small, representative implementations, data shapes, or workflows that
satisfy the requirements. Mark examples as non-normative and avoid turning one
language or framework choice into a cross-ecosystem requirement.

## Rejected patterns

Show the recurring implementation shapes that violate a requirement. Link each
rejection to its Requirement ID and explain the observable failure so an agent
does not copy the pattern elsewhere.

## Exceptions

State the exact conditions under which an implementation may depart from a
`SHOULD` requirement, where it records the decision, and how reviewers verify
the exception. State `None` when this specification defines no exceptions.

An exception cannot weaken a `MUST` requirement without a versioned normative
change.

## Verification

Map every load-bearing Requirement ID to its expected verification mechanism.
Provide canonical commands only when they are portable across consuming
repositories. Do not claim conformance from planned or missing checks.

## Compatibility and migration

Describe compatibility effects, adoption order, rollback conditions,
deprecation, and migration from earlier behavior. State which requirement IDs
are added, preserved, superseded, or removed by a normative revision.

## References

Link the approved ESP when one exists, required upstream specifications, and
primary language, framework, database, or protocol documentation. References
provide provenance and do not add undeclared normative requirements.
