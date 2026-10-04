# Repository-wide editorial consistency review

> **Kind:** Non-normative review record
>
> **Baseline:** `5deda62dbacdbc753b9edbb00d1a891c76415b4a`
>
> **Scope:** All 58 tracked baseline files; current Specifications and guidance
> receive editorial review, while historical/provenance-owned records remain
> byte-preserved.

## Findings and bounded corrections

The review checks repository identity, Catalog availability and release
terminology, document maturity, selection and activation, source ownership,
Requirement wording, example coverage, reference boundaries, and code/test
agreement. It does not reassess the empirical claims in historical research
or certify every external reference as current.

| Finding | Correction | Boundary preserved |
| --- | --- | --- |
| The author entry still named EngineeringWorkflow and omitted documentation | Route to RepoFoundry AI and the local authoring guide; include the documentation layer | No new installed Spec or RF dependency |
| Current guidance treated a Catalog entry as a published release | Distinguish working-tree availability from immutable-tag publication in both languages | Existing release identities are untouched |
| Governance called the repository 0.x and described maturity markers as optional | Separate Catalog version from Development maturity and describe the existing mandatory document-marker check | No Catalog schema or validator change |
| Compliance repeated an incomplete list of Specs with stable IDs | Refer to the current index and selected Catalog instead of a second inventory | No implementation conformance is claimed |
| Release prose treated a local tag check as remote-publication proof | State exactly what the script checks and show the separate remote-identity check | No tag, release policy, or checker behavior change |
| Go Routing said detection installed the optional Spec | Align the explanatory Routing marker with explicit selection | Selection metadata and resolver behavior are unchanged |
| The option-application sentence used an ambiguous It | Name the constructor explicitly | Exactly-once and documented-order obligations are unchanged |
| The no-effect example invoked only the parser | Exercise the entry point with recording spies, a valid control, and deliberately broken controls | DATA-EFFECT-001 is unchanged |
| The factory example could return a successful nil handler | Reject a nil interface result in the non-normative example; replay the same Go case before and after | The existing no-false-success obligation is unchanged |
| Example imports, alternatives, synthetic IDs, and reference authority were implicit | Label fragments and placeholders; distinguish embedded attribution from derived authority; state the reference boundary | No renderer, style guide, or new consumer test strategy is mandated |

All eight Specs receive patch revisions and refreshed source digests. The next
working-tree Catalog is `1.7.1`, with its changes under `Unreleased`.
Prepared `1.7.0` content remains at the baseline commit; this review does not
retag, release, merge, or alter the RF #61 publication dependency.

## Contract comparison

The old and new Catalogs have the same eight IDs, paths, scopes, selection
flags, detection metadata, and dependencies. All 45 Requirement IDs, ordered
Activation/Context dependencies/Automated enforcement metadata, enforcement
classes, evidence fields, and Verification mappings are preserved.

Whitespace-normalized Requirements sections match the baseline exactly after
one explicit normalization: in GO-OPTION-APPLY-001, the sentence subject
changes from `It` to `The constructor`. No obligation, quantifier, condition,
exception, or requirement strength is otherwise edited. This comparison is
stronger than a keyword count, but it is still not a general semantic proof.

All dated Changelog content from `[1.7.0]` onward is byte-preserved. Approved
proposals, R-001 source documents, rounds, Synthesis snapshots, manifests,
research indexes, and allocator state are byte-preserved. The ten source
records in the Research manifest retain their declared sizes and SHA-256.

## Validation and reproducibility

Run the canonical standard-library check from the repository root:

```bash
python3 -B scripts/check.py
```

It includes six new authoring/packaging consistency tests and four tests of the
exact documented boundary fragment. The failure tests call the entry point;
valid input reaches both spies, while deliberate premature writes/publications
make the same documented assertions fail.

With a local Go toolchain, run the additional offline example check:

```bash
python3 -B tests/check_go_examples.py
```

This compiles the exact Go implementation, functional-options, factory, and
alternative closed-interface fragments with their documented imports. Nine
representative cases cover parser rejection, options, forwarding, error
identity, absence, and nil-result handling. The closed-interface alternative
is compile-only. The local check used Go 1.23.2 on Linux/amd64 with module
network access disabled. Before the example repair, the nil-handler case
failed; after the repair, the same case passed.

The canonical check does not require Go. These examples do not establish
conformance by a consuming repository, full platform/race coverage, semantic
clarity, or accessibility. Complete CI results belong to the PR's exact head,
not to the historical baseline or a future release.

## Questions deliberately not resolved by editorial rewriting

- GO-NAME-002 uses a package-name subject followed by a statement about repeated
  package context. Clarifying whether the obligation directly governs exported
  identifiers needs a separately reviewed semantic interpretation, not a
  silent actor change in this patch.
- Approved ESP-0014 contains a duplicate non-normative metadata line, and older
  approved ESPs retain 0000 identifiers. Those are historical records; this
  review records the issues without renumbering or rewriting approval history.
- An external Spec link in a historical Research record may name the mutable
  source path. The record describes its original investigation and is not
  refreshed into a present-day conformance claim.

## Tracked-file coverage

Every path below was read as UTF-8 and verified against its baseline Git blob.
All files participated in the inventory and applicable structural/link checks.
For preserved historical content, the check covers identity, local references,
metadata, and provenance boundaries rather than re-running its research.
The table records the final disposition, not a claim that every file needed an
edit. New review tools and guidance are listed after the baseline inventory.

| Baseline path | Disposition |
| --- | --- |
| `.github/workflows/check.yml` | Reviewed; behavior/schema/workflow preserved |
| `.gitignore` | Reviewed; no consistency change needed |
| `AGENTS.md` | Reviewed; current guidance aligned |
| `CHANGELOG.md` | Reviewed; Unreleased entry only, dated history preserved |
| `CONTRIBUTING.md` | Reviewed; current guidance aligned |
| `LICENSE` | Reviewed; no consistency change needed |
| `README.md` | Reviewed; current guidance aligned |
| `README.zh-CN.md` | Reviewed; current guidance aligned |
| `RELEASING.md` | Reviewed; current guidance aligned |
| `catalog.json` | Reviewed; patch versions/digests only |
| `compliance/README.md` | Reviewed; current guidance aligned |
| `docs/.epctl/lock` | Reviewed for history/provenance; bytes preserved |
| `docs/.epctl/state.json` | Reviewed for history/provenance; bytes preserved |
| `docs/RESEARCH.md` | Reviewed for history/provenance; bytes preserved |
| `docs/research/active/r-001_reusable-go-project-practices/RESEARCH.md` | Reviewed for history/provenance; bytes preserved |
| `docs/research/active/r-001_reusable-go-project-practices/RESEARCH_MANIFEST.json` | Reviewed for history/provenance; bytes preserved |
| `docs/research/active/r-001_reusable-go-project-practices/SYNTHESIS.md` | Reviewed for history/provenance; bytes preserved |
| `docs/research/active/r-001_reusable-go-project-practices/notes/README.md` | Reviewed for history/provenance; bytes preserved |
| `docs/research/active/r-001_reusable-go-project-practices/notes/cross-project-go-naming.md` | Reviewed for history/provenance; bytes preserved |
| `docs/research/active/r-001_reusable-go-project-practices/notes/cross-project-go-requirements.md` | Reviewed for history/provenance; bytes preserved |
| `docs/research/active/r-001_reusable-go-project-practices/notes/go-performance-optimization.md` | Reviewed for history/provenance; bytes preserved |
| `docs/research/active/r-001_reusable-go-project-practices/notes/grafana-observability-practices.md` | Reviewed for history/provenance; bytes preserved |
| `docs/research/active/r-001_reusable-go-project-practices/notes/opentelemetry-collector-practices.md` | Reviewed for history/provenance; bytes preserved |
| `docs/research/active/r-001_reusable-go-project-practices/rounds/rr-001_baseline.md` | Reviewed for history/provenance; bytes preserved |
| `docs/research/active/r-001_reusable-go-project-practices/rounds/rr-002_go-performance-optimization.md` | Reviewed for history/provenance; bytes preserved |
| `docs/research/active/r-001_reusable-go-project-practices/snapshots/synthesis-v001.md` | Reviewed for history/provenance; bytes preserved |
| `docs/research/active/r-001_reusable-go-project-practices/snapshots/synthesis-v002.md` | Reviewed for history/provenance; bytes preserved |
| `docs/specification-model.md` | Reviewed; current guidance aligned |
| `docs/specification-model.zh-CN.md` | Reviewed; current guidance aligned |
| `governance/README.md` | Reviewed; current guidance aligned |
| `governance/enforcement-lifecycle.md` | Reviewed; behavior/schema/workflow preserved |
| `governance/lifecycle.md` | Reviewed; current guidance aligned |
| `governance/specification-principles.md` | Reviewed; current guidance aligned |
| `proposals/0000-enforcement-levels-and-telemetry.md` | Reviewed for history/provenance; bytes preserved |
| `proposals/0000-template.md` | Reviewed for history/provenance; bytes preserved |
| `proposals/0000_requirement-level-context-activation.md` | Reviewed for history/provenance; bytes preserved |
| `proposals/0000_requirement-level-context-activation.zh-CN.md` | Reviewed for history/provenance; bytes preserved |
| `proposals/0007_agent-task-activation-and-data-boundaries.md` | Reviewed for history/provenance; bytes preserved |
| `proposals/0008_versioned-catalog-releases.md` | Reviewed for history/provenance; bytes preserved |
| `proposals/0009_explicit-spec-selection.md` | Reviewed for history/provenance; bytes preserved |
| `proposals/0010_task-activation-router.md` | Reviewed for history/provenance; bytes preserved |
| `proposals/0014_documentation-integrity-contracts.md` | Reviewed for history/provenance; bytes preserved |
| `proposals/README.md` | Reviewed for history/provenance; bytes preserved |
| `schemas/catalog.schema.json` | Reviewed; behavior/schema/workflow preserved |
| `scripts/check.py` | Reviewed; behavior/schema/workflow preserved |
| `scripts/check_release.py` | Reviewed; behavior/schema/workflow preserved |
| `specification/0000-template.md` | Reviewed; current guidance aligned |
| `specification/README.md` | Reviewed; current guidance aligned |
| `specification/core/data-boundaries.md` | Reviewed; editorial patch and digest refresh |
| `specification/core/semantic-naming.md` | Reviewed; editorial patch and digest refresh |
| `specification/documentation/derived-explanations.md` | Reviewed; editorial patch and digest refresh |
| `specification/documentation/technical-documentation.md` | Reviewed; editorial patch and digest refresh |
| `specification/languages/go.md` | Reviewed; editorial patch and digest refresh |
| `specification/languages/go/factory-delegation.md` | Reviewed; editorial patch and digest refresh |
| `specification/languages/go/functional-options.md` | Reviewed; editorial patch and digest refresh |
| `specification/languages/go/performance.md` | Reviewed; editorial patch and digest refresh |
| `tests/test_catalog.py` | Reviewed; align exact version assertions |
| `tests/test_release.py` | Reviewed; behavior/schema/workflow preserved |

New files: `governance/specification-writing.md`, this review record,
`tests/test_documentation_examples.py`, `tests/test_editorial_consistency.py`,
and the optional `tests/check_go_examples.py`.

The temporary CI snapshot used to obtain the pinned public repository is a
work-branch transport artifact. Temporary transport files are removed before
this change is marked ready; they are not a shipped workflow or consumer feature.
