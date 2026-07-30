# Contributing

EngineeringSpecifications contains reusable normative guidance. Changes should
be reviewable as specification changes, not hidden inside consumer tooling.

## Change process

1. Explain the engineering problem and affected specification IDs.
2. Edit or add Markdown under `specification/`.
3. Keep each rule testable, scoped, and independent of one private repository.
4. Update `catalog.json`:
   - preserve stable IDs;
   - bump the affected specification version for normative changes;
   - refresh the source SHA-256;
   - declare dependencies and deterministic detection evidence.
5. Update `CHANGELOG.md` for externally observable changes.
6. Run the canonical check:

```bash
python3 -B scripts/check.py
```

## Compatibility

- Patch versions clarify wording without changing required behavior.
- Minor versions add backward-compatible guidance or supported categories.
- Major versions change or remove an existing normative contract.
- Moving files without changing normative content does not require a
  specification version bump, but Catalog paths and digests must remain valid.

Consumers lock an immutable Git commit, so merging a change does not update a
project until it runs an explicit EngineeringWorkflow update.

## Project-specific rules

Do not add a rule that only describes one repository's architecture or naming.
Keep those rules in the project and register them through its
`docs/.engineering/specs.json` `project_specs` entries.

