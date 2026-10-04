# Technical Documentation

> **Status:** Development
>
> **Catalog ID:** `documentation/technical-documentation`
>
> **Selection:** Explicit
>
> **Routing:** Selection installs this Specification. File candidates and task
> intent determine which requirements apply.
>
> **Catalog metadata:** `catalog.json` owns version, dependencies, scopes,
> activation summary, and content digest.

## Purpose

Preserve engineering meaning when documentation is created, edited, translated,
or reviewed. Prevent unsupported claims, hidden command effects, terminology
changes, and confusion between decisions, implementation, and verification.

Sentence length, voice, capitalization, document layout, and renderer choices
remain editorial or project concerns. This contract neither incorporates an
external style guide nor claims ASD-STE100 or accessibility-standard compliance.

## Applicability

### Load this specification when

- Writing or reviewing engineering behavior, architecture, interfaces, or claims.
- Documenting commands that readers might execute.
- Revising an explanation after its implementation or evidence changes.
- Translating technical statements across languages or presentation surfaces.

### Do not apply this specification when

- Making a purely decorative change with no engineering information affected.
- Reviewing unrelated application data just because a path matches a scope.
- Reformatting vendored text, raw logs, or exact quotations owned elsewhere.

Do not edit a historical or sealed artifact merely to adopt this Specification.
A newly authored explanation of that artifact still falls within scope. An
external spelling or normative excerpt retains the meaning of its owning source.
File scopes select candidates, not obligations. Only task-applicable requirements
enter the context; adoption does not require a whole-repository rewrite.

## Agent workflow

Identify the statement, command, or explanation being changed and its owning
source. Select only the affected requirements. Compare against the available
implementation and evidence, preserve unresolved gaps, and report the checks
actually performed. Do not execute a destructive command merely to test its
wording; verification must stay inside the authorized environment and scope.

## Terminology

An **owning source** controls a fact, requirement, decision, or verification
result. A **source identity** is a resolvable version/revision, immutable artifact,
or retained snapshot with a digest. **Current guidance** describes a stated
supported version; **history** records an earlier state without claiming currency.

BCP 14 uppercase keywords express the obligations. Their automated
enforcement level is independent of that strength. A valid digest establishes
byte identity, not authenticity, truth, or approval.

## Requirements

### DOC-STATE-001 — Preserve state and requirement strength

**Activation:** Load when writing, revising, or translating statements about engineering behavior, decisions, requirements, or verification status.

**Context dependencies:** None

**Automated enforcement:** Advisory

The author **MUST** preserve the owning source's distinctions between observed,
proposed, decided, implemented, verified, and historical information. These are
independent attributes, not a new lifecycle or a mandatory sequence of states.
Editing **MUST NOT** change a condition, negation, uncertainty, unit, quantifier,
or normative requirement strength. Missing implementation or approval evidence
**MUST NOT** be presented as completed verification or authorization.

**Rationale (non-normative):** Polished wording can otherwise turn a plan into a
claim that an implementation already exists or has been accepted.

**Enforcement (review):** Compare affected claims with their sources and actual
statuses. Review translations for meaning, not literal English syntax. A
keyword or tense checker alone does not determine compliance.

**Evidence:** Source identities and reviewed statement locations, including any
unresolved status or evidence gap. An existing PR review can hold this record.

### DOC-EVIDENCE-001 — Bound measured and verified claims

**Activation:** Load when a document presents an outcome as measured, tested, verified, or established by comparative evidence.

**Context dependencies:** `DOC-STATE-001`

**Automated enforcement:** Advisory

A claim presented as measured, tested, or verified **MUST** identify retrievable
supporting evidence and the implementation, artifact, or configuration it covers.
Material workload, units, conditions, negative results, and uncertainty **MUST**
remain attached to the claim's interpretation. Predictions and recommendations
**MUST** be distinguishable from those outcomes as required by `DOC-STATE-001`.
A missing measurement or inaccessible evidence **MUST** be reported as a gap,
not filled with an invented result. This does not require a benchmark for every
conceptual statement or introduce a new evidence format.

**Rationale (non-normative):** A result under one workload is not proof of every
performance, security, or reliability claim about a system.

**Enforcement (hybrid):** Resolve evidence references and review claim scope
against the referenced report or test. A link or hash alone is insufficient.

**Evidence:** A claim-to-evidence mapping in the document or existing review,
with source identity and the scope of the actual observation.

### DOC-PROC-001 — Expose procedure effects and prerequisites

**Activation:** Load when publishing or changing executable instructions, command examples, prerequisites, verification, or recovery guidance.

**Context dependencies:** `DOC-STATE-001`

**Automated enforcement:** Advisory

A procedure **MUST** expose material prerequisites, its target environment, and
whether an action previews/reads, mutates, verifies, or changes authority. These
are effect descriptions, not required labels or CLI names. Before an action,
the procedure **MUST** identify material destructive or external effects and the
conditions that authorize or prevent it. Placeholders **MUST** be identifiable
and their required values explained. Expected outcomes and failure/stop behavior
**MUST** be distinguished from observed execution, consistent with
`DOC-STATE-001`. Unverified commands **MUST NOT** be called tested or safe;
unknown recovery behavior stays explicit rather than being invented.

**Rationale (non-normative):** Readers need to know what running an example will
change, not merely that its syntax looks plausible.

**Enforcement (review):** Walk through the instructions using the documented
interface or a permitted isolated test. Do not run mutating examples without
execution authority. Record which parts were inspected rather than executed.

**Evidence:** Versioned command/interface references, a bounded walkthrough or
execution record, and any untested branch or missing prerequisite.

### DOC-TERM-001 — Preserve the owning technical vocabulary

**Activation:** Load when naming, translating, or mapping a technical concept across documentation, code, interfaces, or schemas.

**Context dependencies:** `SEM-NAME-001`, `SEM-SURFACE-001`

**Automated enforcement:** Advisory

Documentation **MUST** use the owning vocabulary for a technical concept under
`SEM-NAME-001`. When presenting another language or naming surface, it **MUST**
retain an explicit, unambiguous mapping under `SEM-SURFACE-001`. Explanatory
translations **MUST NOT** silently rename commands, paths, identifiers, schema
fields, or externally owned spellings. This adds a documentation application of
the upstream contracts, not a competing glossary or English-only word list.

**Rationale (non-normative):** A simpler synonym can hide a different operation,
unit, or compatibility boundary.

**Enforcement (review):** Trace affected terms to their code, schema, or project
vocabulary. Review mappings rather than imposing the same spelling everywhere.

**Evidence:** Source locations and the reviewed terminology or translation
mapping. Reuse project terminology records instead of creating another owner.

### DOC-FRESH-001 — Distinguish maintained guidance from history

**Activation:** Load when behavior changes affect current documentation, or when earlier decisions and evidence are used to explain present behavior.

**Context dependencies:** `DOC-STATE-001`, `DOC-EVIDENCE-001`

**Automated enforcement:** Advisory

Documentation presented as current **MUST** identify its applicable source or
supported version through the document or its publication context. When an
authorized change makes that guidance inaccurate, the author **MUST** update the
affected claims within scope or record the unresolved gap without reaffirming
them as current. Historical records **MUST NOT** be rewritten in place for this
purpose when the owning lifecycle protects them. Instead, a current explanation
**MUST** distinguish historical intent from current evidence under
`DOC-STATE-001` and `DOC-EVIDENCE-001`. This requires neither periodic monitoring
nor a new owner field, approval process, or automatic archive rewrite.

**Rationale (non-normative):** A correct account of an old decision does not prove
that the present implementation still follows it.

**Enforcement (review):** Compare affected current guidance with the change and
its source identity. Check history links without modifying protected originals.

**Evidence:** Updated current claims or a tracked gap, source/version scope,
and references to untouched historical records where relevant.

## Approved patterns

These are illustrative, not statements about a real project.

- A proposed per-tenant queue design says that isolation is intended and that
  latency has not been measured. It does not claim the proposal is deployed.
- A procedure explains its dry run before the write operation and says that a
  successful validation is not deployment approval.
- A current guide cites a supported release and links an old ADR as history.

## Rejected patterns

- Replacing "the proposal would" with "the service does" without implementation
  evidence violates `DOC-STATE-001`.
- Calling a cache "proven faster" without a scoped measurement violates
  `DOC-EVIDENCE-001`.
- Describing a publishing command as a read-only preview violates `DOC-PROC-001`.
- Translating a literal command flag changes the owning surface and violates
  `DOC-TERM-001`.
- Using an old accepted ADR alone as proof of current behavior violates
  `DOC-FRESH-001`.

## Exceptions

No exception weakens a MUST obligation. Not-applicable tasks remain
outside scope. Unknown evidence can be reported; it cannot be called a pass.
Project-specific layouts and language preferences remain valid when they preserve
meaning. Conflicting normative sources require explicit resolution, not a
silent specificity override.

## Verification

| Requirement | Minimum verification |
| --- | --- |
| `DOC-STATE-001` | Source-to-statement review of state, conditions, units, and normative strength |
| `DOC-EVIDENCE-001` | Resolve evidence and review identity, conditions, units, and claim limits |
| `DOC-PROC-001` | Authorized interface review or isolated walkthrough of effects and failure branches |
| `DOC-TERM-001` | Review vocabulary ownership and cross-surface mappings |
| `DOC-FRESH-001` | Compare changed current claims or tracked gaps without altering protected history |

## Agent handoff

Use an existing task result or PR review to identify activated Requirement IDs,
source/document identities, checks actually performed, exceptions or gaps, and
compatibility effects. No separate report, approval, or receipt schema is added.
A structural test pass does not prove that every statement is true.

## Compatibility and migration

The first version is `0.1.0`, Development, with Advisory automated
enforcement. Nothing is installed until a project explicitly selects a released
Catalog entry. Existing locks and normative contracts remain unchanged. Adoption
is scoped to authorized new work; it does not rewrite existing documents.

If later adopted, changing the selected set or returning to an earlier lock
requires the consumer's normal explicit preview/apply flow. Such a change cannot
undo effects that a user already performed by following a procedure.

## References

- [Approved ESP-0014](../../proposals/0014_documentation-integrity-contracts.md)
- [Semantic Naming](../core/semantic-naming.md)
- [BCP 14 notation](https://www.rfc-editor.org/info/bcp14)

References explain provenance; they do not import undeclared obligations.
