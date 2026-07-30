# EngineeringSpecifications Repository Guide

## Purpose

This repository is the source of truth for versioned engineering
specifications consumed by EngineeringWorkflow.

## Read First

- Read `README.md` for the repository contract.
- Read `docs/specification-model.md` before adding a new category or dependency.
- Read `governance/README.md` before changing normative behavior, maturity, or
  the Catalog contract.
- Read `proposals/README.md` when a change is cross-cutting or significant.
- Read `catalog.json` before adding or moving a specification.
- Start a new normative document from `specification/0000-template.md`.
- Read the relevant file under `specification/` before changing its rules.

## Change Rules

- Keep normative guidance in `specification/`; do not place workflow code here.
- Give every specification a stable lowercase slash-separated ID.
- Bump a specification version when its normative content changes.
- Update its SHA-256 in `catalog.json` after editing the Markdown source.
- Keep dependencies acyclic and reference only cataloged specification IDs.
- Put shared rules in the broadest layer where they remain true; narrower
  specifications depend on them instead of copying them.
- Reserve `core/` for rules required by every implementation repository.
- Treat language, framework, database, testing, and protocol as independent
  composition dimensions.
- Use BCP 14 keywords for explicit requirement strength and keep rationale
  clearly non-normative.
- Give load-bearing requirements stable IDs and connect them to enforcement and
  expected implementation evidence.
- Significant cross-cutting or public-contract changes require an approved ESP
  before normative integration.
- Treat specifications without an explicit maturity marker as Development.
- Keep detection rules deterministic and based on filenames or extensions.
- Do not add project-specific rules unless they are intentionally reusable
  across repositories.

## Validation

Run the canonical check before completion:

```bash
python3 -B scripts/check.py
```

The check validates the catalog schema, paths, digests, dependency graph,
Markdown links, and unit tests.
