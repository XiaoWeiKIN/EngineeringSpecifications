---
schema_version: "1"
id: RR-001
parent_id: R-001
title: "Extract reusable Go engineering practices from mature observability projects — RR-001 Baseline investigation"
status: completed
created: 2026-07-30
updated: 2026-07-30
author: "Codex"
---

# Extract reusable Go engineering practices from mature observability projects — RR-001 Baseline investigation

This round is one bounded investigation pass inside R-001. It does not
create a new Research identity or independently authorize conclusion.

## Focus and Questions

Build the first cross-project evidence matrix for RQ-001 through RQ-005. The
round asks which enforced practices recur, which are already covered, which
shared naming conventions add material value, and which remain
project-specific.

## Scope

Inspect first-party contribution guidance, build targets, CI workflows, lint
configuration, source patterns, and focused tests in OpenTelemetry Collector,
Grafana Loki/Mimir, and Prometheus. Do not infer universal rules from directory
names or library choices.

## Evidence Added

- [RT-001 · OpenTelemetry Collector Go engineering practices](../notes/opentelemetry-collector-practices.md)
- [RT-002 · Grafana Loki and Mimir Go engineering practices](../notes/grafana-observability-practices.md)
- [RT-003 · Cross-project candidate Go requirements](../notes/cross-project-go-requirements.md)
- [RT-004 · Cross-project Go naming conventions](../notes/cross-project-go-naming.md)
- **RT-001** — [OpenTelemetry Collector Go engineering practices](../notes/opentelemetry-collector-practices.md) — addresses `RQ-001`, `RQ-002`, `RQ-004`.
- **RT-002** — [Grafana Loki and Mimir Go engineering practices](../notes/grafana-observability-practices.md) — addresses `RQ-001`, `RQ-002`, `RQ-004`.
- **RT-003** — [Cross-project candidate Go requirements](../notes/cross-project-go-requirements.md) — addresses `RQ-001`, `RQ-002`, `RQ-003`, `RQ-004`.
- **RT-004** — [Cross-project Go naming conventions](../notes/cross-project-go-naming.md) — addresses `RQ-001`, `RQ-002`, `RQ-003`, `RQ-005`.
- **RT-004** — [Cross-project Go naming conventions](../notes/cross-project-go-naming.md) — addresses `RQ-001`, `RQ-002`, `RQ-003`, `RQ-005`.

## Synthesis Delta

The round narrowed a broad list of recurring practices to two new
language-level candidates, three amendments to existing requirements, and a
separate set of project/Harness findings that must not enter `languages/go`.
The naming pass also prevents Go identifier rules from leaking into
cross-language Core or non-Go surfaces.

## Next Inquiry

Research Owner review of candidate wording, especially the breaking strength
of module/generator requirements, the Go-only boundary of naming rules, and the
decision to defer canonical command policy to a future cross-language Research.

## Round Outcome

- 2026-07-30 — Completed for Synthesis review v1.
