# Semantic Naming

> **Status:** Development
>
> **Catalog ID:** `core/semantic-naming`
>
> **Selection:** Required
>
> **Catalog metadata:** `catalog.json` is the source of truth for version,
> dependencies, file scopes, detection evidence, and content digest.

Names expose observable engineering contracts. A shared vocabulary reduces the
number of meanings that an implementation, reviewer, or coding agent must infer
from local context.

## Applicability

### Load this specification when

- introducing or renaming a shared concept, operation, state, identifier, or
  unit;
- defining a parser, decoder, validator, normalizer, converter, loader, or
  other boundary operation;
- mapping one concept across code, schemas, storage, protocols, metrics, or
  documentation;
- reviewing whether a name accurately communicates cardinality, failure, or
  side effects.

### Do not apply this specification when

- rewriting generated or vendored names whose owning source is outside the
  repository;
- replacing a fixed external spelling only to match local style;
- choosing surface syntax already defined by an applicable language,
  framework, database, or protocol specification.

Those cases still require an explicit mapping when the external name enters a
different internal surface.

## Terminology

- A **surface** is a naming domain with its own compatibility rules, such as a
  language API, wire schema, database, metric system, or user-facing document.
- A **semantic value** is a representation whose type or constructor result
  preserves the facts established while interpreting external input.
- **Normalization** converts equivalent valid values to a documented form.
  **Canonicalization** selects the one stable representation required by a
  contract.

## Requirements

### SEM-NAME-001 — Names describe observable contracts

Shared and public names **MUST** describe the behavior that callers can
observe. A reviewer must be able to determine the operation's result
cardinality, failure behavior, and material side effects from its name, type,
and surrounding API.

Names **SHOULD NOT** use generic words such as `process`, `manage`, `data`, or
`helper` when a stable domain concept or observable operation is available.

**Rationale (non-normative):** Precise names narrow the set of behaviors that a
human or coding agent must consider before making a change.

**Enforcement:** Review declarations together with their types and call sites.
Use terminology checks only to find candidates for review; a word match alone
cannot prove a violation.

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
| `Normalize` | Produce a documented equivalent representation, preferably idempotently |
| `Canonicalize` | Select the single stable representation required by a contract |
| `Convert` / `Map` / `To...` | Change representations without implying parsing or validation |
| `Load` | Read from a local or persistent source |
| `Fetch` | Retrieve from a remote source with remote failure modes |
| `Lookup` | Search by an exact key where absence is a valid result |
| `List` | Return a collection, potentially with filtering or pagination |
| `Resolve` | Turn an indirect reference into its target |
| `Plan` | Produce operations that have not yet been executed |
| `Execute` | Run a command, query, or previously constructed plan |

A function named `Parse...` **MUST NOT** return only a Boolean. A function named
`Validate...` **MUST NOT** mutate its input unless mutation is part of an
explicit compatibility contract.

**Rationale (non-normative):** Stable verbs let agents reuse a behavior without
reconstructing its meaning from every implementation.

**Enforcement:** Review the function signature, documented effects, and tests
against the verb table. Static analysis may flag suspicious signatures but
must not infer semantics from the name alone.

**Evidence:** Focused tests covering success, invalid input, absence, and side
effects appropriate to the selected verb.

### SEM-BOUNDARY-001 — Boundary parsing preserves established facts

External data **MUST** be decoded into an untrusted shape and parsed or
converted into domain-safe values before core logic or irreversible side
effects. A successful parser **MUST** return a representation that preserves
the established invariants.

Raw credentials, signatures, tokens, and protocol fields **MUST NOT** be
normalized unless their owning protocol explicitly requires it.

**Rationale (non-normative):** A validation result that leaves the original weak
shape unchanged forces downstream code to remember facts that the type does not
carry.

**Enforcement:** Use boundary types, constructors, schemas, or parsers whose
result excludes invalid structural states. Contract tests must prove rejected
input cannot trigger downstream side effects.

**Evidence:** Parser tests for valid, missing, malformed, unknown, and
cross-field-invalid inputs, plus a typed or otherwise constrained success
result.

### SEM-SURFACE-001 — Cross-surface mappings stay explicit

When one concept appears on multiple surfaces, the implementation **MUST**
declare each externally visible spelling and **MUST** test the mappings between
them. It **MUST NOT** mechanically derive a wire, storage, metric, or protocol
name from an implementation identifier unless that derivation is the published
contract.

**Rationale (non-normative):** Different surfaces evolve under different
compatibility rules. One forced spelling can be unidiomatic internally and
breaking externally.

**Enforcement:** Require explicit schema fields, serialization tags, mapping
tables, or adapters. Contract tests verify both directions when round trips are
supported.

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

**Enforcement:** Prefer semantic types, constructors, schema constraints, and
exhaustive state handling. Static analysis may reject known ambiguous unit
names.

**Evidence:** Type-checking results and boundary tests covering unit conversion,
unknown values, and incompatible states.

### SEM-COMPAT-001 — Stable names change through migration

A published external name **MUST NOT** be changed solely for stylistic
consistency. A necessary rename **MUST** define the old-to-new mapping, read and
write behavior, conflict handling, deprecation signal, and removal condition.

**Rationale (non-normative):** Names in APIs, schemas, storage, configuration,
and telemetry become observable compatibility contracts.

**Enforcement:** Compatibility review and tests cover old-only, new-only, and
conflicting inputs for the supported migration window.

**Evidence:** A versioned migration plan, compatibility tests, and an
observable deprecation signal.

## Approved patterns

The following pseudocode is non-normative:

```text
raw_request = decode_http_body(body)
command = parse_create_command(raw_request)
execute(command)
```

`parse_create_command` returns a domain command or a structured error.
`execute` never receives the transport shape.

An explicit mapping may preserve different native forms:

```text
code identifier: serviceName
wire field:       service_name
metric attribute: service.name
```

## Rejected patterns

- `ParseConfig(value) bool` violates `SEM-VERB-001` because it discards the
  parsed representation.
- Casting decoded data directly to a domain type violates
  `SEM-BOUNDARY-001`.
- Deriving a published JSON field from a renamed implementation field violates
  `SEM-SURFACE-001`.
- Naming an untyped duration `timeout` violates `SEM-TYPE-001` when callers
  cannot determine its unit.
- Renaming a stable field only to match local casing violates
  `SEM-COMPAT-001`.

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
| `SEM-BOUNDARY-001` | Boundary parser and no-side-effect rejection tests |
| `SEM-SURFACE-001` | Schema or adapter mapping contract tests |
| `SEM-TYPE-001` | Type checking and unit or state boundary tests |
| `SEM-COMPAT-001` | Migration and backward-compatibility tests |

## Compatibility and migration

Version `0.2.0` assigns stable Requirement IDs and makes the existing semantic
direction explicit. Consumers must not interpret adoption as authorization to
rename stable APIs or stored data. Existing code can migrate when it changes
for another reason or when a reviewed compatibility plan exists.

## References

- [BCP 14](https://www.rfc-editor.org/info/bcp14)
- [Parse, don't validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/)
