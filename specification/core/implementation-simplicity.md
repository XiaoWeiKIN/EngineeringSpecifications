# Minimal Sufficient Implementation Complexity

> **Status:** Development
>
> **Catalog ID:** `core/implementation-simplicity`
>
> **Selection:** Required
>
> **Routing:** Selection installs this Specification. Load it only for tasks
> that design, implement, modify, refactor, or review executable code.
>
> **Catalog metadata:** `catalog.json` is the source of truth for version,
> dependencies, file scopes, activation summary, and content digest.

## Purpose

Implementation complexity must earn its cost by satisfying an actual supported
business case, preserving a binding contract, or addressing a demonstrated
engineering problem. Keep common code paths simple and maintainable. Do not
burden ordinary requests with speculative abstractions, defenses, fallbacks, or
optimizations aimed at inputs that the product does not support.

This Specification governs implementation decisions independently of language.
It does not replace security controls, data integrity, explicit compatibility
requirements, or the conventions of an applicable language or project Spec.

## Applicability

### Load this specification when

- designing a function, module, API implementation, algorithm, or execution
  path for an actual feature;
- deciding which input forms or uncommon execution cases to support;
- adding guards, error recovery, fallback logic, caching, or optimization;
- introducing helpers, interfaces, patterns, configuration, or shared utilities;
- reviewing a change for unnecessary branches, states, indirection, or scope.

### Do not apply this specification when

- editing documentation without changing implementation behavior;
- analyzing a historical implementation without proposing a code change;
- modifying generated or vendored code whose source is owned elsewhere;
- deciding product requirements, external API compatibility, or security
  policy: those remain owned by their explicit contracts.

This Spec applies to changes of code in any language. A rare but explicitly
supported case still requires correct behavior. Simplicity alone never
authorizes dropping existing compatibility, security, or correctness guarantees.

## Agent workflow

When this Specification is activated, the implementing or reviewing agent:

1. identifies the supported business behavior, real call sites, expected data,
   upstream guarantees, and affected compatibility or trust boundaries;
2. chooses the simplest correct main path and decides whether any low-frequency
   supported path should be isolated;
3. rejects unsupported cases explicitly and adds only validations or fallback
   behavior justified by the owning contract;
4. changes the smallest relevant area, runs focused correctness tests, and
   measures performance only where optimization complexity is proposed;
5. reviews whether removing any new wrapper, check, branch, state, or
   configuration leaves all supported behavior unchanged.

## Terminology

- A **supported case** is an input or behavior required by the product,
  documented interface, compatibility promise, or binding safety contract.
- The **common path** is the execution path exercised most often by real or
  representative supported calls; it must not be guessed from theoretical
  worst-case inputs.
- A **fast path** handles the common case directly. A **slow path** handles a
  genuinely supported case with higher cost or complexity.
- A **trusted internal contract** is a guarantee already enforced upstream by
  types, validation, or the framework, not an unverified assumption.
- **Fallback** means trying a different execution strategy after the primary
  path fails; it is not required unless an applicable contract demands it.

## Requirements

### SIM-SCOPE-001 — Support real requirements before hypothetical cases

**Activation:** Load when deciding supported inputs, use cases, edge behavior, or an algorithm's scope.

**Context dependencies:** None

**Automated enforcement:** Advisory

Before adding implementation behavior, the engineer or agent **MUST**
establish the supported cases from the feature requirements, call sites,
existing contracts, or representative data. An implementation **SHOULD NOT**
add branches, data structures, or compatibility modes solely for hypothetical
inputs with no supported use case. Explicitly unsupported inputs **MAY** be
rejected instead of generalized.

**Rationale (non-normative):** An unlimited hypothetical input space can
consume maintenance effort without improving the product's supported behavior.

**Enforcement (review):** Compare the proposed cases and branches with feature
requirements, call sites, and existing supported contracts.

**Evidence:** A linked requirement or call-site review identifying supported
and deliberately unsupported behavior.

### SIM-PATH-001 — Keep the common execution path direct

**Activation:** Load when introducing a slow path, special-case branch, or additional work on a frequent execution path.

**Context dependencies:** `SIM-SCOPE-001`

**Automated enforcement:** Advisory

For known or representative frequent operations, the implementation **SHOULD**
keep the common case on a direct, low-overhead path. A genuinely supported but
infrequent complex case **SHOULD** be separated when doing so avoids imposing
its cost or control flow on ordinary requests. An unsupported case **MUST NOT**
be treated as a reason to complicate the common path.

**Rationale (non-normative):** Normal requests should not repeatedly pay for
rare behavior they never exercise.

**Enforcement (review):** Trace representative calls through the common path,
including branches and work performed before returning.

**Evidence:** A call-flow review or focused benchmark when the change claims
a performance benefit; the supported rare case remains covered by a test.

### SIM-FAIL-001 — Fail explicitly outside the supported contract

**Activation:** Load when handling invalid, unsupported, or unexpected inputs or designing fallback behavior.

**Context dependencies:** `SIM-SCOPE-001`

**Automated enforcement:** Advisory

An input or state that violates the explicit supported contract **MUST** have
an observable error or unsupported outcome; code **MUST NOT** silently guess a
replacement input, report ambiguous success, or chain speculative fallbacks.
Recovery or fallback **MAY** be used when an owning resilience or compatibility
contract explicitly requires it, with its scope and failure result documented.

**Rationale (non-normative):** Silent recovery obscures defects and expands the
behavior callers must understand.

**Enforcement (hybrid):** Review unsupported-input handling and exercise one
representative rejection; preserve required resilience tests where applicable.

**Evidence:** A focused test showing a clear failure for unsupported input,
or a documented owning contract justifying bounded recovery.

### SIM-CHECK-001 — Validate at meaningful boundaries

**Activation:** Load when adding guards, null checks, type checks, error wrapping, or defensive validation.

**Context dependencies:** `SIM-SCOPE-001`, `SIM-FAIL-001`

**Automated enforcement:** Advisory

Implementations **MUST** retain checks required at untrusted-input,
trust-transition, integrity, and irreversible-effect boundaries. Within a
trusted internal call chain, they **SHOULD NOT** repeat a check already
guaranteed by an enforced upstream type, protocol, or framework contract
unless the duplicate check protects a distinct failure boundary. Error
wrapping **SHOULD** add actionable context rather than another equivalent
layer.

**Rationale (non-normative):** Repeated defenses obscure real boundaries,
while removing boundary checks can produce unsafe behavior.

**Enforcement (review):** Identify the trust owner of each guard and the
specific failure it prevents; retain relevant boundary regression tests.

**Evidence:** A reviewed boundary map or code diff showing where validation
is enforced and why additional checks are needed.

### SIM-ABSTRACT-001 — Require value from abstraction

**Activation:** Load when extracting helpers, creating interfaces, adding indirection, or consolidating duplicate logic.

**Context dependencies:** `SIM-SCOPE-001`

**Automated enforcement:** Advisory

An abstraction **SHOULD** represent a stable domain concept, material
complexity boundary, or demonstrated reuse. Implementations **SHOULD NOT** add
one-use forwarding functions, generic frameworks, configuration knobs, or
polymorphic layers solely for stylistic symmetry or anticipated reuse.
Small duplication **MAY** remain when sharing it would create more parameters,
branches, coupling, or navigation cost than it removes.

**Rationale (non-normative):** An unnecessary abstraction raises the cost of
understanding and changing each call site.

**Enforcement (review):** Inspect consumers of each new abstraction and
compare the cost of inlining or local duplication.

**Evidence:** Call sites or a review rationale showing the abstraction's
actual semantic boundary or reuse.

### SIM-READ-001 — Keep local control flow understandable

**Activation:** Load when a straightforward implementation gains wrappers, hidden state, nested branches, or special cases.

**Context dependencies:** `SIM-ABSTRACT-001`

**Automated enforcement:** Advisory

For a simple business operation, code **SHOULD** expose its inputs, main
decisions, side effects, result, and failures in local, readable flow.
Implementations **SHOULD NOT** add hidden states, fallback tiers, or layers
of indirection that require repeated navigation without a corresponding
supported behavior or maintenance benefit.

**Rationale (non-normative):** Reviewers should be able to follow the
actual operation without reconstructing an artificial framework.

**Enforcement (review):** Walk through the changed function and its immediate
callers; identify states and control-flow branches that affect supported cases.

**Evidence:** A code review explaining the necessary branches and any
intentional complex supported path.

### SIM-PERF-001 — Optimize demonstrated bottlenecks

**Activation:** Load when proposing caches, complex algorithms, specialized fast paths, or CPU, memory, database, or I/O optimization.

**Context dependencies:** `SIM-PATH-001`

**Automated enforcement:** Advisory

Before introducing optimization that materially increases implementation
complexity, the engineer or agent **MUST** identify the representative workload
and the bottleneck or cost it addresses. The chosen optimization **SHOULD**
target frequent operations, meaningful data sizes, or measured CPU, memory,
database, network, or I/O cost. Code **SHOULD NOT** add speculative caches or
algorithmic machinery for unsupported or unmeasured edge workloads.

**Rationale (non-normative):** Theoretical worst cases are not evidence that
additional machinery helps production users.

**Enforcement (hybrid):** Review the workload assumptions and compare
representative before/after evidence for a claimed performance improvement.

**Evidence:** A profile, trace, benchmark, query plan, or documented workload
showing why the extra complexity is justified. No measurement is required for
a correctness-only fix that does not claim an optimization.

### SIM-CHANGE-001 — Make the smallest sufficient modification

**Activation:** Load when editing existing code or reviewing the scope and complexity of a proposed implementation.

**Context dependencies:** `SIM-SCOPE-001`, `SIM-ABSTRACT-001`

**Automated enforcement:** Advisory

A change **SHOULD** touch only code needed for the supported requirement and
its necessary tests, migration, or safety obligations. It **SHOULD NOT**
bundle unrelated refactoring, API changes, style normalization, or speculative
extension points. Before completion, the implementer **MUST** review newly
introduced branches, checks, fallbacks, wrappers, and configuration: if
removing one preserves all supported behavior and required quality guarantees,
it **SHOULD** be removed.

**Rationale (non-normative):** A local fix is easier to review and regress
when unrelated behavior does not change.

**Enforcement (review):** Compare the patch with the stated behavior, inspect
new complexity, and check focused regression coverage.

**Evidence:** A bounded diff with passing relevant tests and an explanation
for retained non-obvious complexity.

## Approved patterns

These examples are non-normative design sketches, not complete programs.

```text
supported common case -> direct handling -> return
supported rare case   -> isolated handling -> return
unsupported input     -> explicit error
```

A handler receiving already validated, typed internal data can use that
guarantee. The system boundary remains responsible for parsing and validating
untrusted input. A deliberately unsupported format is rejected near entry
rather than guessed into a supported one.

A small operation can remain inline instead of becoming three one-line
forwarding helpers. A shared abstraction is useful when multiple call sites
depend on the same stable domain rule, not just similar syntax.

## Rejected patterns

- Adding multiple fallback parsers for unsupported input formats without a
  documented tolerance contract violates `SIM-FAIL-001`.
- Checking the same guaranteed non-null property in every internal helper,
  without a new failure boundary, conflicts with `SIM-CHECK-001`.
- Introducing a Strategy/Factory layer around one direct implementation solely
  for hypothetical future variants conflicts with `SIM-ABSTRACT-001`.
- Adding a complex cache for a path without a representative workload or
  evidence of bottleneck violates `SIM-PERF-001`.
- Refactoring unrelated modules while fixing one local branch conflicts with
  `SIM-CHANGE-001`.

## Exceptions

A binding security, correctness, resilience, compliance, backward-compatibility,
or project contract remains controlling even when its implementation adds
branches, checks, or fallback behavior. A framework guarantee is trusted only
when it is actually enforced at the relevant boundary. Any supported rare
case must remain correct. Record the owning contract when an apparent
simplicity exception materially affects review.

## Verification

| Requirement | Minimum verification |
| --- | --- |
| `SIM-SCOPE-001` | Review supported cases against requirements and call sites |
| `SIM-PATH-001` | Trace common/rare paths and test supported rare behavior |
| `SIM-FAIL-001` | Exercise representative unsupported input or justified recovery |
| `SIM-CHECK-001` | Review trust-boundary ownership and relevant guard tests |
| `SIM-ABSTRACT-001` | Review abstraction consumers against a direct alternative |
| `SIM-READ-001` | Review local control flow, branches, states, and failure visibility |
| `SIM-PERF-001` | Review representative workload and evidence for nontrivial optimization |
| `SIM-CHANGE-001` | Review patch scope, removable complexity, and focused regressions |

## Agent handoff

An agent applying this Specification reports:

```text
Activated requirements: <SIM-* IDs>
Supported cases: <actual inputs, call sites, and contracts>
Main/rare paths: <direct path; isolated path or none>
Validation and fallback: <trust boundary; contract rationale or none>
Complexity retained: <why each non-obvious branch or abstraction is needed>
Verification: <tests; measurements only for claimed optimizations>
Unsupported cases: <explicit failure outcomes>
```

## Compatibility and migration

Version `0.1.0` introduces a Development implementation-simplicity contract
with eight Advisory Requirements. It adds review obligations for code design,
implementation, refactoring, and review but does not demand rewriting
previously compliant code. Adoption follows the consumer's explicit Catalog
upgrade; no migration of existing project locks or runtime defaults occurs
in this change.

## References

- [ESP-0024: Minimal sufficient implementation complexity](https://github.com/XiaoWeiKIN/EngineeringSpecifications/pull/24)
- [Specification principles](../../governance/specification-principles.md)
- [Specification authoring guidance](../../governance/specification-authoring.md)

The proposal and authoring guide provide provenance and review guidance,
not additional normative obligations.
