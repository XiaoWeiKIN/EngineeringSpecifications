# Specification editorial follow-up — 2026-10-04

This is a non-normative, bounded content review. It is not a consumer
conformance report, release approval, or Google/ASD-STE100 certification.

## Baseline and scope

Baseline: `4a0268f0895106ab19b86a243d38ad43d86bc328`, the merged first
editorial review (PR #19). The earlier review remains in
[its original note](spec-editorial-2026-10-04.md).

This pass read Go Implementation, Go Performance, Go Capability Factory
Delegation, Technical Documentation Integrity, and Derived Explanation
Integrity. Only Go Implementation and the derived-explanation examples need
changes for the issues resolved here. Reading a document is not proof of every
example, every consumer, or every possible edge case.

## Resolved findings

| Surface | Original issue | Change and controlling contract | Conformance impact |
| --- | --- | --- | --- |
| Go Routing preamble | "Selection installs ... when Go is detected" can be read as installation by detection alone. | Say detection recommends and explicit project selection installs, as already required by ESP-0009. Keep `Selection: Detected`, `required: false`, detection rules and scopes unchanged. | No new selection behavior; correct the misleading summary. |
| `GO-NAME-002` | "They" follows "Package names" although the anti-repetition advice concerns exported identifiers at call sites. | Name "Exported identifiers". The existing `http.HTTPServer` rejected pattern and call-site review already establish that reading. Keep `SHOULD NOT` and package context. | No intended new naming obligation or mandatory rename. |
| Go Approved patterns | The snippet omits its package/import context and does not demonstrate a whole service's effect gate. | Name the required imports and label the example boundary. Execute the exact unchanged Go block in a temporary wrapper. | No change to the Go snippet or consumer duties. |
| Derived Rejected patterns | A "source revision or explicit freshness limitation" can appear to let a disclaimer justify a current-state claim; it also overlooks valid snapshot/digest identities. | Align the example with unchanged `DOC-DERIVED-PROV-001`: unknown identity cannot support a current-state claim, even with a disclaimer. | No new normative duty; remove a misleading example reading. |
| Derived Approved patterns | The short revision example does not illustrate unknown, snapshot-only, or stale-source cases. | Label placeholders and add three non-normative reading cases. Identity is not proof of current applicability. | No required metadata schema, Git format, or renderer. |

[ESP-0009](../../proposals/0009_explicit-spec-selection.md) remains the
installation contract. This change does not reinterpret the existing Detected
metadata spelling or install an optional Specification in any project.

## Reviewed and retained

Go Performance already separates objectives, representative diagnosis,
hypotheses, comparison, low-level admission, and stopping conditions. Keep its
five Requirement blocks, YAML illustration, exceptions, and dependencies
unchanged. No benchmark or hardware measurement was performed in this review.

Go Capability Factory Delegation already distinguishes interface ownership,
optional omission versus invalid nil injection, discovery, and delegate error
identity. Keep its text and examples unchanged in this editorial patch. The
example's handling of a successful delegate that returns a nil or typed-nil
handler merits a separate behavioral review; forwarding that result is not
proof that meaningful capability work occurred. Do not add a runtime rejection
policy under the label of pronoun cleanup. The factory examples were not
compiled or executed in this pass.

Technical Documentation Integrity already distinguishes proposed, current,
verified, and historical claims and permits explicit evidence gaps. Keep it
unchanged; that gap is not permission to strengthen evidence or invent a
result. The synthetic examples are not actual cache or benchmark findings.

These retention decisions describe this review's scope, not a declaration that
all three documents are defect-free.

## Verification and preservation

[The follow-up tests](../../tests/test_spec_editorial_followup.py) reverse only
[the recorded replacements](../../tests/fixtures/spec-editorial-followup.json)
and recover the exact baseline source hashes. They compare protected sections
and reject changed strength, appended obligations, and missing/duplicate
substitutions. Such checks bound the edit; they do not prove semantic
equivalence by themselves.

The original baseline fixture and first review are unchanged. The earlier
Catalog preservation test now permits these two separately recorded patch
identities, while checking their old hashes/versions against its own baseline.
Every other Catalog field and untouched Spec identity remains protected.

The Go test wrapper supplies only package/import context and standard-library
tests. It exercises valid and invalid parser inputs and verifies that removing
rejection or discarding a valid value makes the test fail. Network/module and
toolchain downloads are disabled. A missing Go executable produces an explicit
skip, not a fabricated execution result. CI logs and the PR report whether Go
execution actually ran and which toolchain was used.

Run from a complete checkout:

```bash
python3 -B -m unittest discover -s tests -p test_spec_editorial_followup.py -v
python3 -B scripts/check.py
```

The provenance table is checked as a reviewed example, not interpreted by a
generic conformance classifier. There is no new linguistic lint gate or claim
of accessibility certification. Local full-checkout access was unavailable;
full repository validation belongs to the exact PR checkout in GitHub CI.

## Version and release boundary

Catalog remains development `1.7.1` under Unreleased. Go Implementation moves
from `0.5.0` to `0.5.1`; Derived Explanation Integrity moves from `0.1.0` to
`0.1.1`, with refreshed digests. All eight Spec IDs and 45 Requirement IDs,
selection, scopes, dependency edges, enforcement levels, and Verification
mappings remain unchanged. The only Requirement-body edit names the subject in
`GO-NAME-002`; the derived Requirement bodies are byte-identical.

This follow-up does not publish or move a tag, change the prepared `1.7.0`
commit or its history, update RF #61 or RF defaults, modify the scheduled task,
or migrate a consuming project's lock. Publication of `1.7.1` is separate work.
