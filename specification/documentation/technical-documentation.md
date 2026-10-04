# Technical Documentation Integrity

> **Status:** Development
>
> **Catalog ID:** `documentation/technical-documentation`
>
> **Selection:** Explicit
>
> **Routing:** Selection installs this Specification. Load it only when the
> task writes or reviews engineering documentation whose state, evidence,
> procedures, terminology, or freshness can affect an engineering decision.
>
> **Catalog metadata:** `catalog.json` is the source of truth for version,
> dependencies, file scopes, detection evidence, activation summary, and
> content digest.

## Purpose

Engineering documentation can change the meaning of a system even when it does
not change executable code. A polished sentence can turn a proposal into an
implemented fact, turn an expectation into a verified result, or make a
mutating command look like a harmless inspection.

This Specification preserves engineering meaning across human-readable
technical documentation. It governs lifecycle and epistemic state, evidence
binding, procedure semantics, terminology ownership, and freshness boundaries.
It does not prescribe prose style, sentence length, tone, document templates,
heading capitalization, or one preferred authoring method.

## Applicability

### Load this specification when

- writing or revising architecture, internals, design, runbook, operations,
  migration, verification, benchmark, research, or decision documentation;
- documenting commands or ordered procedures whose execution can mutate state,
  verify a condition, or change approval or release authority;
- making or reviewing measured, verified, reliability, security, performance,
  compatibility, or completion claims;
- editing terminology that appears across code, schemas, protocols, metrics,
  generated views, or other documentation;
- updating current guidance while historical decisions or evidence remain in
  the repository.

### Do not apply this specification when

- changing only spelling, punctuation, or formatting with no effect on
  technical meaning;
- editing generated or vendored documentation whose source owner defines the
  content and is not being changed;
- copying an exact normative excerpt, raw log, code block, or immutable
  historical record without rewriting it;
- applying a project-specific document layout or publication workflow that is
  owned by the consuming repository.

A project may still activate one Requirement when a narrow editorial change
touches a load-bearing claim, stable term, or procedure.

## Agent workflow

When this Specification is activated, the implementing or reviewing agent:

1. identifies the owning artifact, intended reader task, and whether the text
   describes current, proposed, accepted, verified, or historical information;
2. locates the evidence or source contract for every load-bearing claim;
3. preserves BCP 14 strength, lifecycle state, exact identifiers, and
   externally owned spellings before improving prose;
4. separates read-only or preview actions from mutation, verification, and
   authority-changing steps when a procedure contains those effects;
5. checks whether current guidance is still supported by the cited source
   revision without rewriting immutable history;
6. runs each applicable Verification entry and reports unresolved evidence or
   freshness gaps.

## Terminology

- **Engineering state** is the status that determines how a statement may be
  used, including current, proposed, accepted, rejected, planned, implemented,
  verified, unverified, and historical.
- A **strong claim** is a statement whose truth can materially change an
  engineering decision, such as a measured result or an assertion of
  reliability, security, compatibility, completion, or verification.
- An **evidence locator** identifies the source revision, test, benchmark,
  report, approval record, or other reviewable artifact supporting a claim.
- **Current guidance** describes behavior or procedure intended for present
  use. A **historical record** preserves what was decided, observed, or
  performed at an earlier revision.
- An **owning surface** has the meaning defined by
  `core/semantic-naming`; documentation does not gain ownership of a spelling
  merely by repeating it.

## Requirements

### DOC-STATE-001 — Preserve engineering state and requirement strength

**Activation:** Load when editing text that describes current, proposed, accepted, planned, implemented, verified, unverified, or historical behavior.

**Context dependencies:** None

**Automated enforcement:** Advisory

An engineering document **MUST** preserve the source distinction between
current, proposed, accepted, rejected, planned, implemented, verified,
unverified, and historical information when that distinction changes how a
reader may act on the statement.

An editorial revision **MUST NOT** turn an expectation into a measured result,
a proposal into current behavior, an implementation into verified behavior, or
a historical decision into evidence of current implementation solely through
wording or tense.

When the source uses BCP 14 requirement terms, stable lifecycle labels, or
approval states, a derived or edited document **MUST** preserve their strength
and status unless the owning workflow authorizes a normative or lifecycle
change.

**Rationale (non-normative):** Readers and coding agents often treat polished
technical prose as fact. Preserving state prevents editorial changes from
silently granting authority or verification that the source never established.

**Enforcement (review):** Compare changed claims with their owning source,
status metadata, and lifecycle records. A text classifier may find candidates
but cannot prove semantic equivalence.

**Evidence:** A review that links each changed load-bearing statement to its
owning artifact or explicitly records that the source state is unchanged.

### DOC-EVIDENCE-001 — Strong engineering claims identify their evidence

**Activation:** Load when stating or revising a measured, verified, reliability, security, performance, compatibility, completion, or conformance claim.

**Context dependencies:** `DOC-STATE-001`

**Automated enforcement:** Advisory

A strong claim **MUST** identify an evidence locator and the source revision or
other version boundary to which the evidence applies when those facts are
available.

When required evidence is missing, stale, or not accessible, the document
**MUST** state that gap and **MUST NOT** invent a test result, benchmark,
approval, source revision, or verification outcome.

A summary **MUST NOT** strengthen the underlying evidence. Passing a structural
check, digest check, or style review does not by itself prove semantic
correctness, performance, reliability, security, accessibility, or release
readiness.

**Rationale (non-normative):** Strong claims influence design and operational
decisions. Evidence and version boundaries let a reviewer determine what was
actually demonstrated and where uncertainty remains.

**Enforcement (hybrid):** Structural checks may require evidence fields or
references. Human review verifies that the cited artifact supports the claim
and that its revision remains applicable.

**Evidence:** A claim-to-evidence review containing the source revision and the
test, report, benchmark, approval record, or explicit unresolved gap.

### DOC-PROC-001 — Procedures expose material execution semantics

**Activation:** Load when documenting commands or ordered steps that inspect, preview, mutate, verify, publish, approve, release, migrate, or recover engineering state.

**Context dependencies:** `DOC-STATE-001`, `DOC-EVIDENCE-001`

**Automated enforcement:** Advisory

A procedure **MUST** state the prerequisites, action, and observable success or
stop condition needed for a reader to execute the procedure safely.

When materially different operations exist, the procedure **MUST** distinguish
read-only inspection or preview from mutation, verification, publication,
approval, release, or another authority-changing action.

A command presented as executable project guidance **MUST** be supported by the
project or owning tool contract. An unverified command or placeholder **MUST**
remain explicitly unverified or a placeholder and **MUST NOT** be presented as
a confirmed repository command.

**Rationale (non-normative):** Command sequences are executable interfaces.
Readers need to know which step changes state, which step only checks it, and
what evidence establishes success.

**Enforcement (review):** Execute or inspect the owning command contract when
authorized, then review ordering, failure branches, and effect labels. Static
checks may find unlabeled placeholders but cannot infer every shell side effect.

**Evidence:** A reviewed procedure linked to command help, tool documentation,
test execution, or other project evidence that establishes the described
effects and stop conditions.

### DOC-TERM-001 — Documentation reuses owning technical terminology

**Activation:** Load when introducing, renaming, or mapping a technical term across documentation and another engineering surface.

**Context dependencies:** `SEM-NAME-001`, `SEM-SURFACE-001`

**Automated enforcement:** Advisory

Documentation **MUST** use the owning surface's stable term when it refers to
the same concept, and **MUST** declare a mapping when a different
reader-facing term represents that concept.

An editorial change **MUST NOT** rename a published API, schema field,
protocol value, metric, state, or other stable external term solely for prose
consistency.

A document **SHOULD** use one stable term for one concept within its scope
unless a documented semantic distinction requires different terms.

**Rationale (non-normative):** Documentation participates in the same semantic
system as code, schemas, protocols, and metrics. Unowned synonyms increase
ambiguity and can become accidental compatibility promises.

**Enforcement (hybrid):** Search terminology across owning surfaces and review
mappings against `core/semantic-naming`. Automated searches identify candidates
but do not decide whether two words represent the same concept.

**Evidence:** Reviewed terminology mappings or links to the owning API, schema,
protocol, metric, or project vocabulary.

### DOC-FRESH-001 — Current guidance stays distinct from historical records

**Activation:** Load when current documentation depends on implementation facts, old decisions, generated views, or evidence that can become stale.

**Context dependencies:** `DOC-STATE-001`, `DOC-EVIDENCE-001`

**Automated enforcement:** Advisory

Current guidance **MUST** identify an observable source owner or version
boundary when drift could make the documented behavior unsafe or misleading.

A historical ADR, plan, checkpoint, benchmark result, research snapshot, or
other immutable record **MUST** remain identifiable as historical and **MUST NOT** be treated as proof that the current implementation still has the same
behavior without current supporting evidence.

When current guidance is stale, the maintainer **MUST** update or supersede the
current guidance through its owning workflow. The maintainer **MUST NOT**
rewrite immutable historical evidence solely to make the current documentation
appear consistent.

**Rationale (non-normative):** Historical records can remain correct accounts
of the past after implementation changes. Current operational guidance needs a
different freshness contract.

**Enforcement (review):** Compare current guidance with its source owner and
revision. Repository checks may detect stale generated references or digests;
human review determines whether behavior has materially drifted.

**Evidence:** A current source revision or owner reference, plus a review record
for any historical artifact cited as context rather than current proof.

## Approved patterns

The following examples are non-normative.

A proposal keeps its state:

```text
Proposed behavior: route read traffic through the cache.
Current behavior: direct database reads.
Verification: not yet performed.
```

A procedure exposes effects:

```text
1. Run the plan command. This step is read-only.
2. Review the proposed writes.
3. Run the apply command to mutate repository state.
4. Run validation and record the tested revision.
```

A current document can cite history without treating it as current proof:

```text
ADR-004 records why the project selected the cache in 2025.
Current cache behavior is verified against revision abc123 and test T-17.
```

## Rejected patterns

- Rewriting "proposed" as present tense and implying implementation violates
  `DOC-STATE-001`.
- Writing "latency improved significantly" without a benchmark and applicable
  revision violates `DOC-EVIDENCE-001`.
- Listing mutating and read-only commands without explaining their effects
  violates `DOC-PROC-001` when the distinction affects safe execution.
- Renaming a protocol field in prose to match local casing violates
  `DOC-TERM-001` when the owning protocol spelling remains unchanged.
- Citing an accepted historical ADR as the only proof of current runtime
  behavior violates `DOC-FRESH-001`.

## Exceptions

Exact quoted source text, raw logs, code, generated external documentation, and
immutable historical artifacts may preserve wording that does not follow local
editorial guidance. Their owning source remains authoritative.

Project-specific headings, templates, directory layouts, publication gates,
domain vocabulary, and accessibility targets remain project-owned unless a
separate central Specification explicitly governs them.

## Verification

| Requirement | Minimum verification |
| --- | --- |
| `DOC-STATE-001` | Compare edited claims with source lifecycle and requirement state |
| `DOC-EVIDENCE-001` | Review evidence locator and applicable source revision or explicit gap |
| `DOC-PROC-001` | Review prerequisites, effect boundaries, stop conditions, and command evidence |
| `DOC-TERM-001` | Review owning-surface terminology and declared mappings |
| `DOC-FRESH-001` | Compare current guidance with current source owner and historical references |

## Agent handoff

An agent applying this Specification reports:

```text
Activated requirements: <DOC-* IDs>
Document state: <current / proposed / accepted / historical / mixed>
Evidence and revision: <locators and applicable versions, or unresolved gaps>
Procedure effects: none | <preview / mutation / verification / authority effects>
Terminology owners: <owning surfaces and mappings>
Freshness: <current source revision or stale/unknown condition>
Exceptions: none | <project-owned or source-owned exception>
```

## Compatibility and migration

Version `0.1.0` introduces the first Development contract for reusable
technical-documentation integrity. It does not require existing repositories
to adopt the Specification and does not rewrite existing documents.

Consumers adopting this version should review only documentation changed by the
task or otherwise selected for maintenance. Existing historical artifacts keep
their owning lifecycle and are not rewritten merely to satisfy this
Specification.

## References

- [ESP-0014: Reusable documentation integrity contracts](../../proposals/0014_documentation-integrity-contracts.md)
- [Semantic Naming](../core/semantic-naming.md)
- [BCP 14](https://www.rfc-editor.org/info/bcp14)
- [Google Developer Documentation Style Guide](https://developers.google.com/style)
- [Google Technical Writing](https://developers.google.com/tech-writing)
- [ASD-STE100](https://asd-ste100.org/)
