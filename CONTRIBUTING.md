# Contributing

EngineeringSpecifications contains reusable normative guidance. Changes should
be reviewable as specification changes, not hidden inside consumer tooling.

Read the [Specification Model](docs/specification-model.md) before introducing
a new category or specification dependency.

Read the [Specification Principles](governance/specification-principles.md) and
[Lifecycle](governance/lifecycle.md) before adding behavior or changing a
compatibility promise.

## Choose the broadest valid layer

Place a rule in the broadest reusable layer where its meaning remains true:

- `core/` is reserved for rules required by every implementation repository;
- `languages/` contains language contracts and idiomatic realization;
- `frameworks/` contains framework or major-library constraints;
- `databases/` contains shared schema rules and database-engine specifics;
- `testing/` contains cross-language and focused testing contracts;
- `protocols/` contains shared wire, API, messaging, and compatibility rules.

A cross-language rule is not automatically a Core rule. For example, database
schema design is reusable across languages but remains conditional on a project
using a database.

Put shared behavior in one upstream specification. Narrower specifications
declare it through `requires` and contain only additional constraints. Directory
nesting does not define inheritance or override precedence.

## Route changes by impact

### Editorial changes go directly to review

Spelling, formatting, broken links, and wording changes that preserve required
behavior can use a normal pull request. Explain why the change is
non-normative.

### Scoped normative changes identify their contract

A focused change to an existing Development specification can use a normal pull
request when its behavior, affected IDs, compatibility impact, and evidence are
clear. Update the Changelog and the affected Spec version.

### Significant changes start with an ESP

Create an [Engineering Specification Proposal](proposals/README.md) before a
change that introduces a category, crosses languages or implementation
ecosystems, alters Stable behavior, or changes the Catalog/consumer contract.

An approved ESP records direction. A separate integration change creates the
normative contract, versions it, refreshes digests, and passes repository
validation.

## Write normative text intentionally

The keywords `MUST`, `MUST NOT`, `REQUIRED`, `SHOULD`, `SHOULD NOT`,
`RECOMMENDED`, `NOT RECOMMENDED`, `MAY`, and `OPTIONAL` carry their BCP 14
meaning only when written in uppercase.

Use these terms sparingly:

- `MUST` identifies behavior required for correctness, safety,
  interoperability, or the stated contract.
- `SHOULD` identifies a strong default with legitimate documented exceptions.
- `MAY` identifies an optional capability.
- rationale, examples, and implementation suggestions use ordinary
  non-normative language.

New specifications state their maturity immediately after the title. Until the
Catalog carries machine-readable maturity, a missing marker means Development.

## New specifications close the Harness feedback loop

Copy the
[Formal Specification Template](specification/0000-template.md) when creating a
normative document. The template separates six concerns that a coding agent and
reviewer both need:

1. selection says how the Specification becomes locally available;
2. applicability says when it enters task context;
3. a stable Requirement ID identifies the behavioral contract;
4. enforcement classifies mechanical, review, or hybrid protection;
5. evidence says how a consumer demonstrates compliance;
6. the Agent handoff indexes activated IDs, verification, exceptions, and
   migration effects.

Keep proposal reasoning in the related ESP. The integrated specification
retains only the purpose, observable requirements, rationale needed to apply
them correctly, approved and rejected patterns, exceptions, verification, and
migration contract.

Catalog metadata is not duplicated as free-form normative text. The template
shows human-readable status, ID, and selection intent, while `catalog.json`
remains authoritative for version, dependencies, scopes, detection evidence,
activation summary, and digest.

Required selection means every implementation repository installs the
Specification. It does not mean every task reads the full document. Write the
Catalog `description` as a compact `Load when ...` summary. Use `applies_to` as
a conservative file candidate and the Applicability section as the task-intent
contract.

## Change process

1. Explain the engineering problem and affected specification IDs.
2. State the intended repositories, technologies, and file scopes.
3. Link an approved ESP when the change is significant.
4. Provide prototype, test, implementation, or repository evidence appropriate
   to the requirement.
5. For a new specification, copy `specification/0000-template.md` to its final
   category path and replace every authoring placeholder.
6. Edit or add normative Markdown under `specification/`.
7. Keep each rule testable, scoped, and independent of one private repository.
8. Update `catalog.json`:
   - preserve stable IDs;
   - bump the affected specification version for normative changes;
   - refresh the source SHA-256;
   - declare dependencies and deterministic detection evidence.
   - write the description as an Agent-readable activation summary.
9. Update `CHANGELOG.md` for externally observable changes.
10. Run the canonical check:

```bash
python3 -B scripts/check.py
```

Automatic detection is optional. Use it only when filenames or extensions
provide reliable evidence. Framework and database specifications without such
evidence remain explicit project selections until the Catalog contract gains a
reviewed dependency-evidence model.

## Compatibility

- Patch versions clarify wording without changing required behavior.
- Minor versions add backward-compatible guidance or supported categories.
- Major versions change or remove an existing normative contract.
- Moving files without changing normative content does not require a
  specification version bump, but Catalog paths and digests must remain valid.

Consumers lock an immutable Git commit, so merging a change does not update a
project until it runs an explicit EngineeringWorkflow update.

## Project-specific rules

Do not add a rule that only describes one repository's architecture, directory
layout, framework selection, domain vocabulary, or component pattern. Keep
those rules in the project and register them through its
`docs/.engineering/specs.json` `project_specs` entries.

A project rule becomes a candidate for this repository only after it is useful
across repositories and can be versioned without relying on its original
codebase.
