# Go Implementation

> **Status:** Development
>
> **Catalog ID:** `languages/go`
>
> **Selection:** Detected
>
> **Catalog metadata:** `catalog.json` is the source of truth for version,
> dependencies, file scopes, detection evidence, and content digest.

Go implementations use idiomatic language constructs while preserving the
semantic names, boundary guarantees, and compatibility rules defined by
`core/semantic-naming`.

## Applicability

### Load this specification when

- creating or changing hand-written `.go` files;
- designing exported Go APIs, package boundaries, errors, goroutines, resource
  ownership, or tests;
- mapping external data into Go domain types;
- reviewing Go names whose meaning is not fully determined by the type.

### Do not apply this specification when

- editing generated, vendored, cgo, or protocol-owned code whose source defines
  a different form;
- changing fixed wire, storage, or telemetry names solely to match Go casing;
- replacing a stricter project contract that remains compatible with this
  specification.

## Terminology

- An **exported API** includes exported identifiers, method sets, documented
  error identity, and behavior that callers can observe through them.
- A **consumer-owned interface** is declared by the package that needs the
  behavior, rather than by the package that supplies a concrete implementation.
- An **initialism** is an abbreviation pronounced as letters, such as `API`,
  `HTTP`, `ID`, or `URL`.

## Requirements

### GO-FORMAT-001 — Standard tools own mechanical formatting

Hand-written Go source **MUST** be accepted by `gofmt`. Repositories **SHOULD**
use a deterministic import organizer when they require import grouping beyond
`gofmt`.

**Rationale (non-normative):** Mechanical formatting removes subjective style
decisions from agent output and human review.

**Enforcement:** Run `gofmt` or an equivalent no-diff check on changed Go files.

**Evidence:** A clean formatter check for the reviewed revision.

### GO-NAME-001 — Identifiers follow Go casing and context

Go identifiers **SHOULD** use `MixedCaps` or `mixedCaps` rather than underscores,
except where generated code, tests, cgo, or an external contract requires
another form. Initialisms **SHOULD** keep consistent case within an identifier:
`HTTPClient`, `parseURL`, `spanID`, and `apiClient`.

Names **SHOULD** become more descriptive as their scope grows. Receiver names
**SHOULD** be short, reflect the receiver type, and remain consistent across its
methods. Receivers **SHOULD NOT** be named `this`, `self`, or the full type name.

**Rationale (non-normative):** Consistent casing and contextual length make Go
code predictable without repeating information already supplied by types and
receivers.

**Enforcement:** Use AST-aware naming checks for mechanical casing rules and
review scope, receiver consistency, and protocol exceptions in context.

**Evidence:** Passing naming checks plus reviewed declarations and call sites.

### GO-NAME-002 — Package and API names read naturally at call sites

Package names **SHOULD** be short, lowercase, and meaningful when combined with
their exported identifiers. They **SHOULD NOT** repeat information already
provided by the package name.

Ordinary accessors **SHOULD** omit `Get`. Protocol operations named `Get` and
stable compatibility surfaces may retain it. Constructors **SHOULD** use names
whose behavior matches the shared semantic vocabulary: `New`, `NewType`,
`Open`, `Compile`, or an explicit domain operation. `MustX` **MUST** be limited
to contracts where failure is intentionally unrecoverable.

Boolean methods **SHOULD** read as predicates or capabilities, such as
`IsReady`, `HasEndpoint`, or `CanRetry`. A state expected to grow beyond two
values **SHOULD** use a typed state instead of accumulating Boolean fields.

**Rationale (non-normative):** Call sites such as `json.Marshal`, `time.Now`,
and `store.Save` communicate more than declarations read without package or
receiver context.

**Enforcement:** Review exported declarations at representative call sites.
Treat generic package or operation words as review triggers, not automatic
failures.

**Evidence:** API examples or tests demonstrating clear construction, access,
failure, and predicate behavior.

### GO-API-001 — APIs expose the smallest stable behavior

Operations that can block, perform I/O, or be cancelled **MUST** accept
`context.Context` as their first parameter unless a required interface fixes
the signature. Request-scoped contexts **MUST NOT** be stored in long-lived
structs.

Interfaces **SHOULD** be small, declared near their consumer, and introduced
only after a concrete use exists. Implementations **SHOULD** return concrete
types unless callers need substitution. An interface **SHOULD NOT** be added only
to generate a mock.

Identifiers, units, states, and values that must not be mixed accidentally
**SHOULD** use named types or constructors.

**Rationale (non-normative):** Small consumer-owned contracts reduce accidental
compatibility promises and give implementations room to evolve.

**Enforcement:** Static checks can verify context position and forbid stored
contexts. API review verifies interface ownership, exported surface, and
semantic types.

**Evidence:** Type-checking results, API examples, and focused tests using the
consumer contract.

### GO-BOUNDARY-001 — Go boundaries produce domain-safe values

Decoded requests, configuration, environment variables, storage rows, and tool
results **MUST** be treated as untrusted shapes. Boundary code **MUST** parse or
convert them into domain-safe Go values before invoking core logic or side
effects.

Boundary parsers **SHOULD** use focused standard-library facilities such as
`strconv`, `time`, and `net/url` instead of ad hoc conversions. Unknown
external enum values and invalid cross-field combinations **MUST** be rejected
or represented by an explicit unknown policy.

**Rationale (non-normative):** Go struct decoding establishes structure but
does not establish domain validity.

**Enforcement:** Keep transport or storage inputs distinct from domain
commands. Tests must assert that rejected input cannot invoke downstream
effects.

**Evidence:** Table-driven parser tests covering valid, missing, malformed,
unknown, boundary, and cross-field-invalid inputs.

### GO-ERROR-001 — Errors preserve identity and ownership

Expected failures **MUST** return errors rather than panic. An error
**MUST** be wrapped with `%w` when callers need to inspect its cause, and typed
or sentinel error behavior **MUST** remain stable across layers that promise
that identity.

Internal errors **MUST** be translated into protocol errors only at the owning
boundary. A layer **SHOULD NOT** both log and return the same failure when an
outer layer owns the operational signal. Error strings **SHOULD** begin with a
lowercase word and omit terminal punctuation unless a fixed external message
requires otherwise.

**Rationale (non-normative):** Preserved identity supports recovery while clear
ownership prevents duplicate signals and leaking implementation details.

**Enforcement:** Static analysis and tests cover returned errors,
`errors.Is`/`errors.As`, wrapping, boundary translation, and logging ownership.

**Evidence:** Focused error-path tests and reviewed logs or telemetry for a
single emitted operational signal.

### GO-LIFECYCLE-001 — Goroutines and resources have observable owners

Every started goroutine **MUST** have a bounded lifetime, cancellation or
shutdown path, and defined error strategy. Acquired resources **MUST** be
released on every path, and meaningful close errors **MUST** be handled.

Shared mutable state **MUST** have explicit synchronization or ownership.
Implementations **SHOULD** prefer ownership transfer or immutable values when
that reduces lifecycle ambiguity.

**Rationale (non-normative):** The garbage collector does not stop leaked
goroutines or close external resources.

**Enforcement:** Race-enabled tests, leak checks where available, and lifecycle
review cover creation, cancellation, shutdown, and error paths.

**Evidence:** Tests that terminate all goroutines, release resources, and pass
the repository's configured race or concurrency checks.

### GO-COMPAT-001 — Exported Go contracts migrate deliberately

Exported identifiers, method sets, documented error identity, serialization
tags, and external enum values **MUST** be treated as compatibility contracts
once published.

A necessary Go API rename **MUST** preserve a supported old entry point and add
a `Deprecated:` documentation marker until its removal condition is met.
Generated APIs **MUST** be changed through their source schema.

**Rationale (non-normative):** A stylistic cleanup can otherwise become a
source, wire, storage, or behavioral breaking change.

**Enforcement:** API-diff tooling where available, compile-time compatibility
fixtures, schema checks, and migration review.

**Evidence:** Old and new caller tests, deprecation documentation, and a
versioned removal plan.

### GO-TEST-001 — Tests verify contracts and failure boundaries

Go tests **MUST** cover the failure modes introduced or changed by an
implementation. Table-driven tests **SHOULD** be used when multiple inputs
exercise one contract. Boundary tests **MUST** verify that rejected input does
not trigger downstream effects.

Formatting, static analysis, focused tests, and the repository's canonical
validation command **MUST** pass before completion.

**Rationale (non-normative):** Agent-generated implementations need fast,
specific feedback at the violated contract.

**Enforcement:** Repository CI runs the declared formatter, analyzer, focused
test targets, and canonical validation command.

**Evidence:** Revision-bound CI results and focused test output.

## Approved patterns

The following examples are non-normative:

```go
type HTTPClient struct{}

func parseURL(rawURL string) (*url.URL, error) {
	return url.ParseRequestURI(rawURL)
}

type CreateRequest struct {
	Name string `json:"name"`
}

type CreateCommand struct {
	name string
}

func ParseCreateCommand(req CreateRequest) (CreateCommand, error) {
	if req.Name == "" {
		return CreateCommand{}, errors.New("name is required")
	}
	return CreateCommand{name: req.Name}, nil
}
```

The transport request cannot enter core logic until the parser constructs a
domain command.

## Rejected patterns

- `type HttpClient` and `parseUrl` violate `GO-NAME-001`.
- Package and type pairs such as `http.HTTPServer` may violate `GO-NAME-002`
  when the package already supplies the missing context.
- `response := decoded.(DomainType)` violates `GO-BOUNDARY-001`.
- Logging an error in every layer before returning it violates
  `GO-ERROR-001`.
- Starting a goroutine without cancellation or shutdown violates
  `GO-LIFECYCLE-001`.
- Renaming a published exported symbol for casing alone violates
  `GO-COMPAT-001`.

## Exceptions

Generated, vendored, cgo, and protocol-owned code may retain upstream names and
forms. Repositories may maintain versioned lint baselines for legacy code.
Exceptions must identify their source, scope, and removal condition. They do
not permit new hand-written code to bypass boundary, error, lifecycle, or
compatibility requirements.

## Verification

| Requirement | Minimum verification |
| --- | --- |
| `GO-FORMAT-001` | No-diff `gofmt` check |
| `GO-NAME-001` | AST-aware casing check and contextual review |
| `GO-NAME-002` | Exported API and call-site review |
| `GO-API-001` | Type checking and API contract tests |
| `GO-BOUNDARY-001` | Parser and no-side-effect rejection tests |
| `GO-ERROR-001` | Error identity, wrapping, translation, and signal tests |
| `GO-LIFECYCLE-001` | Shutdown, resource, race, and leak tests |
| `GO-COMPAT-001` | API or schema compatibility tests |
| `GO-TEST-001` | Repository canonical CI |

## Compatibility and migration

Version `0.2.0` preserves the `0.1.0` direction and adds stable Requirement
IDs, explicit Go naming rules, and evidence contracts. Repositories should
apply the rules to new and modified code. They must not bulk-rename stable APIs,
schemas, or stored values without a reviewed migration.

## References

- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
- [Go Doc Comments](https://go.dev/doc/comment)
- [Go `context` package](https://pkg.go.dev/context)
