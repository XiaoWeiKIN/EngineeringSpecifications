# Go Implementation

> **Status:** Development
>
> **Catalog ID:** `languages/go`
>
> **Selection:** Detected
>
> **Routing:** Selection installs this Specification when Go is detected. Load
> it only for tasks that create, change, or review hand-written Go contracts.
>
> **Catalog metadata:** `catalog.json` is the source of truth for version,
> dependencies, file scopes, detection evidence, activation summary, and
> content digest.

## Purpose

Go implementations use idiomatic language constructs while preserving the
semantic names defined by `core/semantic-naming` and the trust transition
defined by `core/data-boundaries`.

## Applicability

### Load this specification when

- creating or changing hand-written `.go` files;
- changing `go.mod`, `go.sum`, `go.work`, committed vendor state, generator
  inputs, generator commands, or committed artifacts owned by a Go module;
- designing exported Go APIs, package boundaries, errors, goroutines, resource
  ownership, or tests;
- mapping external data into Go domain types;
- reviewing Go names whose meaning is not fully determined by the type.

### Do not apply this specification when

- editing generated, vendored, cgo, or protocol-owned code as its authoritative
  source; module and generation consistency requirements still apply to
  repository-owned inputs and projections;
- changing fixed wire, storage, or telemetry names solely to match Go casing;
- replacing a stricter project contract that remains compatible with this
  specification.

## Agent workflow

When this Specification is activated, the implementing or reviewing agent:

1. reads the applicable Core Specifications and the closest project guidance;
2. inventories affected modules, workspaces, committed generated artifacts,
   and their declared validation commands;
3. inspects package call sites before naming or exporting an API;
4. identifies context, error, goroutine, resource, boundary, compatibility,
   platform, toolchain, and build-tag ownership affected by the change;
5. runs applicable formatting, module normalization, regeneration, static
   analysis, focused tests, risk checks, and the repository's canonical
   validation command;
6. reports affected `GO-*` Requirement IDs, evidence, and any governed
   exception.

## Terminology

- An **exported API** includes exported identifiers, method sets, documented
  error identity, and behavior that callers can observe through them.
- A **consumer-owned interface** is declared by the package that needs the
  behavior, rather than by the package that supplies a concrete implementation.
- An **initialism** is an abbreviation pronounced as letters, such as `API`,
  `HTTP`, `ID`, or `URL`.
- A **declared module inventory** is the repository-owned set of Go modules and
  workspaces that its canonical dependency check is expected to cover.
- A **committed generated artifact** is a tracked file whose authoritative
  source is a schema, template, grammar, generator input, or other declared
  source rather than the generated file itself.

## Requirements

### GO-FORMAT-001 — Standard tools own mechanical formatting

Hand-written Go source **MUST** be accepted by `gofmt`. Repositories **SHOULD**
use a deterministic import organizer when they require import grouping beyond
`gofmt`.

**Rationale (non-normative):** Mechanical formatting removes subjective style
decisions from agent output and human review.

**Enforcement (mechanical):** Run `gofmt` or an equivalent no-diff check on
changed Go files.

**Evidence:** A clean formatter check for the reviewed revision.

### GO-MODULE-001 — Module dependency state is reproducible

Every checked-in Go module **MUST** have `go.mod` and `go.sum` state that is
canonical for the repository's declared Go toolchain. Dependency changes
**MUST** run `go mod tidy` or an equivalent deterministic no-diff check over
the declared module inventory. CI **MUST** fail when normalization produces an
uncommitted difference.

A committed vendor tree **MUST** be regenerated from the same module state.
Multi-module repositories **MUST** identify and check every repository-owned
module rather than validating only the module at the repository root.

**Rationale (non-normative):** Tests can pass while module metadata, checksums,
workspace replacements, or vendored content remain stale. Canonical dependency
state makes a revision reproducible for agents, reviewers, and CI.

**Enforcement (mechanical):** Run the repository's declared tidy or dependency
normalization command with the declared Go toolchain, regenerate committed
vendor state when present, and require a clean tracked diff.

**Evidence:** A revision-bound dependency check that names the module inventory,
toolchain, normalization command, and clean result.

### GO-GENERATE-001 — Committed generated artifacts are reproducible

When a Go package or module commits generated artifacts, the repository
**MUST** identify their authoritative inputs and a reproducible generation
command. CI **MUST** regenerate those artifacts with the declared toolchain and
**MUST** fail when the resulting tracked files differ.

Generated output **MUST NOT** be edited as the authoritative source. A scoped
local edit **MAY** support debugging, but the reviewed revision **MUST** be
produced by updating the owning input and rerunning the declared generator.

**Rationale (non-normative):** `go build` and `go test` do not automatically
run `go generate` or project generators, so ordinary test success does not
prove that committed projections match their sources.

**Enforcement (mechanical):** Regenerate the declared artifact inventory in a
clean worktree with the declared generator and toolchain, then require a clean
tracked diff.

**Evidence:** A revision-bound generation check identifying the authoritative
inputs, command, tool versions, generated paths, and clean result.

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

**Enforcement (hybrid):** Use AST-aware naming checks for mechanical casing
rules and review scope, receiver consistency, and protocol exceptions in
context.

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

Single-method interfaces **SHOULD** use a grammatical agent noun derived from
the method when one is clear, such as `Reader`, `Writer`, `Formatter`, or
`CloseNotifier`. A method that reuses a canonical Go operation name such as
`Read`, `Write`, `Close`, `Flush`, or `String` **SHOULD** preserve its
established meaning and signature; otherwise it **SHOULD** use a domain-specific
name.

Boolean methods **SHOULD** read as predicates or capabilities, such as
`IsReady`, `HasEndpoint`, or `CanRetry`. A state expected to grow beyond two
values **SHOULD** use a typed state instead of accumulating Boolean fields.

**Rationale (non-normative):** Call sites such as `json.Marshal`, `time.Now`,
and `store.Save` communicate more than declarations read without package or
receiver context.

**Enforcement (review):** Review exported declarations at representative call
sites. Treat generic package or operation words as review triggers, not
automatic failures.

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

**Enforcement (hybrid):** Static checks can verify context position and forbid
stored contexts. API review verifies interface ownership, exported surface,
and semantic types.

**Evidence:** Type-checking results, API examples, and focused tests using the
consumer contract.

### GO-BOUNDARY-001 — Go boundaries produce domain-safe values

Decoded requests, configuration, environment variables, storage rows, and tool
results **MUST** be treated as untrusted shapes. Boundary code **MUST** parse or
convert them into domain-safe Go values before invoking core logic or side
effects.

Go boundary code **MUST** satisfy `DATA-SHAPE-001`, `DATA-PARSE-001`, and
`DATA-EFFECT-001`. Error and normalization behavior **MUST** satisfy
`DATA-ERROR-001` and `DATA-NORMALIZE-001` when those concerns are present.

Boundary parsers **SHOULD** use focused standard-library facilities such as
`strconv`, `time`, and `net/url` instead of ad hoc conversions. Unknown
external enum values and invalid cross-field combinations **MUST** be rejected
or represented by an explicit unknown policy.

**Rationale (non-normative):** Go struct decoding establishes structure but
does not establish domain validity.

**Enforcement (hybrid):** Keep transport or storage inputs distinct from domain
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

**Enforcement (hybrid):** Static analysis and tests cover returned errors,
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

Concurrency-bearing packages **MUST** run race-enabled tests on the
repository's declared race-capable validation target when the changed path can
execute there. Any package, platform, or path omitted from race coverage
**MUST** record a scoped reason and alternate concurrency evidence.

**Rationale (non-normative):** The garbage collector does not stop leaked
goroutines or close external resources.

**Enforcement (hybrid):** Race-enabled tests, leak checks where available, and
lifecycle review cover creation, cancellation, shutdown, and error paths.

**Evidence:** Revision-bound tests that terminate all goroutines, release
resources, and pass the declared race or alternate concurrency checks, plus
the scope and reason for any omitted path.

### GO-COMPAT-001 — Exported Go contracts migrate deliberately

Exported identifiers, method sets, documented error identity, serialization
tags, and external enum values **MUST** be treated as compatibility contracts
once published.

A necessary Go API rename **MUST** preserve a supported old entry point and add
a `Deprecated:` documentation marker until its removal condition is met.
Generated APIs **MUST** be changed through their source schema.

**Rationale (non-normative):** A stylistic cleanup can otherwise become a
source, wire, storage, or behavioral breaking change.

**Enforcement (hybrid):** API-diff tooling where available, compile-time
compatibility fixtures, schema checks, and migration review.

**Evidence:** Old and new caller tests, deprecation documentation, and a
versioned removal plan.

### GO-TEST-001 — Tests verify contracts and failure boundaries

Go tests **MUST** cover the failure modes introduced or changed by an
implementation. Table-driven tests **SHOULD** be used when multiple inputs
exercise one contract. Boundary tests **MUST** verify that rejected input does
not trigger downstream effects.

Formatting, static analysis, focused tests, and the repository's canonical
validation command **MUST** pass before completion.

Validation **MUST** include a risk-based compile or test matrix for each
changed behavior that depends on supported Go versions, target platforms,
architectures, or build tags. A materially affected dimension that is not
exercised **MUST** be disclosed as a scoped exception with alternate evidence.

**Rationale (non-normative):** Agent-generated implementations need fast,
specific feedback at the violated contract.

**Enforcement (mechanical):** Repository CI runs the declared formatter,
analyzer, focused test targets, canonical validation command, and applicable
toolchain, platform, architecture, and build-tag matrix dimensions.

**Evidence:** Revision-bound CI results, focused test output, the exercised
matrix, and governed exceptions for intentionally uncovered dimensions.

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

A multi-module repository can satisfy `GO-MODULE-001` with one deterministic
command that enumerates every declared module, runs the repository's selected
tidy policy, regenerates vendor state when present, and fails on a tracked
diff. A generator check can use the same pattern for its declared artifact
inventory.

## Rejected patterns

- `type HttpClient` and `parseUrl` violate `GO-NAME-001`.
- Package and type pairs such as `http.HTTPServer` may violate `GO-NAME-002`
  when the package already supplies the missing context.
- Committing changed module metadata without normalizing every declared module
  violates `GO-MODULE-001`.
- Hand-editing a committed generated file without updating its authoritative
  input and regenerating it violates `GO-GENERATE-001`.
- `response := decoded.(DomainType)` violates `GO-BOUNDARY-001`.
- Logging an error in every layer before returning it violates
  `GO-ERROR-001`.
- Starting a goroutine without cancellation or shutdown violates
  `GO-LIFECYCLE-001`.
- Changing tag- or platform-specific behavior while testing only the default
  build violates `GO-TEST-001` unless a scoped exception supplies alternate
  evidence.
- Renaming a published exported symbol for casing alone violates
  `GO-COMPAT-001`.

## Exceptions

Generated, vendored, cgo, and protocol-owned code may retain upstream names and
forms. Repositories may maintain versioned lint baselines for legacy code.
Exceptions must identify their source, scope, and removal condition. They do
not permit new hand-written code to bypass boundary, error, lifecycle, or
compatibility requirements.

Toolchain, platform, architecture, build-tag, and race exceptions must identify
the untested dimension, why the canonical CI cannot exercise it, the alternate
evidence, and a review or removal condition. They do not permit a repository to
silently omit materially affected supported behavior.

## Verification

| Requirement | Minimum verification |
| --- | --- |
| `GO-FORMAT-001` | No-diff `gofmt` check |
| `GO-MODULE-001` | Declared module inventory normalization and clean tracked diff |
| `GO-GENERATE-001` | Declared artifact regeneration and clean tracked diff |
| `GO-NAME-001` | AST-aware casing check and contextual review |
| `GO-NAME-002` | Exported API and call-site review |
| `GO-API-001` | Type checking and API contract tests |
| `GO-BOUNDARY-001` | Parser and no-side-effect rejection tests |
| `GO-ERROR-001` | Error identity, wrapping, translation, and signal tests |
| `GO-LIFECYCLE-001` | Shutdown, resource, race, and leak tests |
| `GO-COMPAT-001` | API or schema compatibility tests |
| `GO-TEST-001` | Repository canonical CI |

## Agent handoff

An agent applying this Specification reports:

```text
Activated requirements: <GO-* IDs and applicable upstream Core IDs>
Packages and public contracts: <affected packages, APIs, errors, and schemas>
Dependency and generation state: <module inventory, generators, or not applicable>
Verification: <gofmt, tidy/no-diff, regeneration/no-diff, analyzer, focused tests, race, matrix, or lifecycle evidence>
Exceptions: none | <generated, vendored, protocol-owned, or legacy scope>
Compatibility or migration: none | <preserved API and removal condition>
```

## Compatibility and migration

Version `0.4.0` preserves every existing `GO-*` Requirement ID, adds
`GO-MODULE-001` and `GO-GENERATE-001`, and strengthens `GO-NAME-002`,
`GO-LIFECYCLE-001`, and `GO-TEST-001`. The naming change is Go-specific and
does not govern Java, Python, database, configuration, wire, storage, or
telemetry names.

Repositories adopting `0.4.0` should first inventory modules, committed
generated artifacts, concurrency-bearing packages, and supported validation
dimensions. They must not bulk-rename stable APIs, schemas, or stored values
without a reviewed migration. Consumers that cannot yet satisfy the new
Development requirements can remain pinned to an earlier Catalog revision
while they prepare the required checks.

## References

- [ESP-0007: Separate Spec selection from task activation](../../proposals/0007_agent-task-activation-and-data-boundaries.md)
- [Semantic Naming](../core/semantic-naming.md)
- [Data Boundaries](../core/data-boundaries.md)
- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
- [Go Doc Comments](https://go.dev/doc/comment)
- [Go `context` package](https://pkg.go.dev/context)
- [Go Modules Reference: `go mod tidy`](https://go.dev/ref/mod#go-mod-tidy)
- [Go command documentation: generate](https://pkg.go.dev/cmd/go#hdr-Generate_Go_files_by_processing_source)
- [Go Data Race Detector](https://go.dev/doc/articles/race_detector)
