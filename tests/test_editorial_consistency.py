"""Keep local authoring references consistent without adding consumer contracts."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = (ROOT / "governance/specification-authoring.md").resolve()
CATALOG = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))


class EditorialConsistencyTests(unittest.TestCase):
    def test_authoring_entrypoints_link_one_local_guide(self) -> None:
        paths = (
            "AGENTS.md", "CONTRIBUTING.md", "governance/README.md",
            "specification/0000-template.md", "specification/README.md",
            "README.md", "README.zh-CN.md",
        )
        for relative in paths:
            with self.subTest(path=relative):
                source = ROOT / relative
                links = re.findall(r"\]\(([^)]+)\)", source.read_text(encoding="utf-8"))
                targets = {(source.parent / link).resolve() for link in links
                           if not link.startswith(("https://", "http://", "#"))}
                self.assertIn(GUIDE, targets)

    def test_authoring_guide_never_becomes_a_consumer_spec(self) -> None:
        self.assertTrue(GUIDE.is_file())
        for item in CATALOG["specs"]:
            self.assertNotEqual((ROOT / item["path"]).resolve(), GUIDE)
            self.assertFalse(any(dep.startswith("documentation/")
                                 for dep in item["requires"])
                             if item["id"].startswith(("core/", "languages/"))
                             else False)

    def test_specification_index_tracks_catalog_paths(self) -> None:
        source = ROOT / "specification/README.md"
        links = re.findall(r"\]\(([^)]+)\)", source.read_text(encoding="utf-8"))
        indexed = {"specification/" + link for link in links
                   if link.startswith(("core/", "languages/", "documentation/"))}
        self.assertEqual(indexed, {item["path"] for item in CATALOG["specs"]})

    def test_remote_release_is_not_inferred_from_local_validator(self) -> None:
        text = (ROOT / "RELEASING.md").read_text(encoding="utf-8")
        self.assertIn("git ls-remote --tags origin", text)
        self.assertIn("A local `RELEASE_OK` alone does not", text)

    def test_current_consumer_name(self) -> None:
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("RepoFoundry AI", text)
        self.assertNotIn("EngineeringWorkflow", text)


if __name__ == "__main__":
    unittest.main()
