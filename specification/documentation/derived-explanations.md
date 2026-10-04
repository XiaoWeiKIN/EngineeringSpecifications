# Derived Engineering Explanations

> **Status:** Development
>
> **Catalog ID:** `documentation/derived-explanations`
>
> **Selection:** Explicit
>
> **Routing:** Selection installs this Specification. Apply it only to tasks
> producing or reviewing explanations of engineering facts, not all matched files.
>
> **Catalog metadata:** `catalog.json` owns version, dependencies, scopes,
> activation summary, and content digest.

## Purpose

Keep a generated explanation traceable to its sources and prevent its
presentation from implying new authority. Preserve access to material engineering
information across text, diagrams, interactive pages, presentations, and videos.

No renderer, language, media format, frame rate, dependency, or deployment service
is required. This is a limited information-integrity contract, not a complete
accessibility standard or certification.

## Applicability

### Load this specification when

- Creating or reviewing a derived explanation of engineering facts.
- Changing a generator, storyboard, caption, or view that can change those facts.
- Republishing a derived view after a material source or interpretation change.

### Do not apply this specification when

- Editing unrelated program logic or data with no explanation-producing effect.
- Changing decoration that carries no engineering information.
- Executing a normal application workflow solely because its source file matches.

Broad file scope includes generator sources and media companions. Task intent,
not the extension, decides applicability. Binary outputs are not parsed as
normative text. Out-of-repository exports require explicit producer/output review;
this contract does not claim that a path Router can gate them automatically.

## Agent workflow

Identify the canonical sources, represented versions, and intended reader task.
Check only the affected explanation and producer. Compare the claims and limits
with those sources, then inspect the delivered view and its text equivalent.
Report any absent runtime, media render, accessibility check, or source evidence
without claiming a pass. Do not install tools, upload sources, or publish output
without the corresponding task authority.

## Terminology

A **derived explanation** presents information obtained from another owning
source. The owning source can itself be generated, such as a signed test report.
**Material information** includes facts and limits needed for the stated reader
task. A **companion** is a retrievable source or text representation distributed
with, embedded in, or clearly linked from the explanation.

Uppercase BCP 14 keywords govern the requirements. A byte digest
proves neither a source's authenticity nor the truth of its statements.

## Requirements

### DOC-DERIVED-AUTH-001 — Rendering does not confer authority

**Activation:** Load when an explanation presents requirements, decisions, approvals, implementation state, or verification results from another source.

**Context dependencies:** `DOC-STATE-001`, `DOC-EVIDENCE-001`

**Automated enforcement:** Advisory

A derived explanation **MUST** identify its derived status in the view or an
unambiguous accompanying context. It **MUST NOT** acquire or claim independent
requirement, decision, approval, or verification authority merely because it was
rendered or is easier to read. States and evidence limits **MUST** be preserved
under `DOC-STATE-001` and `DOC-EVIDENCE-001`. Simulation, interpolation, animated
reading order, and measured behavior **MUST** be distinguishable when a reader
could confuse them. Exact embedded evidence retains its source identity; its
container does not create a new decision or test outcome. An owning lifecycle
can designate an authoritative generated artifact, but rendering alone is not
that designation.

**Rationale (non-normative):** An attractive diagram or video can appear more
certain or official than the evidence it explains.

**Enforcement (review):** Compare displayed conclusions and status with the
sources. Check labels for simulated behavior and presentation-only time.

**Evidence:** Identified source/view versions and a review of authority, state,
and measurement boundaries. No new approval record is implied.

### DOC-DERIVED-PROV-001 — Bind a view to identifiable sources

**Activation:** Load when exporting, sharing, or regenerating an engineering explanation from source artifacts, local changes, or recorded measurements.

**Context dependencies:** `DOC-DERIVED-AUTH-001`, `DOC-FRESH-001`

**Automated enforcement:** Advisory

An explanation **MUST** identify the source artifacts or retained snapshot it
actually represents, using resolvable revisions, immutable identities, or content
digests paired with retrievable source bytes. A digest without a source locator
is insufficient. A repository HEAD **MUST NOT** be presented as identifying
uncommitted source changes; retain the relevant snapshot or equivalent byte
identity. Generation method/version and assumptions that affect interpretation
**MUST** be recorded in the view or companion. Material source changes **MUST**
trigger regeneration within the authorized work or a clear stale/unknown notice,
consistent with `DOC-FRESH-001`. No continuous monitoring is required.

The provenance **MUST** preserve `DOC-DERIVED-AUTH-001` when exported separately.
It **MUST NOT** expose secrets or bypass the source's sharing restrictions. When
restricted sources cannot be distributed, retain approved locators and state
access limits; do not invent a public evidence URL or claim public verifiability.
A fixed JSON schema, absolute machine path, or bundled full repository is not
required.

**Rationale (non-normative):** A viewer needs to distinguish an explanation of
an old or locally modified source from a statement about today's repository.

**Enforcement (hybrid):** Resolve source/companion locators, verify supplied
byte identities, and review generation assumptions and disclosure boundaries.

**Evidence:** Source and view identities, generation inputs/method, a digest
check where applicable, and recorded stale or restricted-source limitations.

### DOC-A11Y-001 — Preserve equivalent access to material information

**Activation:** Load when a diagram, interactive control, presentation, or audio/video carries material engineering information for its intended reader task.

**Context dependencies:** None

**Automated enforcement:** Advisory

Material information **MUST** have an accessible text equivalent in the view or
an associated companion. Equivalent information includes conditions, state,
uncertainty, and relevant visual relationships, not merely the title of an image.
Color, position, animation, or audio **MUST NOT** be the sole way to obtain it.
Essential interactive functions **MUST** have a keyboard-operable equivalent;
required information **MUST NOT** be available only through pointer hover or drag.

Prerecorded speech or other meaningful audio accompanying visual explanations
**MUST** have synchronized captions when it contributes information. Essential
visual-only facts **MUST** be described in the associated text. A silent video
needs no fabricated audio captions. A clearly identified redundant media version
may point to a complete accessible text source instead of introducing another
fact owner. A transcript alone **MUST NOT** be described as meeting a separate
synchronized-caption obligation. Project or applicable external accessibility
requirements can be stricter; this limited contract **MUST NOT** be represented
as full WCAG conformance.

**Rationale (non-normative):** Readers should not lose facts, limitations, or
required actions because they cannot see a color, use a pointer, or hear audio.

**Enforcement (hybrid):** Inspect the actual view with its text equivalent;
exercise essential functions using a keyboard. Inspect caption synchronization
and visual descriptions when applicable. Static markup checks cannot establish
semantic equivalence; unavailable renderers mean an unperformed check, not pass.

**Evidence:** Reviewed view/text identities and applicable keyboard, caption,
and equivalence checks, with untested modes explicitly recorded.

## Approved patterns

These examples are non-normative.

- A dependency SVG has a text edge list, labels direct/dependency roles without
  color alone, and links the exact Requirement source snapshot.
- An interactive page offers labeled keyboard controls and a static fact list.
  Animation time is explicitly a reading sequence, not measured execution time.
- A video carries synchronized captions and a companion explanation of essential
  visual relationships; both identify their sources and represented version.

## Rejected patterns

- Calling a rendered story an accepted ADR violates `DOC-DERIVED-AUTH-001`.
- Showing only HEAD while describing uncommitted files, with no retained source
  identity, violates `DOC-DERIVED-PROV-001`.
- A hash beside a missing snapshot cannot establish provenance under
  `DOC-DERIVED-PROV-001`.
- A green/red-only outcome or pointer-only evidence control violates
  `DOC-A11Y-001`.

## Exceptions

No exception weakens a MUST obligation. Decorations and unrelated code
remain outside scope. Reusing a complete text companion is supported and does
not require duplicating canonical facts. Unavailable tools or evidence are gaps,
not permission to claim successful verification.

## Verification

| Requirement | Minimum verification |
| --- | --- |
| `DOC-DERIVED-AUTH-001` | Compare displayed authority, state, simulation, and timing with source evidence |
| `DOC-DERIVED-PROV-001` | Resolve source identities and check snapshots, generation assumptions, and sharing limits |
| `DOC-A11Y-001` | Review text equivalence, non-color cues, keyboard operation, and applicable captions/descriptions |

## Agent handoff

An existing task result or review identifies activated requirements, source and
view versions, actual checks, gaps/exceptions, and compatibility effects. Report
whether output is source code, a rendered view, or a rendered video; do not call
an exported source bundle a tested video. A structural pass is not an accessibility
or semantic conformance certificate.

## Compatibility and migration

The first version is `0.1.0`, Development, with Advisory enforcement.
Explicit adoption brings in `documentation/technical-documentation` and its
upstream dependency. No renderer is installed and no old artifact is rewritten.

An explanation's format can change without changing the normative owner. Remove
or replace disposable views only with task authority; de-selection of a Spec
cannot revoke an already published artifact or repair an inaccessible video.
Release and consumer-default changes remain separate reviewed operations.

## References

- [Approved ESP-0014](../../proposals/0014_documentation-integrity-contracts.md)
- [Google accessible documentation](https://developers.google.com/style/accessibility)
- [W3C explanation of prerecorded captions](https://www.w3.org/WAI/WCAG21/Understanding/captions-prerecorded.html)

References provide background, not incorporation of an external standard. The
wording and limited scope are EngineeringSpecifications' proposal;
no Google, ASD, or W3C endorsement or certification is asserted.
