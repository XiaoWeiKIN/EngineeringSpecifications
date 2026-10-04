"""Protect the reviewed delta; do not classify arbitrary prose as compliant."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLLOWUP = json.loads(
    (ROOT / "tests/fixtures/spec-editorial-followup.json").read_text(encoding="utf-8")
)
GO = "specification/languages/go.md"
DERIVED = "specification/documentation/derived-explanations.md"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def restore(relative: str, text: str) -> str:
    for edit in reversed(FOLLOWUP["edits"][relative]["replacements"]):
        if text.count(edit["after"]) != 1:
            raise AssertionError("Missing or duplicated reviewed replacement")
        text = text.replace(edit["after"], edit["before"])
    if digest(text) != FOLLOWUP["edits"][relative]["before_sha256"]:
        raise AssertionError("Unreviewed content change")
    return text


def section(text: str, title: str) -> str:
    heading = f"## {title}\n"
    if text.count(heading) != 1:
        raise AssertionError("Missing or duplicated section")
    return text.split(heading, 1)[1].split("\n## ", 1)[0]


def go_example(text: str) -> str:
    examples = re.findall(
        r"^```go\n(.*?)^```$", section(text, "Approved patterns"), re.M | re.S
    )
    if len(examples) != 1:
        raise AssertionError("Expected one Go example")
    return examples[0]


class FollowupEditorialTests(unittest.TestCase):
    def test_followup_scope_and_baseline_are_explicit(self) -> None:
        self.assertEqual(FOLLOWUP["baseline_revision"], "4a0268f0895106ab19b86a243d38ad43d86bc328")
        self.assertEqual(FOLLOWUP["catalog_version"], "1.7.1")
        self.assertEqual(set(FOLLOWUP["edits"]), {GO, DERIVED})
        self.assertEqual(FOLLOWUP["edits"][GO]["version"], "0.5.1")
        self.assertEqual(FOLLOWUP["edits"][DERIVED]["version"], "0.1.1")

    def test_exact_replacements_restore_original_source_hashes(self) -> None:
        for relative, data in FOLLOWUP["edits"].items():
            with self.subTest(path=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                self.assertEqual(digest(text), data["sha256"])
                self.assertEqual(digest(restore(relative, text)), data["before_sha256"])

    def test_requirements_except_named_subject_and_protected_sections_match(self) -> None:
        for relative in (GO, DERIVED):
            text = (ROOT / relative).read_text(encoding="utf-8")
            before = restore(relative, text)
            for title in ("Applicability", "Agent workflow", "Terminology", "Exceptions", "Verification", "Agent handoff"):
                with self.subTest(path=relative, section=title):
                    self.assertEqual(section(text, title), section(before, title))
            actual = section(text, "Requirements")
            if relative == GO:
                replacement = FOLLOWUP["edits"][GO]["replacements"][1]
                self.assertEqual(actual.count(replacement["after"]), 1)
                actual = actual.replace(replacement["after"], replacement["before"])
            self.assertEqual(actual, section(before, "Requirements"))

    def test_preservation_rejects_strength_and_scope_changes(self) -> None:
        for relative in (GO, DERIVED):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("**MUST**", text)
            for changed in (text.replace("**MUST**", "**MAY**", 1), text + "\nAdditional unreviewed obligation.\n"):
                with self.subTest(path=relative), self.assertRaises(AssertionError):
                    restore(relative, changed)

    def test_preservation_rejects_missing_or_duplicate_substitutions(self) -> None:
        for relative, data in FOLLOWUP["edits"].items():
            text = (ROOT / relative).read_text(encoding="utf-8")
            after = data["replacements"][0]["after"]
            for changed in (text.replace(after, "", 1), text + after):
                with self.subTest(path=relative), self.assertRaises(AssertionError):
                    restore(relative, changed)

    def test_go_route_distinguishes_recommendation_from_selection(self) -> None:
        text = (ROOT / GO).read_text(encoding="utf-8")
        self.assertIn("Go detection recommends this optional Specification", text)
        self.assertIn("project selection installs it", text)
        self.assertIn("> **Selection:** Detected", text)
        # Detected remains the existing metadata spelling, not install authority.
        catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
        item = next(item for item in catalog["specs"] if item["id"] == "languages/go")
        self.assertFalse(item["required"])
        self.assertIn(".go", item["detection"]["extensions"])

    def test_provenance_examples_preserve_alternatives_and_unknown_state(self) -> None:
        text = (ROOT / DERIVED).read_text(encoding="utf-8")
        examples = section(text, "Approved patterns")
        self.assertIn("placeholders, not measured project evidence", examples)
        self.assertIn("A revision is one source-identity option", examples)
        self.assertIn("Freshness is unknown; do not label the view current, even with a disclaimer", examples)
        self.assertIn("no current-state claim follows", examples)
        self.assertIn("Regenerate or revalidate", examples)
        self.assertIn("even if a freshness disclaimer", section(text, "Rejected patterns"))
        # These are editorial regression checks, not a semantic classifier.

    def test_go_example_bytes_are_unchanged(self) -> None:
        text = (ROOT / GO).read_text(encoding="utf-8")
        self.assertEqual(go_example(text), go_example(restore(GO, text)))


class GoSnippetTests(unittest.TestCase):
    def test_exact_go_snippet_and_rejection_positive_controls(self) -> None:
        go = shutil.which("go")
        if go is None:
            self.skipTest("Go toolchain unavailable; example execution was not verified")
        snippet = go_example((ROOT / GO).read_text(encoding="utf-8"))
        tests = '''package docsfixture
import "testing"
func TestParseCreateCommand(t *testing.T) {
    valid, err := ParseCreateCommand(CreateRequest{Name: "example"})
    if err != nil || valid.name != "example" { t.Fatalf("valid input: %+v, %v", valid, err) }
    invalid, err := ParseCreateCommand(CreateRequest{})
    if err == nil || invalid.name != "" { t.Fatalf("empty name not rejected: %+v, %v", invalid, err) }
}
func TestParseURL(t *testing.T) {
    valid, err := parseURL("https://example.invalid/path")
    if err != nil || valid.Host != "example.invalid" { t.Fatalf("valid URL: %v, %v", valid, err) }
    if _, err := parseURL("://"); err == nil { t.Fatal("invalid URI not rejected") }
}
'''
        with tempfile.TemporaryDirectory(prefix="spec-go-example-") as directory:
            root = Path(directory)
            env = os.environ.copy()
            env.update(GOTOOLCHAIN="local", GOPROXY="off", GOSUMDB="off", GOWORK="off", GOENV="off", GOFLAGS="", CGO_ENABLED="0", GOCACHE=str(root / "cache"))
            # Never download tools/modules or run commands from a consuming repo.
            for key in ("GOOS", "GOARCH"):
                env.pop(key, None)
            (root / "go.mod").write_text("module example.invalid/docsfixture\n\ngo 1.20\n", encoding="utf-8")
            (root / "example_test.go").write_text(tests, encoding="utf-8")
            source = root / "example.go"
            version = subprocess.run([go, "version"], capture_output=True, text=True, env=env, timeout=10, check=True).stdout.strip()
            print(f"Go example validation: {version}", flush=True)
            variants = (
                ("documented", snippet, 0),
                ("omitted-rejection", snippet.replace('if req.Name == "" {', 'if false {', 1), 1),
                ("lost-valid-value", snippet.replace('name: req.Name', 'name: ""', 1), 1),
            )
            for label, code, expected in variants:
                with self.subTest(variant=label):
                    source.write_text('package docsfixture\nimport ("errors"; "net/url")\n' + code, encoding="utf-8")
                    result = subprocess.run([go, "test", "-count=1", "-v", "./..."], cwd=root, capture_output=True, text=True, env=env, timeout=90)
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                    self.assertIn("TestParseCreateCommand", result.stdout)
                    self.assertIn("TestParseURL", result.stdout)
                    if expected:
                        self.assertIn("--- FAIL: TestParseCreateCommand", result.stdout)
                    else:
                        self.assertIn("--- PASS: TestParseCreateCommand", result.stdout)
                        self.assertIn("--- PASS: TestParseURL", result.stdout)


if __name__ == "__main__":
    unittest.main()
