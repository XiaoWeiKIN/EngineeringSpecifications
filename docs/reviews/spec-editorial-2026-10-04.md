# Existing Specification editorial review — 2026-10-04

This is a non-normative authoring review, not a consumer conformance report,
release approval, or claim of full Google/ASD-STE100 compliance.

## Baseline and scope

Baseline: `5deda62dbacdbc753b9edbb00d1a891c76415b4a`, the prepared Catalog
`1.7.0` release commit. Review covered the existing Data Boundaries, Semantic
Naming, and Go Functional Options prose. The two new documentation Specs and
the other Go contracts are not claimed to have completed this editorial audit.

The change is a bounded editorial patch. It adds a local authoring entry point,
clarifies two subjects, and corrects an insufficient illustration. It does not
change allowed implementations, exceptions, requirement strength, selection,
scopes, dependency graphs, or Automated enforcement levels.

## Review decisions

| Source | Original meaning and issue | Revision | Effect on conformance |
| --- | --- | --- | --- |
| `GO-OPTION-USE-001` | The API chooses a dedicated constructor or configuration method for a distinct mode. "It" follows discussion of a configuration struct. | Name "The API" while retaining `SHOULD` and the distinct-mode condition. | None; the actor is explicit, not new. |
| `GO-OPTION-APPLY-001` | The constructor applies every supplied option exactly once in documented order. "It" immediately follows "The default call". | Name "The constructor". Keep every supplied option, exactly once, and documented order. | None; no new call or option behavior. |
| Data Boundaries, Approved patterns | The parser-only rejection illustration inspects repository/publisher counters without exercising the entry point that owns those effects. | Replace it with a runnable in-memory boundary entry, rejected inputs, and a valid-input positive control. | None; `DATA-EFFECT-001` and its Verification row remain byte-identical. |
| Semantic Naming, five Requirement blocks | Existing subjects, verb contracts, owning-surface mappings, units, and migration exceptions are already explicit for this review's purpose. | Leave the complete source unchanged. | None; no patch version or gratuitous rewording. |

The Data Boundaries example covers only a decoded object's retention field and
two in-memory observers. Invalid-before-effect ordering remains the existing
obligation. This example does not remove the existing transactional or
compensating exception, make Python normative, or add a mandatory consumer
fixture. It is not evidence about a production parser or database.

No Go example code changes. Functional-option representation alternatives,
error behavior, validation timing, nil handling, compatibility, and test duties
remain as before. No claim is made that the Go examples were executed as part
of this prose-only change.

## Checks and their limits

[The regression tests](../../tests/test_spec_editorial.py) execute the exact
marked Python example from the Specification. They also inject deliberately
broken entry points that write or publish before parsing, and entry points
that omit valid-path effects. The original assertions reject those variants.
This checks that the example does not pass merely because its observers are
unused; it is not an exhaustive mutation-testing result.

[The baseline fixture](../../tests/fixtures/spec-editorial-baseline.json)
contains hashes rather than another copy of normative documents. It binds the
review to the baseline commit and records the two exact subject substitutions.
Reversing only those substitutions restores the original section fingerprints.
Untouched applicability, exceptions, Verification rows, routing metadata, and
other protected sections are compared byte-for-byte through their hashes.
The Catalog comparison permits only the two Spec patch versions/digests and
the development Catalog version to change; all routing metadata is retained.

These tests establish the edit boundary and sample behavior, not semantic
equivalence by themselves. The table above records the wording-review judgment
for maintainers to assess. Later intentional normative changes should update
the review baseline with their own compatibility analysis, not bypass a test.

From a complete repository checkout, run:

```bash
python3 -B -m unittest discover -s tests -p test_spec_editorial.py -v
python3 -B scripts/check.py
```

Execution results and tested commit belong in the PR/CI record. A command
listed here is a verification instruction, not evidence that it ran.

## Version and deployment boundary

The changed Data Boundaries and Go Functional Options documents advance from
`0.2.0` to `0.2.1`, with refreshed digests. The development Catalog is `1.7.1`;
its changes remain under Unreleased. Catalog schema 1, all eight Spec IDs, and
all 45 Requirement IDs remain unchanged.

This review does not modify the prepared `1.7.0` release commit, its historical
Changelog entry, or any release tag. It does not publish `1.7.1`, merge a PR,
change RepoFoundry's default version, or migrate consuming project locks.
The scheduled RF #61 task remains tied to the separate `v1.7.0` release.

Author guidance lives in
[governance/specification-authoring.md](../../governance/specification-authoring.md).
AGENTS, CONTRIBUTING, and the formal template link to it. No new `requires`
edges force Core or Go consumers to load writing guidance or documentation
Specs just because this repository's authors use that guidance.
