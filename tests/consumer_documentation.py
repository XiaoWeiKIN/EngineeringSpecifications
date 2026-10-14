"""Separate, explicit compatibility test against a pinned RF source checkout.

Not discovered by the dependency-free Spec check. The consumer CI invokes it
with --rf-root; missing consumer code is an error, not a skipped integration.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RF_ROOT: Path
REQUIRED = {"core/semantic-naming", "core/data-boundaries"}
TECHNICAL = "documentation/technical-documentation"
DERIVED = "documentation/derived-explanations"
DOC_IDS = {
    "DOC-STATE-001", "DOC-EVIDENCE-001", "DOC-PROC-001", "DOC-TERM-001",
    "DOC-FRESH-001", "DOC-DERIVED-AUTH-001", "DOC-DERIVED-PROV-001", "DOC-A11Y-001",
}


def run(*command: str, cwd: Path | None = None) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=90)
    if result.returncode:
        raise AssertionError(f"Command failed ({result.returncode}): {command!r}\n{result.stdout}\n{result.stderr}")
    return result.stdout


def inventory(root: Path) -> dict[str, str]:
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob("*") if p.is_file()}


class RFDocumentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(RF_ROOT / "scripts"))
        import explain_spec_activation
        cls.explainer = explain_spec_activation
        cls.router = explain_spec_activation.load_router()
        cls.ref = run("git", "rev-parse", "HEAD", cwd=ROOT).strip()

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()
        run("git", "init", "-b", "main", cwd=self.root)
        # Mere Markdown/HTML presence must not install the optional contracts.
        (self.root / "README.md").write_text("# Fixture project\n", encoding="utf-8")
        (self.root / "view.html").write_text("<!doctype html><title>Fixture</title>", encoding="utf-8")

    def bootstrap(self, selected: str | None) -> set[str]:
        args = [sys.executable, "-B", str(RF_ROOT / "scripts/foundryctl.py"),
                "--repo", str(self.root), "bootstrap", "--adapter", "portable",
                "--spec-repository", ROOT.as_uri(), "--spec-ref", self.ref, "--apply"]
        args.extend(["--spec", selected] if selected else ["--required-only"])
        run(*args)
        state = self.router.load_state(self.root)
        return {entry.key for entry in state.entries}

    def preview(self, paths, requirements=(), budget_bytes=32768):
        return self.explainer.build_preview(self.root, self.router, {
            "paths": list(paths), "requirements": list(requirements), "budget_bytes": budget_bytes})

    def test_required_only_does_not_adopt_documentation(self) -> None:
        self.assertEqual(self.bootstrap(None), REQUIRED)
        result = self.preview(["README.md"])
        self.assertTrue(all(not s["id"].startswith("documentation/") for s in result["specs"]))

    def test_technical_selection_document_scopes_and_external_dependencies(self) -> None:
        self.assertEqual(self.bootstrap(TECHNICAL), REQUIRED | {TECHNICAL})
        for path in ("README.md", "docs/intro.md", "guide.mdx"):
            with self.subTest(path=path):
                result = self.preview([path], ["DOC-TERM-001"])
                self.assertEqual({r["id"] for r in result["resolved"]}, {
                    "DOC-TERM-001", "SEM-NAME-001", "SEM-SURFACE-001"})
                self.assertNotIn(DERIVED, {s["id"] for s in result["specs"]})
        for path in ("src/main.go", "guide.rst", "manual.adoc", "view.html"):
            with self.subTest(path=path):
                unrelated = self.preview([path])
                self.assertNotIn(TECHNICAL, {s["id"] for s in unrelated["specs"]})

    def test_derived_selection_exact_capsule_read_only_and_budget(self) -> None:
        self.assertEqual(self.bootstrap(DERIVED), REQUIRED | {TECHNICAL, DERIVED})
        before = inventory(self.root)
        result = self.preview(["README.md", "assets/story.mjs"], sorted(DOC_IDS))
        state = self.router.load_state(self.root)
        resolved = self.router.requirement_dependency_closure(state.requirement_index, sorted(DOC_IDS))
        text, mode = self.router.compile_context_capsule(self.root, state, tuple(sorted(DOC_IDS)), resolved, (), (), 32768)
        self.assertEqual(result["capsule"]["text"], text)
        self.assertEqual(result["capsule"]["mode"], mode)
        self.assertEqual(result["capsule"]["sha256"], hashlib.sha256(text.encode("utf-8")).hexdigest())
        self.assertEqual(result["capsule"]["bytes"], len(text.encode("utf-8")))
        self.assertLessEqual(result["capsule"]["bytes"], 32768)
        self.assertFalse(result["receipt_created"])
        self.assertEqual(inventory(self.root), before)
        with self.assertRaisesRegex(self.router.RouterError, "ROUTER_CONTEXT_BUDGET_EXCEEDED"):
            self.preview(["README.md", "assets/story.mjs"], sorted(DOC_IDS), 100)
        self.assertEqual(inventory(self.root), before)

    def test_derived_producer_candidacy_and_source_drift(self) -> None:
        self.bootstrap(DERIVED)
        result = self.preview(["assets/story.mjs"], ["DOC-DERIVED-PROV-001"])
        self.assertEqual({r["id"] for r in result["resolved"]}, {
            "DOC-DERIVED-PROV-001", "DOC-DERIVED-AUTH-001", "DOC-FRESH-001",
            "DOC-STATE-001", "DOC-EVIDENCE-001"})
        # Broad candidacy alone never records semantic applicability/activation.
        empty = self.preview(["src/unrelated.go"])
        self.assertIsNone(empty["capsule"])
        self.assertFalse(empty["receipt_created"])
        path = self.root / "docs/agent-guides/managed/documentation/derived-explanations.md"
        path.write_bytes(path.read_bytes()+b"\nunreviewed drift\n")
        with self.assertRaisesRegex(self.router.RouterError, "DRIFT"):
            self.preview(["assets/story.mjs"], ["DOC-DERIVED-PROV-001"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rf-root", type=Path, required=True)
    args = parser.parse_args()
    RF_ROOT = args.rf_root.resolve(strict=True)
    if not (RF_ROOT / "scripts/explain_spec_activation.py").is_file():
        parser.error("The specified RF checkout does not contain Spec Lab")
    unittest.main(argv=[sys.argv[0]], verbosity=2)
