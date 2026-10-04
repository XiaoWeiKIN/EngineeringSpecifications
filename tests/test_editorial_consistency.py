"""Check authoring/distribution consistency, not linguistic or semantic quality."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
GUIDE = "governance/specification-writing.md"


class EditorialConsistencyTests(unittest.TestCase):
    def test_authoring_entrypoints_resolve_the_same_local_guide(self) -> None:
        for relative in ("AGENTS.md", "CONTRIBUTING.md", "governance/README.md",
                         "specification/0000-template.md", "specification/README.md",
                         "README.md", "README.zh-CN.md"):
            with self.subTest(path=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                if relative == "AGENTS.md":
                    self.assertIn(f"`{GUIDE}`", text)
                else:
                    links = re.findall(r"\]\(([^)]+)\)", text)
                    targets = {(ROOT / relative).parent.joinpath(link).resolve()
                               for link in links if not link.startswith("https://")}
                    self.assertIn((ROOT / GUIDE).resolve(), targets)

    def test_authoring_guidance_is_not_installed_as_a_spec_dependency(self) -> None:
        for item in CATALOG["specs"]:
            self.assertNotEqual(item["path"], GUIDE)
            if item["id"].startswith(("core/", "languages/")):
                self.assertFalse(any(d.startswith("documentation/")
                                     for d in item["requires"]))

    def test_spec_index_matches_the_current_catalog_paths(self) -> None:
        text = (ROOT / "specification/README.md").read_text(encoding="utf-8")
        links = re.findall(r"\]\(([^)]+)\)", text)
        indexed = {"specification/" + link for link in links
                   if link.startswith(("core/", "languages/", "documentation/"))}
        self.assertEqual(indexed, {item["path"] for item in CATALOG["specs"]})

    def test_catalog_versions_match_the_first_compatibility_note(self) -> None:
        for item in CATALOG["specs"]:
            with self.subTest(spec=item["id"]):
                text = (ROOT / item["path"]).read_text(encoding="utf-8")
                compatibility = text.split("## Compatibility and migration\n", 1)[1]
                first = re.search(r"Version `([0-9]+\.[0-9]+\.[0-9]+)`", compatibility)
                self.assertIsNotNone(first)
                self.assertEqual(first.group(1), item["version"])

    def test_reference_sections_keep_external_sources_non_normative(self) -> None:
        for item in CATALOG["specs"]:
            with self.subTest(spec=item["id"]):
                text = (ROOT / item["path"]).read_text(encoding="utf-8")
                references = text.split("## References\n", 1)[1]
                self.assertIn("They do not add undeclared\nnormative obligations", references)

    def test_current_repository_entry_names_the_current_consumer(self) -> None:
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("RepoFoundry AI", text)
        self.assertNotIn("EngineeringWorkflow", text)


if __name__ == "__main__":
    unittest.main()
