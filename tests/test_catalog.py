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
        self.assertEqual(catalog["catalog_version"], "0.2.0")
        self.assertEqual(len(catalog["specs"]), 4)
        self.assertEqual(
            CHECK.check_requirement_ids(ROOT, catalog),
            (
                "GO-API-001",
                "GO-BOUNDARY-001",
                "GO-COMPAT-001",
                "GO-ERROR-001",
                "GO-FORMAT-001",
                "GO-LIFECYCLE-001",
                "GO-NAME-001",
                "GO-NAME-002",
                "GO-TEST-001",
                "SEM-BOUNDARY-001",
                "SEM-COMPAT-001",
                "SEM-NAME-001",
                "SEM-SURFACE-001",
                "SEM-TYPE-001",
                "SEM-VERB-001",
            ),
        )

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

    def test_requirement_id_check_rejects_duplicates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / "specification" / "core" / "first.md"
            second = root / "specification" / "languages" / "second.md"
            first.parent.mkdir(parents=True)
            second.parent.mkdir(parents=True)
            requirement = (
                "# Test\n\n"
                "## Requirements\n\n"
                "### TEST-RULE-001 — Unique behavior\n"
            )
            first.write_text(requirement, encoding="utf-8")
            second.write_text(requirement, encoding="utf-8")
            catalog = {
                "specs": [
                    {"id": "core/first", "path": "specification/core/first.md"},
                    {
                        "id": "languages/second",
                        "path": "specification/languages/second.md",
                    },
                ]
            }

            with self.assertRaisesRegex(
                ValueError,
                "duplicate Requirement ID TEST-RULE-001",
            ):
                CHECK.check_requirement_ids(root, catalog)

    def test_requirement_id_check_rejects_malformed_headings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "specification" / "core" / "malformed.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                "# Test\n\n"
                "## Requirements\n\n"
                "### TEST-RULE-1 — Invalid number\n",
                encoding="utf-8",
            )
            catalog = {
                "specs": [
                    {
                        "id": "core/malformed",
                        "path": "specification/core/malformed.md",
                    }
                ]
            }

            with self.assertRaisesRegex(
                ValueError,
                "malformed Requirement heading",
            ):
                CHECK.check_requirement_ids(root, catalog)

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
