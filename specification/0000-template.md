# Specification Title

> **Status:** Development
>
> **Catalog ID:** `category/spec-name`
>
> **Selection:** Required | Detected | Explicit
>
> **Routing:** Selection installs this Specification. File scope and the
> Applicability contract decide whether an agent reads it for a task.
>
> **Catalog metadata:** `catalog.json` is the source of truth for version,
> dependencies, file scopes, detection evidence, activation summary, and
> content digest.

Replace the title and metadata before review. Delete every authoring
instruction that does not belong in the published Specification.

## Purpose

State one reusable engineering outcome. Identify the recurring failure,
inconsistency, safety risk, or review cost this Specification prevents. Keep
project-specific architecture outside this repository.

List explicit non-goals when adjacent behavior could otherwise be mistaken for
part of the contract. The Catalog description must be a compact activation
summary suitable for a generated Agent routing index.

## Applicability

### Load this specification when

- Name observable task intents, such as adding an external-data parser,
  changing a public API, or mapping a value across compatibility surfaces.
- Describe repository evidence an agent can inspect before editing.
- Keep exact file globs and deterministic detection metadata in `catalog.json`.

### Do not apply this specification when

- Identify generated, vendored, migration-only, legacy, or protocol-owned
  contexts.
- State which owning surface or project Specification governs the decision.
- Explain whether an adapter or compatibility mapping still activates part of
  this contract.

`applies_to` creates a conservative file candidate. Applicability decides task
activation. Required selection guarantees local availability; it does not make
the full document part of every task context.

## Agent workflow

When this Specification is activated, the implementing or reviewing agent:

1. identifies the Requirement IDs affected by the task;
2. inspects existing vocabulary, public contracts, and owning external
   surfaces before introducing a new form;
3. applies the smallest change that satisfies the activated requirements;
4. runs each applicable Verification entry;
5. reports immutable or reproducible evidence and any governed exception.

Keep this procedure specific enough to produce a reviewable result. Do not
repeat a generic software-development loop that every task already follows.

## Terminology

Define only terms that carry a specific meaning in this contract. Reuse terms
from required upstream Specifications instead of creating synonyms.

## Requirements

Assign stable IDs to load-bearing requirements. Use a globally recognizable
uppercase prefix followed by a topic and number, such as `DATA-PARSE-001` or
`MYSQL-SCHEMA-001`. Never reuse an ID for a different semantic requirement.

### AREA-TOPIC-001 — Requirement title

[The implementation or agent] **MUST** [state one observable behavior].

**Rationale (non-normative):** Explain why the requirement exists and which
failure it prevents. Do not introduce additional requirements here.

**Enforcement (mechanical | review | hybrid):** Choose one class and identify
at least one plausible enforcement path:

- schema, type system, lint, or static analysis;
- focused unit, integration, structural, or contract test;
- deterministic review procedure when mechanical enforcement is impractical.

**Evidence:** Describe the immutable source revision, test result, generated
report, or reviewed artifact that can demonstrate compliance. Planned or
missing checks are not evidence.

Repeat this subsection only for requirements that need an independent stable
ID. Use `SHOULD` for strong defaults with legitimate exceptions and `MAY` for
optional behavior.

## Approved patterns

Provide small, representative implementations, data shapes, or workflows that
satisfy the requirements. Mark examples as non-normative and avoid turning one
language or framework choice into a cross-ecosystem requirement.

## Rejected patterns

Show recurring implementation shapes that violate a requirement. Link every
rejection to its Requirement ID and explain the observable failure so an agent
does not reproduce the pattern elsewhere.

## Exceptions

State the exact conditions under which an implementation may depart from a
`SHOULD` requirement, where it records the decision, and how reviewers verify
the exception. State `None` when this Specification defines no exceptions.

An exception cannot weaken a `MUST` requirement without a versioned normative
change.

## Verification

Map every load-bearing Requirement ID exactly once to its minimum verification
mechanism. Include only IDs declared by this document. Provide canonical
commands only when they are portable across consuming repositories.

| Requirement | Minimum verification |
| --- | --- |
| `AREA-TOPIC-001` | Name the deterministic check or review record |

## Agent handoff

An agent that applies this Specification reports the following information in
its plan, pull request, review, or final task result:

```text
Activated requirements: AREA-TOPIC-001
Verification: <command, test result, or reviewed artifact>
Exceptions: none | <governed exception and owner>
Compatibility or migration: none | <observable effect and plan>
```

The handoff is an evidence index. It does not replace the underlying test,
source revision, generated report, or reviewed artifact.

## Compatibility and migration

Describe compatibility effects, adoption order, rollback conditions,
deprecation, and migration from earlier behavior. State which Requirement IDs
are added, preserved, superseded, or removed by a normative revision.

Development requirements remain normative within a pinned version even though
a later Development version may change incompatibly.

## References

Link the approved ESP when one exists, required upstream Specifications, and
primary language, framework, database, or protocol documentation. References
provide provenance and do not add undeclared normative requirements.
