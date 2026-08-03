# Semantic Naming

> **Status:** Development
>
> **Catalog ID:** `core/semantic-naming`
>
> **Selection:** Required
>
> **Routing:** Selection installs this Specification. Load it only when the
> task changes shared names, semantic operations, cross-surface mappings,
> units, states, or naming compatibility.
>
> **Catalog metadata:** `catalog.json` is the source of truth for version,
> dependencies, file scopes, detection evidence, activation summary, and
> content digest.

## Purpose

Names expose observable engineering contracts. A shared vocabulary reduces the
number of meanings that an implementation, reviewer, or coding agent must infer
from local context.

This Specification governs semantic meaning across naming surfaces. It does
not prescribe language casing, project vocabulary, or the implementation
mechanism used to parse external data.

## Applicability

### Load this specification when

- introducing or renaming a shared concept, operation, state, identifier, or
  unit;
- naming a parser, decoder, validator, normalizer, converter, loader, lookup,
  plan, or executor;
- mapping one concept across code, schemas, storage, protocols, metrics, or
  documentation;
- reviewing whether a name communicates cardinality, failure, compatibility,
  or material side effects.

### Do not apply this specification when

- editing names generated or vendored from an owning source outside the
  repository;
- preserving a fixed external spelling;
- choosing casing or syntax already defined by an applicable language,
  framework, database, protocol, or project Specification;
- changing implementation details that introduce no shared or observable
  vocabulary.

An adapter still activates the cross-surface mapping requirements when an
external name enters a different internal surface.

## Agent workflow

When this Specification is activated, the implementing or reviewing agent:

1. searches the repository for the existing concept and its call sites;
2. identifies every affected surface and its compatibility owner;
3. selects a semantic verb from its observable result, failure, cardinality,
   and side effects;
4. records explicit mappings instead of deriving external spellings from an
   implementation identifier;
5. runs the applicable Verification entries and reports affected Requirement
   IDs, evidence, and migration effects.

## Terminology

- A **surface** is a naming domain with its own compatibility rules, such as a
  language API, wire schema, database, metric system, or user-facing document.
- A **semantic value** is a representation whose type or constructor result
  preserves facts established while interpreting weaker input.
- **Normalization** idempotently converts an accepted value to a documented
  equivalent form under an explicit equivalence relation.
  **Canonicalization** selects the one stable representation required by a
  contract.
- **Extraction** returns an existing embedded value or view from a containing
  value. The surrounding API identifies the extracted subject, its source, and
  its cardinality.
- An **owning surface** is the schema, protocol, storage contract, public API,
  or project domain that controls a spelling and its compatibility promise.

## Requirements

### SEM-NAME-001 — Names describe observable contracts

Shared and public names **MUST** describe behavior that callers can observe. A
reviewer must be able to determine the operation's result cardinality, failure
behavior, and material side effects from its name, type, and surrounding API.

Names **SHOULD NOT** use generic words such as `process`, `manage`, `data`, or
`helper` when a stable domain concept or observable operation is available.

**Rationale (non-normative):** Precise names narrow the set of behaviors that a
human or coding agent must consider before making a change.

**Enforcement (review):** Review declarations together with their types and
call sites. Use terminology searches only to find candidates; a word match
alone cannot prove a violation.

**Evidence:** A reviewed API, schema, or documentation change that identifies
the observable contract and reuses the repository's existing vocabulary.

### SEM-VERB-001 — Semantic verbs keep stable meanings

An API **MUST** use the following verbs only when its observable behavior
matches the stated contract:

| Verb | Contract |
| --- | --- |
| `Parse` | Interpret untrusted text, tokens, or weak data and return a semantic value or error |
| `Decode` / `Unmarshal` | Recover structure from an encoding or wire representation |
| `Encode` / `Marshal` | Produce an encoding or wire representation |
| `Validate` | Check constraints without changing the input or returning a stronger representation |
| `Normalize` | Produce a documented equivalent representation idempotently under an explicit equivalence relation |
| `Canonicalize` | Select the single stable representation required by a contract |
| `Extract` | Return an existing embedded value or view from a containing value |
| `Convert` / `Map` / `To...` | Change representations without implying parsing or validation |
| `Load` | Read from a local or persistent source |
| `Fetch` | Retrieve from a remote source with remote failure modes |
| `Lookup` | Search by an exact key where absence is a valid result |
| `List` | Return a collection, potentially with filtering or pagination |
| `Resolve` | Turn an indirect reference into its target |
| `Plan` | Produce operations that have not yet been executed |
| `Execute` | Run a command, query, or previously constructed plan |

An operation named `Normalize...` **MUST** document the accepted input, the
equivalence relation it preserves, and the output form. Applying it again to
its own output **MUST** produce the same result. `Normalize` **MUST NOT** hide
parsing of invalid input, validation-only behavior, default injection,
enrichment, aggregation, local or remote I/O, or material side effects.

An operation named `Extract...` **MUST** make the extracted subject, containing
source, and result cardinality clear through its name, owning type, parameters,
and return type. `Extract` **MUST NOT** be a catch-all name for parsing,
normalization, computation, enrichment, loading, fetching, removal, mutation,
or material side effects.

When one atomic operation necessarily combines semantic stages, its public
contract **MUST** expose the primary observable behavior or use an explicit
composed name. An implementation **MUST NOT** select `Normalize`, `Extract`, or
another generic verb merely because that verb describes one internal step.

A function named `Parse...` **MUST NOT** return only a Boolean. A function named
`Validate...` **MUST NOT** mutate its input unless mutation is part of an
explicit compatibility contract.

**Rationale (non-normative):** Stable verbs let agents reuse behavior without
reconstructing its meaning from every implementation.

**Enforcement (hybrid):** Review function signatures, documented effects, and
tests against the verb table. Static analysis may flag suspicious signatures
but must not infer behavior from a name alone.

**Evidence:** Focused tests covering success, invalid input, absence, and side
effects appropriate to the selected verb.

### SEM-SURFACE-001 — Cross-surface mappings stay explicit

When one concept appears on multiple surfaces, the implementation **MUST**
declare each externally visible spelling and **MUST** test the mappings between
them. It **MUST NOT** mechanically derive a wire, storage, metric, or protocol
name from an implementation identifier unless that derivation is the published
contract.

The owning surface **MUST** control its spelling. A language or project naming
rule **MUST NOT** silently rewrite an external compatibility contract; an
adapter must map the external form into the internal domain form.

**Rationale (non-normative):** Different surfaces evolve under different
compatibility rules. One forced spelling can be unidiomatic internally and
breaking externally.

**Enforcement (hybrid):** Require explicit schema fields, serialization tags,
mapping tables, or adapters. Contract tests verify both directions when round
trips are supported.

**Evidence:** Versioned schemas or mapping code and tests that pin every stable
external spelling.

### SEM-TYPE-001 — Types and names expose semantic distinctions

Public contracts **MUST** distinguish incompatible identifiers, units, states,
and time concepts through types or unambiguous names. Raw numeric values
**MUST** identify their unit when the type does not.

External enum and status values **MUST** have explicit stable spellings and a
defined unknown-value policy.

**Rationale (non-normative):** Structurally similar values are easy to exchange
accidentally, especially when code is generated or transformed by an agent.

**Enforcement (hybrid):** Prefer semantic types, constructors, schema
constraints, and exhaustive state handling. Static analysis may reject known
ambiguous unit names.

**Evidence:** Type-checking results and boundary tests covering unit
conversion, unknown values, and incompatible states.

### SEM-COMPAT-001 — Stable names change through migration

A published external name **MUST NOT** be changed solely for stylistic
consistency. A necessary rename **MUST** define the old-to-new mapping, read and
write behavior, conflict handling, deprecation signal, and removal condition.

**Rationale (non-normative):** Names in APIs, schemas, storage, configuration,
and telemetry become observable compatibility contracts.

**Enforcement (hybrid):** Compatibility review and tests cover old-only,
new-only, and conflicting inputs for the supported migration window.

**Evidence:** A versioned migration plan, compatibility tests, and an
observable deprecation signal.

## Approved patterns

The following mappings are non-normative:

```text
domain concept:   service name
code identifier:  serviceName
wire field:       service_name
metric attribute: service.name
```

The forms differ because each surface has its own owner. Explicit adapters and
tests preserve the common meaning.

The following names expose different behavior:

```text
DecodeRequest(body) -> transport shape or encoding error
ParseCreateCommand(shape) -> domain command or semantic error
Validate(command) -> unchanged command plus success or error
Execute(command) -> side effects or execution error
```

The following names keep normalization and extraction narrow:

```text
NormalizeLineEndings(text) -> equivalent text with documented line endings
ExtractPayload(envelope) -> the payload already contained by the envelope
ParseAndNormalizeURL(raw) -> a parsed URL in the documented normalized form
```

## Rejected patterns

- `ParseConfig(value) bool` violates `SEM-VERB-001` because it discards the
  parsed representation.
- `NormalizeConfig(config)` violates `SEM-VERB-001` when it also injects
  defaults, parses durations, validates fields, or mutates shared state without
  exposing those contracts.
- `ExtractData(source)` violates `SEM-VERB-001` when it performs a remote query,
  computes an aggregate, enriches the result, or leaves the extracted subject
  and cardinality ambiguous.
- Deriving a published JSON field from a renamed implementation field violates
  `SEM-SURFACE-001`.
- Naming an untyped duration `timeout` violates `SEM-TYPE-001` when callers
  cannot determine its unit.
- Renaming a stable field only to match local casing violates
  `SEM-COMPAT-001`.
- Replacing `service.name` with `service_name` in telemetry because code uses
  underscores violates `SEM-SURFACE-001`.

## Exceptions

Generated code, vendored code, and fixed external protocols may retain names
that conflict with local conventions. The owning schema or upstream source
remains authoritative. An adapter must document and test any mapping into a
different internal surface.

## Verification

| Requirement | Minimum verification |
| --- | --- |
| `SEM-NAME-001` | Declaration, type, call-site, and terminology review |
| `SEM-VERB-001` | Signature and behavioral tests for the chosen verb |
| `SEM-SURFACE-001` | Schema or adapter mapping contract tests |
| `SEM-TYPE-001` | Type checking and unit or state boundary tests |
| `SEM-COMPAT-001` | Migration and backward-compatibility tests |

## Agent handoff

An agent applying this Specification reports:

```text
Activated requirements: <SEM-* IDs>
Surfaces and owners: <code, wire, storage, metric, protocol, or documentation>
Verification: <tests, schema checks, API review, or migration evidence>
Exceptions: none | <upstream-owned form and adapter>
Compatibility or migration: none | <old-to-new contract>
```

## Compatibility and migration

Version `1.1.0` preserves every Requirement ID and strengthens
`SEM-VERB-001`. It makes the existing `Normalize` contract explicitly
idempotent, prohibits hidden secondary behavior, and adds the cross-language
`Extract` contract. Consumers updating from `1.0.0` should review declarations
and call sites containing `Normalize` or `Extract`; rename or split operations
whose primary observable behavior is parsing, validation, defaulting,
computation, I/O, mutation, or another more precise semantic verb. Fixed
external and protocol-owned names remain governed by the documented exception
and adapter contract.

Version `1.0.0` separates data-shape parsing into
[`core/data-boundaries`](data-boundaries.md). Existing names and mappings do
not require migration.

`SEM-BOUNDARY-001` is superseded as follows:

| Previous requirement | Replacement |
| --- | --- |
| Decode external data into an untrusted shape | `DATA-SHAPE-001` |
| Produce a domain-safe value before core logic | `DATA-PARSE-001` |
| Prevent rejected input from causing side effects | `DATA-EFFECT-001` |
| Preserve protocol-owned credentials and tokens | `DATA-NORMALIZE-001` |

Consumers that recorded evidence against `SEM-BOUNDARY-001` must remap that
evidence to every applicable replacement ID before claiming coverage of this
version. Requirement IDs `SEM-NAME-001`, `SEM-VERB-001`, `SEM-SURFACE-001`,
`SEM-TYPE-001`, and `SEM-COMPAT-001` preserve their previous meanings.

## References

- [ESP-0007: Separate Spec selection from task activation](../../proposals/0007_agent-task-activation-and-data-boundaries.md)
- [BCP 14](https://www.rfc-editor.org/info/bcp14)
- [Data Boundaries](data-boundaries.md)
