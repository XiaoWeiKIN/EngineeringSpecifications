"""Validate actual documentation contracts, not natural-language conformance."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "proposals/0014_documentation-integrity-contracts.md"
REQ = re.compile(r"^### ([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+-[0-9]{3}) — .+$", re.M)
EXPECTED = {
    "DOC-STATE-001", "DOC-EVIDENCE-001", "DOC-PROC-001", "DOC-TERM-001",
    "DOC-FRESH-001", "DOC-DERIVED-AUTH-001", "DOC-DERIVED-PROV-001", "DOC-A11Y-001",
}


def entries() -> list[dict]:
    return [e for e in json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))["specs"] if e["id"].startswith("documentation/")]


def content(entry: dict) -> str:
    return (ROOT / entry["path"]).read_text(encoding="utf-8")


def blocks(text: str) -> list[tuple[str, str]]:
    section = text.split("\n## Requirements\n", 1)[1].split("\n## ", 1)[0]
    matches = list(REQ.finditer(section))
    return [(m.group(1), section[m.start():matches[i+1].start() if i+1 < len(matches) else len(section)])
            for i, m in enumerate(matches)]


class DocumentationShapeTests(unittest.TestCase):
    """Portable shape/rubric checks; no inference about natural-language truth."""

    def test_documentation_plan_is_explicit_and_schema1_shaped(self) -> None:
        plan = entries()
        self.assertEqual([e["id"] for e in plan], [
            "documentation/technical-documentation", "documentation/derived-explanations"])
        for entry in plan:
            self.assertEqual(set(entry), {"id", "version", "path", "sha256", "required",
                                         "requires", "applies_to", "description"})
            self.assertFalse(entry["required"])
            self.assertEqual(entry["version"], "0.1.0")
            self.assertTrue(entry["description"].startswith("Load when "))
            self.assertLessEqual(len(entry["description"]), 180)
        self.assertEqual(plan[0]["requires"], ["core/semantic-naming"])
        self.assertEqual(plan[1]["requires"], [plan[0]["id"]])
        self.assertEqual(plan[0]["applies_to"], ["**/*.md", "**/*.mdx"])
        self.assertEqual(plan[1]["applies_to"], ["**/*"])

    def test_documentation_digests_and_document_identity_match(self) -> None:
        for entry in entries():
            with self.subTest(spec=entry["id"]):
                raw = (ROOT / entry["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"])
                text = raw.decode("utf-8")
                self.assertIn(f'> **Catalog ID:** `{entry["id"]}`', text)
                self.assertIn("> **Selection:** Explicit", text)
                self.assertNotIn("Proposal fixture", text)

    def test_documentation_has_eight_bounded_advisory_blocks_and_verification(self) -> None:
        seen = set()
        for entry in entries():
            text = content(entry)
            rows = re.findall(r"^\| `([^`]+)` \| .+ \|$", text.split("\n## Verification\n", 1)[1], re.M)
            local = blocks(text)
            self.assertEqual(sorted(rows), sorted(rid for rid, _ in local))
            for rid, block in local:
                self.assertNotIn(rid, seen)
                seen.add(rid)
                self.assertLessEqual(len(block.encode("utf-8")), 8192)
                self.assertRegex(block, r"\A### .+\n\n\*\*Activation:\*\* Load when [^\n]+\n\n\*\*Context dependencies:\*\* [^\n]+\n\n\*\*Automated enforcement:\*\* Advisory\n\n")
                activation = block.split("**Activation:** ", 1)[1].split("\n", 1)[0]
                self.assertLessEqual(len(activation), 180)
                for marker in ("**Rationale (non-normative):**", "**Evidence:**"):
                    self.assertEqual(block.count(marker), 1)
                self.assertEqual(len(re.findall(r"\*\*Enforcement \((?:review|hybrid|mechanical)\):\*\*", block)), 1)
        self.assertEqual(seen, EXPECTED)

    def test_documentation_exact_dependencies_are_closed_and_acyclic(self) -> None:
        graph = {rid: re.findall(r"`([^`]+)`", block.split("**Context dependencies:** ", 1)[1].split("\n", 1)[0])
                 for entry in entries() for rid, block in blocks(content(entry))}
        upstream = {"SEM-NAME-001", "SEM-SURFACE-001"}
        for rid, deps in graph.items():
            self.assertEqual(len(deps), len(set(deps)))
            self.assertNotIn(rid, deps)
            self.assertLessEqual(set(deps), EXPECTED | upstream)
        remaining = {rid: set(deps) - upstream for rid, deps in graph.items()}
        while remaining:
            ready = {rid for rid, deps in remaining.items() if not deps}
            self.assertTrue(ready, "Requirement cycle")
            remaining = {rid: deps-ready for rid, deps in remaining.items() if rid not in ready}
        self.assertEqual(set(graph["DOC-TERM-001"]), upstream)

    def test_documentation_integration_links_recorded_approval(self) -> None:
        text = PROPOSAL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# ESP-0014:"))
        self.assertIn("**Status:** Approved", text)
        self.assertIn("**Normative:** No", text)
        for entry in entries():
            self.assertIn("../../proposals/0014_documentation-integrity-contracts.md", content(entry))


class CanonicalDocumentationTests(unittest.TestCase):
    """Use the actual repository validator on a temporary Catalog, without RF."""

    @classmethod
    def setUpClass(cls) -> None:
        spec = importlib.util.spec_from_file_location("documentation_compatibility_check", ROOT / "scripts/check.py")
        assert spec is not None and spec.loader is not None
        cls.check = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.check)

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.original_catalog = (ROOT / "catalog.json").read_bytes()
        self.catalog = json.loads(self.original_catalog)
        self.production_files = {}
        for entry in self.catalog["specs"]:
            source = ROOT / entry["path"]
            self.production_files[source] = source.read_bytes()
            destination = self.root / entry["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        self.save_catalog()

    def tearDown(self) -> None:
        self.assertEqual((ROOT / "catalog.json").read_bytes(), self.original_catalog)
        for path, raw in self.production_files.items():
            self.assertEqual(path.read_bytes(), raw)

    def save_catalog(self) -> None:
        (self.root / "catalog.json").write_text(json.dumps(self.catalog, indent=2)+"\n", encoding="utf-8")

    def mutate(self, old: str, new: str) -> None:
        entry = self.catalog["specs"][-2]
        path = self.root / entry["path"]
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        entry["sha256"] = self.check.digest_file(path)
        self.save_catalog()

    def validate(self):
        return self.check.check_requirement_ids(self.root, self.check.load_catalog(self.root))

    def test_canonical_uses_real_catalog_and_requirement_checks(self) -> None:
        baseline = self.check.check_requirement_ids(ROOT, self.check.load_catalog(ROOT))
        self.assertEqual(set(self.validate()), set(baseline))
        self.assertLessEqual(EXPECTED, set(baseline))
        # Exact root/nested file matching belongs to the RF consumer's separate
        # integration test. This test validates scopes as Catalog strings only.

    def test_canonical_source_drift_fails_closed(self) -> None:
        entry = self.catalog["specs"][-2]
        path = self.root / entry["path"]
        path.write_bytes(path.read_bytes()+b"\ndrift\n")
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            self.validate()

    def test_canonical_missing_verification_fails_closed(self) -> None:
        self.mutate("| `DOC-STATE-001` | Compare edited claims with source lifecycle and requirement state |\n", "")
        with self.assertRaisesRegex(ValueError, "Verification coverage mismatch"):
            self.validate()

    def test_canonical_context_cycle_fails_closed(self) -> None:
        self.mutate("**Context dependencies:** None", "**Context dependencies:** `DOC-FRESH-001`")
        with self.assertRaisesRegex(ValueError, "Requirement context dependency cycle"):
            self.validate()

    def test_canonical_undeclared_catalog_dependency_fails_closed(self) -> None:
        self.catalog["specs"][-1]["requires"] = []
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, "outside its Catalog dependency closure"):
            self.validate()

    def test_canonical_oversized_activation_and_block_fail_closed(self) -> None:
        original = content(entries()[0])
        for old, new, error in [
            ("Load when editing text that describes current, proposed, accepted, planned, implemented, verified, unverified, or historical behavior.", "Load when "+"x"*181, "Activation exceeds"),
            ("An engineering document **MUST** preserve", "x"*8192+"\nAn engineering document **MUST** preserve", "maximum is 8192")]:
            with self.subTest(error=error):
                path = self.root / self.catalog["specs"][-2]["path"]
                path.write_text(original, encoding="utf-8")
                self.mutate(old, new)
                with self.assertRaisesRegex(ValueError, error):
                    self.validate()


if __name__ == "__main__":
    unittest.main()
