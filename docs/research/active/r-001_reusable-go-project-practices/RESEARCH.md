---
schema_version: "1.1"
id: R-001
title: "Extract reusable Go engineering practices from mature observability projects"
status: active
maturity: review_ready
research_type: comparative
synthesis: SYNTHESIS.md
manifest: RESEARCH_MANIFEST.json
created: 2026-07-30
updated: 2026-07-30
owner: "Unassigned"
author: "Codex"
current_round: RR-001
synthesis_revision: "1"
approved_by: ""
approved_at: ""
approval_ref: ""
---

# Extract reusable Go engineering practices from mature observability projects

This controller is the bounded entrypoint for a multi-document Research
package. Keep current questions, routes, findings, and next actions here. Put
focused analysis in the declared corpus, raw evidence in `artifacts/`, and the
current decision-ready view in `SYNTHESIS.md`. Decision readiness never grants
permission to conclude or archive the Research.

## Research Metadata

| Field | Value |
|---|---|
| Date | 2026-07-30 |
| Last Updated | 2026-07-30 |
| Research Type | Comparative |
| Research Owner | Unassigned |
| Author | Codex |
| Lifecycle | active |
| Maturity | review_ready |
| Current Round | RR-001 |
| Synthesis Revision | v1 |
| Approval | Pending |

## Purpose and Decision to Enable

Identify which engineering practices used by mature, production-grade Go
observability projects are reusable enough to strengthen `languages/go`.
The Research must distinguish language-level contracts from repository,
framework, and observability-domain choices, then hand downstream governance a
small set of evidence-backed candidate requirements rather than a copied style
guide.

## Current Snapshot

- Current state: revision-pinned evidence across OpenTelemetry Collector,
  Grafana Loki/Mimir, Prometheus, and Go's official documentation supports two
  new language-level candidates: reproducible module state and reproducible
  committed generated artifacts. Race and support-matrix evidence strengthens
  existing lifecycle/test requirements. Naming evidence supports one narrow
  `GO-NAME-002` amendment for single-method interfaces while preserving a hard
  boundary between cross-language semantics, Go-only style, and project
  vocabulary.
- Next inquiry: Research Owner review of the integrated Synthesis and candidate
  layer boundaries.
- Open blockers: none.

## Research Rounds

Use one round for one bounded pass over the shared Research purpose. A round
may add or reopen Research Questions and may reference any number of corpus
documents.

| Round | Focus | Status | Author | Started | Evidence and outcome |
|---|---|---|---|---|---|
| RR-001 | Baseline investigation | completed | Codex | 2026-07-30 | `rounds/rr-001_baseline.md` |

## Scope and Non-goals

In scope are public repository policies and mechanically observable practices
for hand-written Go code, tests, generated artifacts, dependency hygiene, and
CI feedback. OpenTelemetry Collector is the primary sample; Grafana Loki and
Mimir provide a second ecosystem, and Prometheus is a control sample.

Out of scope are project-specific package layouts, component factories,
telemetry schemas, release processes, vendor choices, and Datafox code or
documentation. Popularity alone is not evidence that a practice should become
normative.

## Research Questions

| ID | Status | Question | Answer or disposition | Evidence |
|---|---|---|---|---|
| RQ-001 | answered | Which practices recur across the sampled repositories and are suitable for reusable Go requirements? | Canonical module state and reproducible committed generation qualify; risk-based race/support matrices reinforce existing requirements. | `notes/cross-project-go-requirements.md` |
| RQ-002 | answered | Which observed practices are project, framework, or observability-domain specific and must remain outside `languages/go`? | Exact import bans, logger/metrics libraries, component/module layouts, deployment modes, and Make target names remain project or framework rules. | `notes/opentelemetry-collector-practices.md`; `notes/grafana-observability-practices.md` |
| RQ-003 | answered | Which candidate requirements add material value beyond the current `languages/go` contract? | `GO-MODULE-001` and `GO-GENERATE-001` close uncovered state-consistency gaps; race and matrix behavior should amend existing IDs. | `notes/cross-project-go-requirements.md` |
| RQ-004 | answered | How can each accepted candidate be enforced and evidenced by a coding-agent Harness? | Run declared normalization/regeneration over the complete module/artifact inventory and fail on diff; bind risk tests to revision-specific CI dimensions and scoped exceptions. | `notes/cross-project-go-requirements.md` |
| RQ-005 | answered | Which naming practices recur across official Go guidance and the sampled repositories, and which should amend the existing `GO-NAME-*` requirements? | Existing rules already cover the shared baseline. Add only a conditional single-method interface/canonical method clause to `GO-NAME-002`; keep Go casing out of Core and keep Collector-specific vocabulary at project/framework level. | `notes/cross-project-go-naming.md` |

Allowed statuses: `open`, `answered`, `deferred`, `invalidated`.

## Method and Sources

Use only first-party repositories, documentation, CI definitions, Makefiles,
lint configuration, source, and tests. Pin every repository observation to a
full Git commit. Treat prose guidance as stated policy and executable checks as
stronger behavioral evidence. Promote a rule candidate only when it is either
supported by at least two independent ecosystems or by Go's official guidance
plus one mature implementation. Record counterexamples and weaker adoption.

## Experiments and Prototypes

No runtime prototype is required. The reproducible procedure is a
revision-pinned source audit: resolve each repository commit, retrieve the
exact declared files, and compare their checks and policies. Candidate
requirements are promoted only if their applicability, enforcement, and
evidence can be stated without referring to a sampled repository.

## Findings

- OTel Collector demonstrates repository-wide coverage through paired
  module/repository targets, clean-diff generation and dependency checks, and
  race/toolchain matrices (`notes/opentelemetry-collector-practices.md`).
- Loki and Mimir independently apply clean-diff generation and dependency
  normalization while keeping exact architecture lints project-scoped
  (`notes/grafana-observability-practices.md`).
- Prometheus and Go's official documentation corroborate the two state
  consistency candidates and the limits of unconditional race testing
  (`notes/cross-project-go-requirements.md`).
- Naming evidence confirms a three-layer boundary: semantic contracts remain
  cross-language, identifier/call-site rules remain Go-only, and domain
  vocabulary remains project/framework-owned
  (`notes/cross-project-go-naming.md`).

## Contradictions and Uncertainty

Repository automation demonstrates what maintainers enforce, not necessarily
whether branch protection marks every observed job as required. The samples
are observability-heavy, and Loki/Mimir share an organizational ecosystem.
Prometheus plus official Go semantics reduce, but do not eliminate, sampling
bias. These limits do not affect module/generator semantics; they lower
confidence in prescribing an exact test matrix.

## Decision Drivers and Options

Rank candidates by cross-project recurrence, Go-level applicability,
mechanical enforceability, incremental value over existing Requirement IDs,
and migration risk.

The downstream options are: retain `languages/go` unchanged; add the two
strongly corroborated requirements and narrowly strengthen existing test
language; or add the broader set of project practices. The middle option ranks
highest because it closes mechanical gaps without importing sampled
architectures.

## Blockers

| ID | Status | Opened | Resolved | Missing capability | Impact | Unblock or resolution |
|---|---|---|---|---|---|---|

## Progress

- [x] (2026-07-30T16:30:25Z) Research created and bounded to public,
  revision-pinned evidence from mature Go observability repositories.
- [x] (2026-07-31) Audited OTel Collector `e864743`, Loki `6962b12`, Mimir
  `9f8400e`, Prometheus `bf5a981`, and relevant official Go documentation.
- [x] (2026-07-31) Answered RQ-001 through RQ-004 and produced candidate
  normative text with enforcement, evidence, exclusions, and falsifiers.
- [x] (2026-07-31) Answered RQ-005 with an explicit cross-language/Go/project
  naming boundary and one narrow `GO-NAME-002` candidate amendment.
- [ ] Obtain Research Owner review; decision readiness does not authorize
  conclusion.

## Outcome

Research is review-ready at Synthesis v1, but remains active. Milestone snapshot: `snapshots/synthesis-v001.md`. Only explicit Research Owner authorization may conclude it.

## Artifacts and Notes

- Manifest: `docs/research/active/r-001_reusable-go-project-practices/RESEARCH_MANIFEST.json`
- Synthesis: `docs/research/active/r-001_reusable-go-project-practices/SYNTHESIS.md`
- Round controllers belong under `rounds/`; managed analysis belongs under
  `notes/`; sparse, immutable Synthesis milestone snapshots belong under
  `snapshots/`; raw logs, benchmarks, traces and captures belong under
  `artifacts/`.

## Revision Notes

- 2026-07-30T16:30:25Z — Initial Research package created.
- 2026-07-31 — Completed the first revision-pinned cross-project evidence
  round and prepared the Synthesis for review.
- 2026-07-31 — Reopened the first round to add RQ-005 after naming conventions
  were added to the requested extraction scope.
- 2026-07-30T16:46:23Z — Marked review-ready at Synthesis v1; Milestone snapshot: `snapshots/synthesis-v001.md`. Research remains active.
