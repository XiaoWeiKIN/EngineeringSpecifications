# Specification Principles

EngineeringSpecifications publishes rules only when they can guide more than
one repository and survive independent versioning. These principles form the
review rubric for adding or changing a specification.

## Start from observable engineering value

A specification change identifies the failure, inconsistency, compatibility
risk, or repeated review cost it addresses. It explains who benefits and how a
reviewer can observe the improvement.

New behavior should include implementation examples, tests, prototypes, or
repository evidence. Cross-language rules should show that their concepts
survive materially different language models. Reviewers may request additional
prototypes when one ecosystem cannot expose the important trade-offs.

## Specify behavior at the broadest valid layer

Rules describe observable contracts and invariants. They avoid prescribing one
implementation unless interoperability, safety, or verification requires it.

A shared requirement belongs in the broadest layer where it remains true.
Language, framework, database, testing, and protocol specifications add their
own constraints through explicit dependencies.

## Protect consumers from surprise

Stable specifications preserve their observable contract. Changes explain
compatibility effects, migration paths, failure behavior, and rollback
conditions.

Development specifications may evolve, but they still record changes and avoid
needless churn. Deprecation identifies a replacement or an explicit removal
plan.

## Reuse concepts before inventing synonyms

Specifications use the same semantic verbs, units, statuses, error concepts,
and boundary terminology when they describe the same behavior.

A narrower specification should reference an upstream requirement instead of
restating it. A new term must identify a real semantic distinction.

## Keep the contract smaller than the implementation space

Every requirement consumes long-term compatibility budget. Authors keep the
normative surface small, place rationale and examples in clearly
non-normative sections, and leave idiomatic implementation choices to the
owning ecosystem.

Significant proposals stay focused. If one part delivers independent value, it
can move through review as a separate Proposal.

## Make important rules verifiable

Each load-bearing requirement states how a project can demonstrate compliance:

- schema, type, or static-analysis evidence;
- focused unit, integration, or contract tests;
- deterministic structural checks;
- documented human review where mechanical verification is impractical.

A rule without a plausible verification path remains guidance until its
expected evidence is clear.

## Keep project decisions in the project

Repository architecture, private framework choices, internal paths, domain
vocabulary, and component patterns remain project-owned. A rule becomes a
central specification candidate after multiple repositories can adopt it
without importing the original project's architecture.
