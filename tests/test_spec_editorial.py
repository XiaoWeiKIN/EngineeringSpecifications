"""Test the bounded editorial review and its example, not prose conformance."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import types
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads(
    (ROOT / "tests/fixtures/spec-editorial-baseline.json").read_text(encoding="utf-8")
)
DATA_PATH = "specification/core/data-boundaries.md"
GO_PATH = "specification/languages/go/functional-options.md"
FOLLOWUP = json.loads(
    (ROOT / "tests/fixtures/spec-editorial-followup.json").read_text(encoding="utf-8")
)["edits"]


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sections(text: str) -> dict[str, str]:
    parts = re.split(r"(?m)^## ", text)
    result = {"preamble": parts[0]}
    for part in parts[1:]:
        name, _, rest = part.partition("\n")
        if name in result:
            raise AssertionError(f"Duplicate section: {name}")
        result[name] = rest
    return result


def restore_subject_edits(relative: str, text: str) -> str:
    # Only the two reviewed substitutions are permitted by this snapshot.
    # Future normative edits need their own reviewed baseline, not a style waiver.
    for old, new in BASELINE["requirement_edits"].get(relative, []):
        if text.count(new) != 1:
            raise AssertionError("Missing or duplicated reviewed subject edit")
        text = text.replace(new, old)
    return text


class EditorialBoundaryTests(unittest.TestCase):
    def test_catalog_only_changes_reviewed_spec_patch_identities(self) -> None:
        catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(catalog["schema_version"], 1)
        self.assertEqual(catalog["catalog_version"], "1.7.1")
        self.assertEqual(
            {item["id"] for item in catalog["specs"]},
            set(BASELINE["catalog_metadata"]),
        )
        for item in catalog["specs"]:
            with self.subTest(spec=item["id"]):
                old = BASELINE["catalog_metadata"][item["id"]]
                metadata = {k: v for k, v in item.items() if k not in ("sha256", "version")}
                self.assertEqual(digest(json.dumps(metadata, sort_keys=True)), old["metadata_sha256"])
                if item["path"] in (DATA_PATH, GO_PATH):
                    self.assertEqual(item["version"], "0.2.1")
                    self.assertNotEqual(item["sha256"], old["sha256"])
                    self.assertEqual(item["sha256"], hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest())
                elif item["path"] in FOLLOWUP:
                    # A separate reviewed delta extends, not replaces, the
                    # original baseline. Follow-up tests reverse every edit.
                    reviewed = FOLLOWUP[item["path"]]
                    self.assertEqual(reviewed["before_sha256"], old["sha256"])
                    self.assertEqual(reviewed["old_version"], old["version"])
                    self.assertEqual(item["version"], reviewed["version"])
                    self.assertEqual(item["sha256"], reviewed["sha256"])
                    self.assertEqual(item["sha256"], hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest())
                else:
                    self.assertEqual(item["version"], old["version"])
                    self.assertEqual(item["sha256"], old["sha256"])

    def test_reviewed_sections_preserve_baseline_except_named_subjects(self) -> None:
        for relative, expected in BASELINE["sections"].items():
            text = (ROOT / relative).read_text(encoding="utf-8")
            restored = sections(restore_subject_edits(relative, text))
            for name, expected_digest in expected.items():
                with self.subTest(path=relative, section=name):
                    self.assertEqual(digest(restored[name]), expected_digest)

    def test_preservation_detects_changed_strength_or_quantity(self) -> None:
        text = (ROOT / GO_PATH).read_text(encoding="utf-8")
        restored = sections(restore_subject_edits(GO_PATH, text))["Requirements"]
        expected = BASELINE["sections"][GO_PATH]["Requirements"]
        self.assertEqual(digest(restored), expected)
        for before, after in (("**MUST**", "**SHOULD**"), ("exactly\nonce", "at least\nonce")):
            with self.subTest(before=before):
                self.assertIn(before, restored)
                self.assertNotEqual(digest(restored.replace(before, after, 1)), expected)

    def test_authoring_entrypoints_use_one_local_non_normative_guide(self) -> None:
        guide = ROOT / "governance/specification-authoring.md"
        for relative in ("AGENTS.md", "CONTRIBUTING.md", "specification/0000-template.md"):
            path = ROOT / relative
            links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8"))
            matches = [link for link in links if link.endswith("specification-authoring.md")]
            self.assertEqual(len(matches), 1, relative)
            self.assertEqual((path.parent / matches[0]).resolve(), guide.resolve())
        text = guide.read_text(encoding="utf-8")
        self.assertIn("non-normative guidance", text)
        self.assertIn("requires no installed Skill", text)
        self.assertNotIn("### DOC-", text)
        catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
        self.assertNotIn("governance/specification-authoring.md", {item["path"] for item in catalog["specs"]})
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("RepoFoundry AI", agents)
        self.assertNotIn("EngineeringWorkflow", agents)

    def test_previous_release_notes_are_byte_preserved(self) -> None:
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertEqual(changelog.count("## [1.7.0]"), 1)
        self.assertEqual(digest(changelog.split("## [1.7.0]", 1)[1]), BASELINE["release_history_sha256"])
        self.assertIn("## Unreleased", changelog)
        # Release preparation changes only the new heading, not past notes.
        self.assertEqual(changelog.count("## [1.7.1] - 2026-10-04"), 1)


class BoundaryExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        text = (ROOT / DATA_PATH).read_text(encoding="utf-8")
        start, end = "<!-- boundary-effect-example:start -->", "<!-- boundary-effect-example:end -->"
        self.assertEqual(text.count(start), 1)
        self.assertEqual(text.count(end), 1)
        fragment = text.split(start, 1)[1].split(end, 1)[0]
        blocks = re.findall(r"^```python\n(.*?)^```$", fragment, flags=re.MULTILINE | re.DOTALL)
        self.assertEqual(len(blocks), 1)
        name = "_documentation_boundary_fixture"
        self.example = types.ModuleType(name)
        sys.modules[name] = self.example
        self.addCleanup(sys.modules.pop, name, None)
        # Execute only the marked, repository-owned test example. This is not
        # a runner for untrusted user documents or a product runtime dependency.
        exec(compile(blocks[0], DATA_PATH + "::boundary-effect-example", "exec"), self.example.__dict__)

    def test_exact_documented_entrypoint_passes_its_controls(self) -> None:
        self.example.check_boundary(self.example.handle_create)

    def test_missing_and_invalid_values_do_not_reach_effect_spies(self) -> None:
        for value in (None, 0, -1, True, "7", 2.5):
            with self.subTest(value=value):
                spy = self.example.EffectsSpy()
                with self.assertRaises(self.example.Rejected):
                    self.example.handle_create({"retention_days": value}, spy)
                self.assertEqual(spy.writes, [])
                self.assertEqual(spy.messages, [])

    def test_observers_detect_effects_before_rejection(self) -> None:
        for effect in ("write", "publish"):
            with self.subTest(effect=effect):
                def broken(transport, spy):
                    getattr(spy, effect)(transport)
                    return self.example.handle_create(transport, spy)
                with self.assertRaises(AssertionError):
                    self.example.check_boundary(broken)

    def test_positive_control_detects_unconnected_observers(self) -> None:
        for omitted in ("write", "publish"):
            with self.subTest(omitted=omitted):
                def broken(transport, spy):
                    command = self.example.parse_create_command(transport)
                    for effect in ("write", "publish"):
                        if effect != omitted:
                            getattr(spy, effect)(command)
                    return command
                with self.assertRaises(AssertionError):
                    self.example.check_boundary(broken)


if __name__ == "__main__":
    unittest.main()
