# Specification authoring

This is non-normative guidance for authors and reviewers of this repository's
Specifications. It is not a Catalog Specification, a consumer dependency, or
an additional approval step. It works offline and requires no installed Skill.
The [contribution process](../CONTRIBUTING.md), existing contracts, and
[formal template](../specification/0000-template.md) remain controlling.

## Start with the reader's decision

Identify the implementation or review decision the reader needs to make, and
the vocabulary the reader already has. Explain when the rule applies before
presenting its obligations. Keep exclusions near the affected behavior; do not
make a conditional rule look universal by moving its condition to an example.

A useful review question is: who does what, under which conditions, with which
exceptions, and what observation would distinguish compliance from failure?
Use an explicit subject when another component, call, or value could be the
antecedent of "it". Keep connected reasoning in paragraphs; splitting every
clause into a bullet can obscure the relation between a condition and a duty.
Leave wording alone when it already answers those questions.

## Preserve the contract before improving the wording

Compare the old and new text against the same source revision. Preserve
negation, quantifiers such as "each" and "exactly once", ordering, units,
conditions, exception scope, and requirement strength. Do not replace `MUST`,
`SHOULD`, or `MAY` to match an editorial preference. Keep proposed, current,
verified, unverified, and historical claims distinct.

Stable Requirement IDs, headings, Activation, Context dependencies, Automated
enforcement, enforcement classes, and Verification mappings are part of the
review. A shorter sentence does not justify changing them. Keep the existing
metadata order and budgets from the formal template; this guide adds no word
count, preferred-word dictionary, or linguistic lint gate.

Reuse owning technical terms and exact identifiers. Do not rename an external
API, field, command, state, or protocol value for stylistic consistency. A new
term should identify a real distinction, not merely vary the prose.

If the new wording changes which implementations comply, classify that change
as normative under CONTRIBUTING. Do not hide a new duty, a narrower exception,
or a larger test matrix inside a supposedly editorial patch. If equivalence
cannot be established, leave the disputed text unchanged and record the gap.

## Keep requirements, reasons, and examples separate

Put the obligation in its Requirement block. Use Rationale to explain the
failure the rule prevents, without introducing a second hidden obligation.
Examples illustrate a permitted realization; they do not make that language,
framework, type shape, or testing tool mandatory. Keep alternatives and
protocol-owned exceptions visible.

Label pseudocode and omitted context. When presenting a runnable example,
include its imports, fixture assumptions, and how its checks are executed.
Keep synthetic values and hypothetical outcomes distinguishable from measured
results. Do not invent a repository command or claim execution based only on
reading a snippet. Check the owning tool contract before describing command
effects, prerequisites, failure handling, or approval consequences.

A no-effects test should call the boundary entry point that can produce the
effect. A parser-only call followed by assertions about unused spies can pass
without checking the integration. A valid-input positive control shows that
the same entry point reaches the observer. A deliberately broken variant can
check that the assertion fails for the intended defect. Record the limits:
passing a fixture does not establish conformance of a consuming project.

For diagrams, explain the relationship or outcome in text as well. A picture
must not become a second requirement owner. Preserve source references and
state; distinguish animated or synthetic timing from a measured execution.

## Review a bounded change

Use the existing PR discussion or a focused review note to record the source
revision, affected IDs, old meaning, new wording or example, conformance
impact, and supporting checks. Do not create a new approval artifact solely
for prose. Review complete Requirement blocks and their dependencies, not just
a diff line isolated from its condition.

Run `python3 -B scripts/check.py` from the repository root. It checks structure,
digests, dependencies, links, and tests. It does not prove semantic equivalence
or reader understanding. Record automated results separately from the
wording-review judgment and report checks that were not run.

Use the existing patch-version policy for clarifications that preserve required
behavior, refresh changed source digests, and put new changes under Unreleased.
Do not edit past release notes, retarget a release tag, rewrite accepted
history, or update consuming project locks as a side effect of an editorial
change. [RELEASING.md](../RELEASING.md) governs later publication.

Do not add `documentation/*` to another Specification's `requires` merely to
improve its author's prose. Those dependencies govern consumer tasks; local
authoring guidance belongs here. Project style conventions and the reader's
language remain valid; English grammar or capitalization advice does not
become a Chinese-language rule.

## Background, not incorporated requirements

This guide uses independently worded review advice informed by the following
primary references and this repository's own integrity contracts. Links are
optional background, not instructions to fetch external pages for every task.
It does not reproduce the ASD-STE100 dictionary or claim full ASD-STE100 or
Google-style conformance, certification, or endorsement.

- [Google: unambiguous pronouns](https://developers.google.com/style/pronouns)
- [Google: procedures](https://developers.google.com/style/procedures)
- [Google: code samples](https://developers.google.com/style/code-samples)
- [ASD-STE100: scope and technical vocabulary](https://www.asd-ste100.org/about.html)
- [Specification principles](specification-principles.md)
