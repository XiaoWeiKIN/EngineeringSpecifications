# Data Boundaries

> **Status:** Development
>
> **Catalog ID:** `core/data-boundaries`
>
> **Selection:** Required
>
> **Routing:** Selection installs this Specification. Load it only when the
> task consumes external data, introduces a parser or adapter, crosses a trust
> boundary, or can trigger effects from decoded input.
>
> **Catalog metadata:** `catalog.json` is the source of truth for version,
> dependencies, file scopes, detection evidence, activation summary, and
> content digest.

## Purpose

External data enters the system as an untrusted shape and reaches core logic
only after parsing establishes domain invariants. This boundary prevents weak
representations, guessed fields, invalid combinations, and secret-bearing
values from leaking into downstream behavior.

This Specification defines the cross-language contract. Language, framework,
protocol, and project Specifications own idiomatic types, libraries, Handler
layers, and error representations.

## Applicability

### Load this specification when

- decoding HTTP, RPC, message, event, configuration, environment, storage,
  command-line, file, or tool data;
- converting maps, generic JSON objects, generated transport types, or weak
  scalar values into domain values;
- adding a constructor or parser that can reject invalid input;
- changing normalization, canonicalization, unknown-value handling, boundary
  errors, or side effects reachable from external input;
- reviewing whether a typed SDK or generated schema establishes every domain
  invariant required by the consumer.

### Do not apply this specification when

- moving a value entirely inside a domain that already preserves the required
  invariants;
- formatting output without interpreting it as stronger input;
- editing generated or vendored decoding code whose owning schema remains
  authoritative and an adapter owns the domain transition;
- changing an internal algorithm with no new trust, representation, or effect
  boundary.

## Agent workflow

When this Specification is activated, the implementing or reviewing agent:

1. identifies the external owner, trust level, raw shape, and downstream
   effects;
2. separates decoding from domain parsing and names both operations according
   to `core/semantic-naming`;
3. lists required, optional, unknown, and cross-field-invalid cases;
4. constructs a success representation that preserves established facts;
5. proves rejected input cannot reach downstream effects;
6. reports affected Requirement IDs, parser tests, effect-isolation evidence,
   and any protocol-owned exception.

## Terminology

- An **external value** originates outside the current domain contract,
  including network, storage, configuration, environment, file, user, SDK,
  generated-code, and tool results.
- An **untrusted shape** preserves decoded structure without claiming domain
  validity.
- A **domain-safe value** preserves the invariants required by downstream core
  logic through its type, constructor, schema, or otherwise constrained
  representation.
- A **boundary effect** is I/O, persistence, publication, mutation,
  authentication decision, command execution, or another externally observable
  action reachable from input.

## Requirements

### DATA-SHAPE-001 — Decoding produces an untrusted shape

**Activation:** Load when decoding external bytes, tokens, rows, fields, configuration, or tool results.

**Context dependencies:** None

Boundary code **MUST** decode external bytes, tokens, rows, fields, or tool
results into an explicitly untrusted transport or source shape. Decoding
success **MUST NOT** be treated as proof of domain validity.

The shape **MUST** preserve information required for later semantic checks,
including missing versus present values when that distinction affects the
contract.

**Rationale (non-normative):** Encodings and schemas can establish structure
while leaving ranges, identities, states, permissions, and cross-field rules
unproven.

**Enforcement (hybrid):** Keep transport, storage, configuration, or tool
result types distinct from domain values. Schema checks and review verify that
decoding does not invoke core logic directly.

**Evidence:** Type or schema declarations plus tests for missing, malformed,
unknown, and structurally valid but semantically invalid inputs.

### DATA-PARSE-001 — Parsing returns a domain-safe value

**Activation:** Load when converting an untrusted boundary shape into a domain value or validating a type with no safe zero value.

**Context dependencies:** `DATA-SHAPE-001`

Boundary code **MUST** parse or explicitly convert an untrusted shape into a
domain-safe value before core logic consumes it. Successful parsing **MUST**
return a representation that preserves every established invariant so
downstream code does not repeat the same checks.

A domain with no safe zero value **MUST** require a constructor, parser, or
equivalent operation that can fail.

**Rationale (non-normative):** A Boolean validation result leaves the weak
representation unchanged and forces every downstream caller to remember facts
the representation does not carry.

**Enforcement (hybrid):** Use semantic types, constructors, schemas, or parser
results that exclude invalid structural states. Review signatures and compile-
time boundaries; test valid, boundary, and cross-field-invalid cases.

**Evidence:** Parser or constructor tests and a typed or otherwise constrained
success value used by core logic.

### DATA-EFFECT-001 — Rejected input cannot trigger effects

**Activation:** Load when invalid or partially parsed input could reach writes, messages, commands, or other effects.

**Context dependencies:** `DATA-PARSE-001`

Core logic and boundary effects **MUST NOT** run until every required boundary
parse succeeds. Partial parsing **MUST NOT** leave an externally observable
mutation unless the protocol defines a reviewed transactional or compensating
contract.

**Rationale (non-normative):** Validation after mutation converts malformed
input into partial writes, duplicate messages, authorization mistakes, or
commands executed with guessed values.

**Enforcement (mechanical):** Contract tests use spies, fakes, transactions, or
observable state to prove each rejected input leaves downstream effects
untouched.

**Evidence:** Failure-path tests covering zero calls, zero writes, rollback, or
the protocol's documented compensation behavior.

### DATA-ERROR-001 — Boundary errors are actionable and secret-safe

**Activation:** Load when defining, translating, logging, or returning errors for rejected external input.

**Context dependencies:** `DATA-PARSE-001`

A rejected input **MUST** produce an error that identifies the affected field,
path, or contract and the violated expectation. The error **MUST NOT** expose
credentials, signatures, tokens, passwords, private keys, or unredacted
secret-bearing payloads.

Boundary error translation **MUST** occur at the layer that owns the external
protocol. Internal causes may be preserved only when the receiving contract
can inspect them safely.

**Rationale (non-normative):** Agents and operators need enough structure to
repair invalid input, while secret values must remain outside logs, responses,
and review artifacts.

**Enforcement (hybrid):** Use structured boundary errors or deterministic
field paths. Tests assert public error shape and redaction; review verifies
translation ownership.

**Evidence:** Error-contract tests for missing, malformed, unknown, cross-field
invalid, and secret-bearing inputs.

### DATA-NORMALIZE-001 — Protocol-owned values preserve their contract

**Activation:** Load when trimming, case-folding, normalizing, decoding, reordering, or canonicalizing protocol-owned values.

**Context dependencies:** `SEM-VERB-001`

Boundary code **MUST NOT** trim, case-fold, Unicode-normalize, reorder, decode,
or otherwise transform credentials, signatures, tokens, password material, or
protocol-owned fields unless the owning contract explicitly requires that
operation.

When normalization or canonicalization is required, the implementation
**MUST** document its equivalence rules, ordering relative to verification,
and idempotence or stable-output contract.

**Rationale (non-normative):** A transformation that is harmless for display
text can invalidate a signature, change an identifier, weaken authentication,
or produce a different storage key.

**Enforcement (hybrid):** Review the owning protocol and keep transformations
explicit. Golden tests preserve raw bytes and verify required normalized or
canonical forms.

**Evidence:** Primary protocol references plus raw-value, equivalence,
idempotence, signature, or authentication tests appropriate to the field.

## Approved patterns

The following pseudocode is non-normative:

```text
raw_body = read_request_body(request)
transport = decode_json(raw_body)
command = parse_create_command(transport)
result = execute(command)
encode_response(result)
```

`decode_json` establishes JSON structure. `parse_create_command` establishes
domain invariants and returns a command that `execute` can safely consume.

A rejection test observes the effect boundary:

```text
command, error = parse_create_command(invalid_transport)
assert error.field == "retention_days"
assert command is absent
assert repository.write_count == 0
assert publisher.message_count == 0
```

## Rejected patterns

- Casting a decoded map or transport object directly to a domain type violates
  `DATA-SHAPE-001` and `DATA-PARSE-001`.
- `ValidateRequest(value) bool` followed by reuse of the same weak value
  violates `DATA-PARSE-001` when downstream safety depends on remembered
  checks.
- Writing a row before validating a dependent field violates
  `DATA-EFFECT-001`.
- Returning `invalid token: <raw token>` violates `DATA-ERROR-001`.
- Trimming a signature or lowercasing an opaque identifier without protocol
  authority violates `DATA-NORMALIZE-001`.

## Exceptions

A versioned, typed SDK or generated schema may establish some structural and
semantic facts. The adapter must identify which invariants the upstream
contract proves and must parse every remaining local domain invariant.

Generated and vendored types may cross the decoding boundary unchanged. They
cannot enter core logic as domain-safe values unless their owning contract
proves the complete local invariant set.

## Verification

| Requirement | Minimum verification |
| --- | --- |
| `DATA-SHAPE-001` | Source-shape declarations and malformed or semantically invalid decode cases |
| `DATA-PARSE-001` | Parser or constructor tests and constrained success representation |
| `DATA-EFFECT-001` | No-side-effect rejection tests or transactional compensation tests |
| `DATA-ERROR-001` | Structured error and secret-redaction contract tests |
| `DATA-NORMALIZE-001` | Protocol references and raw-value or canonicalization tests |

## Agent handoff

An agent applying this Specification reports:

```text
Activated requirements: <DATA-* IDs>
Boundary: <source owner> -> <untrusted shape> -> <domain-safe value>
Effects gated: <I/O, write, publish, mutation, auth, or execution>
Verification: <parser, error, redaction, and no-side-effect evidence>
Exceptions: none | <upstream contract and remaining local checks>
```

## Compatibility and migration

Version `0.1.1` adds non-normative Requirement activation summaries and exact
context-dependency metadata. It does not change the behavioral meaning of any
`DATA-*` Requirement ID.

Version `0.1.0` extracts the cross-language behavior previously published as
`SEM-BOUNDARY-001` in `core/semantic-naming` version `0.2.0`. Consumers should
remap existing evidence using the migration table in Semantic Naming.

The split does not authorize changes to existing wire, storage, credential,
signature, token, or public error formats. Adapters can adopt the stronger
internal boundary without changing an owning external surface.

## References

- [ESP-0007: Separate Spec selection from task activation](../../proposals/0007_agent-task-activation-and-data-boundaries.md)
- [Semantic Naming](semantic-naming.md)
- [BCP 14](https://www.rfc-editor.org/info/bcp14)
- [Parse, don't validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/)
- [Harness engineering](https://openai.com/index/harness-engineering/)
