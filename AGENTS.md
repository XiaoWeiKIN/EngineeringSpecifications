# EngineeringSpecifications Repository Guide

## Purpose

This repository is the source of truth for versioned engineering
specifications consumed by EngineeringWorkflow.

## Read First

- Read `README.md` for the repository contract.
- Read `catalog.json` before adding or moving a specification.
- Read the relevant file under `specification/` before changing its rules.

## Change Rules

- Keep normative guidance in `specification/`; do not place workflow code here.
- Give every specification a stable lowercase slash-separated ID.
- Bump a specification version when its normative content changes.
- Update its SHA-256 in `catalog.json` after editing the Markdown source.
- Keep dependencies acyclic and reference only cataloged specification IDs.
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

