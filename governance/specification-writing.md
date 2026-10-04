# Writing and reviewing Specifications

This is non-normative guidance for authors and reviewers of this repository.
It is not a Catalog Specification, a consumer dependency, or an approval gate.
It does not require RepoFoundry to be installed. The existing contribution,
lifecycle, release, and Specification contracts remain controlling.

## Write for the implementation or review decision

Start by identifying what the reader needs to decide: whether a rule applies,
what behavior is required, which alternatives remain valid, and what evidence
would demonstrate compliance. Explain unfamiliar domain terms without replacing
established technical vocabulary. English and Chinese explanatory documents
should preserve the same decisions and evidence, not mechanically share English
sentence lengths or capitalization rules.

Use connected paragraphs for mechanisms and trade-offs. Prefer a named actor
when a pronoun could refer to several components. Keep a condition near the
obligation it limits, and preserve negation, quantifiers, units, exceptions,
and requirement strength. A shorter sentence is not an improvement if it loses
one of those facts. No fixed word limit or approved-word dictionary applies.

## Keep a Requirement independently interpretable

Use the [formal template](../specification/0000-template.md) for the exact
metadata shape and budgets. Preserve the stable ID, heading, Activation,
Context dependencies, Automated enforcement, and Verification mapping when the
change is editorial. Do not split or merge IDs merely to shorten a paragraph.

Ask who performs the action, which input or state triggers it, what outcome is
observable, and which alternatives or exceptions the source permits. Keep
rationale separate from obligations. Do not hide a new requirement in an
example, evidence field, or review instruction.

BCP 14 strength, document maturity, automated enforcement, installation
selection, and task activation answer different questions. In particular,
Advisory does not weaken a normative MUST; detection does not authorize optional
installation; and a Development marker is not a Catalog version.

## Make examples demonstrate the claimed boundary

Label code as runnable, a fragment with named prerequisites, or pseudocode.
Name omitted packages, imports, and harness functions when readers need them.
Mark synthetic data, abbreviated revisions, and placeholder commands so they
cannot be mistaken for verified project evidence. Alternative implementations
should not look like declarations to paste into one compilation unit.

A rejection example that claims no downstream effects should call the entry
point that can reach those effects. Calling only a parser and inspecting unused
spies is insufficient. A valid-input control can show that the spies are wired
in; a deliberately broken implementation can show that the same assertions
actually detect the prohibited behavior. These are authoring techniques, not a
new mandatory test strategy for every consumer.

An illustrative implementation is not proof of conformance by another project.
Do not describe an example, syntax check, digest check, or model-generated review
as measured production behavior or completed verification.

## Preserve readable and traceable explanations

Use descriptive headings and meaningful link labels, but preserve required
headings and existing public anchors. Prefer ordered steps for procedures.
Explain prerequisites, placeholders, material effects, and stop conditions;
distinguish preparing a release from publishing its immutable identity.

Mermaid is useful for relationships and failure paths. Keep a text explanation
of what the diagram establishes. For richer views, identify the owning source
and provide equivalent access to unique information. Captions that repeat only
audio do not describe engineering facts shown only visually.

External references provide provenance, not undeclared obligations. Keep this
repository's contracts understandable offline; do not replace a Requirement
with an instruction to fetch a changing web page. Do not copy Google or STE
text into each language Specification or add documentation dependencies merely
to improve the prose used to author it.

## Review the change against a fixed baseline

Compare the old and new text before classifying the change. Record the actor,
condition, obligation, exception, and verification meaning for any changed
Requirement. Check nearby examples and translations for the same meaning.
If the wording supports more than one technical interpretation, report that
question for normative review rather than silently choosing one.

Use the [contribution process](../CONTRIBUTING.md) for versioning and digests.
Editorial Spec revisions use patch versions. A change in required behavior or
consumer-visible metadata needs its own compatibility assessment. Preserve
dated release entries, approved proposal history, raw evidence, and sealed
research snapshots; document an erratum instead of rewriting them for style.

Run `python3 -B scripts/check.py` from the repository root and inspect the diff.
For Go example changes, an additional offline check is available as
`python3 -B tests/check_go_examples.py` when a local Go toolchain is installed.
It compiles the exact fragments with their documented imports and exercises
representative cases; the canonical standard-library check does not require Go.
The checks verify structure, references, digests, and examples. They do not prove
semantic equivalence, accessibility, or a reader-comprehension improvement.

## Sources and attribution

This guide combines repository-specific review techniques with selected clarity
and reader-task ideas from the following sources. It is not a reproduction or
certification of either external standard.

- [Google developer documentation style guide](https://developers.google.com/style)
- [Google procedure guidance](https://developers.google.com/style/procedures)
- [Google accessible-documentation guidance](https://developers.google.com/style/accessibility)
- [ASD-STE100 overview](https://www.asd-ste100.org/about_STE.html)

The cited Google guidance is by Google and uses
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The selected ideas are
adapted here for Specification authors; no endorsement is implied. The STE
standard and dictionary are not reproduced, and no full STE conformance is
claimed. Reference retrieval is optional for maintainers, not a task-time
network dependency.
