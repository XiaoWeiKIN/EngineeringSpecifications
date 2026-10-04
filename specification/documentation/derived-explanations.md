# Derived Explanation Integrity

> **Status:** Development
>
> **Catalog ID:** `documentation/derived-explanations`
>
> **Selection:** Explicit
>
> **Routing:** Selection installs this Specification. Load it only when a task
> generates or reviews a diagram, interactive view, presentation, simulation,
> video, or other derived surface that communicates engineering facts.
>
> **Catalog metadata:** `catalog.json` is the source of truth for version,
> dependencies, file scopes, detection evidence, activation summary, and
> content digest.

## Purpose

Diagrams, interactive pages, presentations, simulations, and videos can make
engineering systems easier to understand. They can also hide their source,
outlive the revision they explain, or appear more authoritative than the
underlying decision and evidence.

This Specification governs the authority, provenance, and equivalent
information contract of derived explanation surfaces. It does not prescribe a
renderer, visual style, animation framework, frame rate, presentation
template, or media format.

## Applicability

### Load this specification when

- generating or reviewing a diagram, architecture map, dependency graph,
  interactive explainer, presentation, simulation, or video from engineering
  source material;
- transforming ADR, Research, Benchmark, Design, ExecPlan, Spec, source code,
  test, or runtime evidence into a reader-oriented derived view;
- embedding exact source excerpts or generated summaries inside an explanation
  bundle;
- publishing an explanation whose source may change independently of the
  generated output;
- using color, motion, pointer interaction, or audio to communicate engineering
  state or relationships.

### Do not apply this specification when

- editing the canonical source artifact itself rather than a derived
  explanation;
- creating decorative media that carries no unique engineering information;
- rendering a byte-preserving view whose authority and freshness are already
  defined by the owning source and no additional interpretation is introduced.

A derived surface may embed canonical source bytes. That embedding does not
make the surrounding bundle an independent canonical owner.

## Agent workflow

When this Specification is activated, the implementing or reviewing agent:

1. identifies the canonical source artifacts and the source identity that the
   output explains;
2. records that the output is derived and preserves the authority boundary of
   requirements, decisions, approvals, and verification evidence;
3. records source revision, snapshot, or digest information sufficient to
   detect stale output;
4. labels simulations, projections, or hypothetical sequences so they are not
   reported as observed implementation behavior;
5. checks that unique engineering information has an equivalent representation
   that does not depend only on color, pointer interaction, motion, or audio;
6. reports source identity, freshness limits, and accessibility-equivalent
   information in the handoff.

## Terminology

- A **canonical source** is the artifact that owns the requirement, decision,
  evidence, or current fact being explained.
- A **derived explanation** is a representation created from one or more
  canonical sources for reader understanding. It does not gain source
  authority through presentation quality.
- **Source identity** is the artifact identity plus revision, snapshot, digest,
  or equivalent version boundary needed to determine what source bytes or
  state the derived explanation represents.
- An **equivalent representation** communicates the same unique engineering
  information without requiring the sensory or interaction channel used by the
  primary presentation.
- A **simulation** computes or illustrates possible behavior from assumptions;
  it is not an observation of the implementation unless independent evidence
  establishes that fact.

## Requirements

### DOC-DERIVED-AUTH-001 — Derived explanations preserve source authority

**Activation:** Load when a generated or manually derived view restates requirements, decisions, approvals, implementation state, or verification results.

**Context dependencies:** `DOC-STATE-001`, `DOC-EVIDENCE-001`

**Automated enforcement:** Advisory

A derived explanation **MUST** preserve the authority and engineering state of
its canonical sources. It **MUST NOT** become the authoritative source for a
requirement, decision, approval, implementation state, or verification result
solely because it is easier to consume.

When a reader could reasonably mistake the output for a canonical artifact,
the derived explanation **MUST** identify itself as derived and identify the
owning source.

A simulation, projection, hypothetical sequence, or synthetic fixture **MUST**
be identified as such and **MUST NOT** be reported as observed implementation
behavior without independent evidence.

**Rationale (non-normative):** Rich presentation can create false confidence.
An explicit authority boundary lets teams generate disposable interfaces
without creating a second manually maintained source of truth.

**Enforcement (review):** Review labels and claims against the canonical source
and its lifecycle state. Structural metadata may identify a derived bundle but
cannot prove that every visual claim preserves source meaning.

**Evidence:** A reviewed mapping from the derived claims to canonical source
artifacts, including any simulation or synthetic-data labels.

### DOC-DERIVED-PROV-001 — Derived engineering claims carry source identity

**Activation:** Load when a derived explanation can outlive, be shared separately from, or be regenerated independently of its canonical source.

**Context dependencies:** `DOC-DERIVED-AUTH-001`, `DOC-FRESH-001`

**Automated enforcement:** Advisory

A derived explanation that makes engineering claims **MUST** identify its
canonical source artifacts and source identity with enough precision to
determine which revision, snapshot, or digest the output represents.

When the source identity cannot be established, the output **MUST** state that
its freshness cannot be verified and **MUST NOT** claim to represent the
current implementation or current decision state.

After a canonical source changes in a way that can affect the explanation, the
derived output **MUST** be regenerated or explicitly revalidated before it is
presented as current.

A digest **MAY** demonstrate byte consistency. A digest alone **MUST NOT** be
described as proof of authenticity, semantic correctness, approval, or current
applicability.

**Rationale (non-normative):** Derived output is intentionally disposable.
Source identity makes staleness detectable without requiring the generated
surface to become a governed source itself.

**Enforcement (hybrid):** Generated bundles may verify source IDs, revisions,
and digests mechanically. Review confirms that the declared sources actually
own the explained claims.

**Evidence:** Source-artifact identifiers plus revision, snapshot, digest, or
equivalent version metadata and a regeneration or revalidation record when
sources changed.

### DOC-A11Y-001 — Unique engineering information has an equivalent representation

**Activation:** Load when color, pointer interaction, motion, visual layout, or audio carries engineering information that is not already available elsewhere.

**Context dependencies:** `DOC-DERIVED-AUTH-001`

**Automated enforcement:** Advisory

Critical engineering state, severity, ownership, dependency, or verification
status **MUST NOT** be communicated only through color.

When a diagram or visual layout carries unique engineering relationships, the
derived explanation **MUST** provide an equivalent representation, such as
structured text, a relationship list, or another inspectable form.

When an interactive view carries unique engineering information, the output
**MUST** provide a non-pointer path to that information appropriate to the
medium, such as keyboard-operable controls or an equivalent structured text
view.

When video or audio carries unique engineering information, the output
**MUST** provide an equivalent text form appropriate to the content, such as
captions, a transcript, or a synchronized textual description.

The presence of an automated accessibility check **MAY** provide evidence for
mechanical properties. It **MUST NOT** by itself be described as proof that the
explanation is understandable or fully accessible.

**Rationale (non-normative):** Engineering facts must remain reviewable when a
reader cannot perceive or operate the primary presentation channel. Equivalent
representations also improve machine inspection and long-term portability.

**Enforcement (hybrid):** Structural checks may inspect labels, keyboard
controls, transcripts, captions, or text equivalents. Human review confirms
that the equivalent form carries the same unique engineering information.

**Evidence:** The equivalent text or interaction path plus any structural
accessibility check and a review of the engineering information it preserves.

## Approved patterns

The following examples are non-normative. Artifact IDs and abbreviated
revisions are placeholders, not evidence for a real project.

A generated diagram bundle can record:

```text
Derived explanation: yes
Canonical source: ADR-061
Source revision: abc123
Authority: none
Relationships: A requires B; B owns state C
```

An interactive benchmark explorer can expose the same parameter values and
result table in structured text rather than requiring pointer interaction.

A video can pair narration and animation with captions or a transcript that
preserves the engineering claims and source references.

## Rejected patterns

- Treating a generated architecture diagram as the only owner of a requirement
  violates `DOC-DERIVED-AUTH-001`.
- Labeling synthetic timing animation as measured runtime violates
  `DOC-DERIVED-AUTH-001`.
- Publishing a derived view as "current" without a source revision or explicit
  freshness limitation violates `DOC-DERIVED-PROV-001`.
- Using green and red as the only representation of verification status
  violates `DOC-A11Y-001`.
- Requiring a mouse hover to discover the only copy of a failure condition
  violates `DOC-A11Y-001`.
- Publishing unique engineering claims only in narration without captions,
  transcript, or equivalent text violates `DOC-A11Y-001`.

## Exceptions

Decorative media with no unique engineering information needs no equivalent
engineering representation under this Specification.

A byte-preserving rendering of a canonical artifact may rely on the canonical
artifact's identity when the renderer adds no claims or interpretation. The
rendering still does not gain independent authority.

Project-specific visual branding, renderer choice, hosting model, and
organization accessibility targets remain project-owned.

## Verification

| Requirement | Minimum verification |
| --- | --- |
| `DOC-DERIVED-AUTH-001` | Review source ownership, derived labeling, and simulation/synthetic boundaries |
| `DOC-DERIVED-PROV-001` | Verify source artifact identity and revision/snapshot/digest freshness boundary |
| `DOC-A11Y-001` | Review non-color state and equivalent text or interaction path for unique information |

## Agent handoff

An agent applying this Specification reports:

```text
Activated requirements: <DOC-DERIVED-* / DOC-A11Y-* IDs>
Canonical sources: <artifact IDs or paths>
Source identity: <revision / snapshot / digests, or unverifiable>
Derived authority: none
Embedded source attribution: none | <owning source and its unchanged authority>
Simulation or synthetic data: none | <assumptions and label>
Equivalent representation: <text, relationship list, keyboard path, captions, transcript>
Freshness: current at <source identity> | stale | unknown
```

## Compatibility and migration

Version `0.1.1` clarifies prose, example boundaries, and reference authority.
It preserves Requirement IDs, obligations, activation metadata, context
dependencies, automated enforcement levels, and Verification mappings.
No consumer behavior migration is introduced by this editorial patch.

Version `0.1.0` introduces the first Development contract for reusable derived
explanation surfaces. It does not require any renderer or media format and does
not convert existing diagrams, presentations, or videos into governed
canonical artifacts.

Consumers adopting this version should add source identity and equivalent
information when they regenerate or materially revise a derived explanation.
Existing outputs do not become current merely because the Specification is
selected.

## References

References provide provenance and explanation. They do not add undeclared
normative obligations or require adoption of an external style guide.

- [ESP-0014: Reusable documentation integrity contracts](../../proposals/0014_documentation-integrity-contracts.md)
- [Technical Documentation Integrity](technical-documentation.md)
- [Google Developer Documentation Style Guide: Accessibility](https://developers.google.com/style/accessibility)
- [Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/standards-guidelines/wcag/)
