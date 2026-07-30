from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MODULE_SPEC = importlib.util.spec_from_file_location(
    "engineering_spec_check",
    ROOT / "scripts" / "check.py",
)
assert MODULE_SPEC is not None and MODULE_SPEC.loader is not None
CHECK = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(CHECK)


class CatalogTestCase(unittest.TestCase):
    def test_repository_catalog_is_valid(self) -> None:
        catalog = CHECK.load_catalog(ROOT)
        self.assertEqual(
            catalog["catalog_id"],
            "io.github.xiaoweikin.engineering-specifications",
        )
        self.assertEqual(len(catalog["specs"]), 4)

    def test_safe_relative_path_rejects_traversal(self) -> None:
        with self.assertRaisesRegex(ValueError, "path traversal"):
            CHECK.safe_relative("../outside.md", "test.path")

    def test_catalog_detects_digest_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "catalog.json").write_bytes(
                (ROOT / "catalog.json").read_bytes()
            )
            for relative in (
                "specification/core/semantic-naming.md",
                "specification/languages/go.md",
                "specification/languages/python.md",
                "specification/languages/typescript.md",
            ):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / relative).read_bytes())
            (root / "specification/languages/go.md").write_text(
                "# changed\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "digest mismatch"):
                CHECK.load_catalog(root)

    def test_formal_specification_template_is_an_authoring_resource(self) -> None:
        template_path = ROOT / "specification" / "0000-template.md"
        template = template_path.read_text(encoding="utf-8")
        for marker in (
            "> **Status:** Development",
            "> **Catalog ID:**",
            "## Applicability",
            "## Requirements",
            "### AREA-TOPIC-001",
            "**Enforcement:**",
            "**Evidence:**",
            "## Approved patterns",
            "## Rejected patterns",
            "## Exceptions",
            "## Verification",
            "## Compatibility and migration",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, template)

        catalog = CHECK.load_catalog(ROOT)
        catalog_paths = {item["path"] for item in catalog["specs"]}
        self.assertNotIn(
            "specification/0000-template.md",
            catalog_paths,
        )


if __name__ == "__main__":
    unittest.main()
