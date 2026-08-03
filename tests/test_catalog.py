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


def catalog_spec(spec_id: str, path: str) -> dict[str, object]:
    return {
        "id": spec_id,
        "path": path,
        "required": True,
    }


def contract_document(
    spec_id: str,
    *,
    heading: str = "### TEST-RULE-001 — Unique behavior",
    evidence: bool = True,
    verification_id: str = "TEST-RULE-001",
    selection: str = "Required",
) -> str:
    evidence_text = "\n**Evidence:** Reviewed artifact.\n" if evidence else "\n"
    return (
        "# Test Specification\n\n"
        "> **Status:** Development\n>\n"
        f"> **Catalog ID:** `{spec_id}`\n>\n"
        f"> **Selection:** {selection}\n>\n"
        "> **Routing:** Test routing contract.\n>\n"
        "> **Catalog metadata:** `catalog.json` is authoritative.\n\n"
        "## Purpose\n\nTest purpose.\n\n"
        "## Applicability\n\nLoad for tests.\n\n"
        "## Agent workflow\n\n1. Apply the contract.\n\n"
        "## Requirements\n\n"
        f"{heading}\n\n"
        "The implementation **MUST** preserve the behavior.\n\n"
        "**Rationale (non-normative):** Prevent drift.\n\n"
        "**Enforcement (review):** Review the behavior.\n"
        f"{evidence_text}\n"
        "## Verification\n\n"
        "| Requirement | Minimum verification |\n"
        "| --- | --- |\n"
        f"| `{verification_id}` | Reviewed behavior |\n\n"
        "## Agent handoff\n\nReport evidence.\n\n"
        "## Compatibility and migration\n\nNo migration.\n"
    )


class CatalogTestCase(unittest.TestCase):
    def test_repository_catalog_is_valid(self) -> None:
        catalog = CHECK.load_catalog(ROOT)
        self.assertEqual(
            catalog["catalog_id"],
            "io.github.xiaoweikin.engineering-specifications",
        )
        self.assertEqual(catalog["catalog_version"], "1.3.0")
        self.assertEqual(len(catalog["specs"]), 3)
        self.assertEqual(
            {item["id"] for item in catalog["specs"]},
            {
                "core/semantic-naming",
                "core/data-boundaries",
                "languages/go",
            },
        )
        for item in catalog["specs"]:
            self.assertTrue(item["description"].startswith("Load when "))
            self.assertLessEqual(
                len(item["description"]),
                CHECK.MAX_ACTIVATION_SUMMARY_LENGTH,
            )
        go_spec = next(
            item for item in catalog["specs"] if item["id"] == "languages/go"
        )
        semantic_naming = next(
            item
            for item in catalog["specs"]
            if item["id"] == "core/semantic-naming"
        )
        self.assertEqual(semantic_naming["version"], "1.1.0")
        self.assertIn("Normalize or Extract", semantic_naming["description"])
        semantic_naming_text = (
            ROOT / "specification/core/semantic-naming.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "its own output **MUST** produce the same result",
            semantic_naming_text,
        )
        self.assertIn(
            "`Extract` **MUST NOT** be a catch-all name",
            semantic_naming_text,
        )
        self.assertEqual(go_spec["version"], "0.4.0")
        self.assertIn("**/go.sum", go_spec["applies_to"])
        self.assertIn("**/vendor/modules.txt", go_spec["applies_to"])
        self.assertEqual(
            CHECK.check_requirement_ids(ROOT, catalog),
            (
                "DATA-EFFECT-001",
                "DATA-ERROR-001",
                "DATA-NORMALIZE-001",
                "DATA-PARSE-001",
                "DATA-SHAPE-001",
                "GO-API-001",
                "GO-BOUNDARY-001",
                "GO-COMPAT-001",
                "GO-ERROR-001",
                "GO-FORMAT-001",
                "GO-GENERATE-001",
                "GO-LIFECYCLE-001",
                "GO-MODULE-001",
                "GO-NAME-001",
                "GO-NAME-002",
                "GO-TEST-001",
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
            catalog = CHECK.load_catalog(ROOT)
            for item in catalog["specs"]:
                relative = item["path"]
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / relative).read_bytes())
            (root / "specification/languages/go.md").write_text(
                "# changed\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "digest mismatch"):
                CHECK.load_catalog(root)

    def test_requirement_contract_rejects_duplicate_ids(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / "specification/core/first.md"
            second = root / "specification/core/second.md"
            first.parent.mkdir(parents=True)
            first.write_text(
                contract_document("core/first"),
                encoding="utf-8",
            )
            second.write_text(
                contract_document("core/second"),
                encoding="utf-8",
            )
            catalog = {
                "specs": [
                    catalog_spec("core/first", "specification/core/first.md"),
                    catalog_spec("core/second", "specification/core/second.md"),
                ]
            }
            with self.assertRaisesRegex(
                ValueError,
                "duplicate Requirement ID TEST-RULE-001",
            ):
                CHECK.check_requirement_ids(root, catalog)

    def test_requirement_contract_rejects_malformed_heading(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "specification/core/malformed.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                contract_document(
                    "core/malformed",
                    heading="### TEST-RULE-1 — Invalid number",
                ),
                encoding="utf-8",
            )
            catalog = {
                "specs": [
                    catalog_spec(
                        "core/malformed",
                        "specification/core/malformed.md",
                    )
                ]
            }
            with self.assertRaisesRegex(
                ValueError,
                "malformed Requirement heading",
            ):
                CHECK.check_requirement_ids(root, catalog)

    def test_requirement_contract_requires_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "specification/core/missing-evidence.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                contract_document("core/missing-evidence", evidence=False),
                encoding="utf-8",
            )
            catalog = {
                "specs": [
                    catalog_spec(
                        "core/missing-evidence",
                        "specification/core/missing-evidence.md",
                    )
                ]
            }
            with self.assertRaisesRegex(ValueError, "exactly one Evidence"):
                CHECK.check_requirement_ids(root, catalog)

    def test_requirement_contract_requires_exact_verification_coverage(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "specification/core/missing-verification.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                contract_document(
                    "core/missing-verification",
                    verification_id="TEST-OTHER-001",
                ),
                encoding="utf-8",
            )
            catalog = {
                "specs": [
                    catalog_spec(
                        "core/missing-verification",
                        "specification/core/missing-verification.md",
                    )
                ]
            }
            with self.assertRaisesRegex(
                ValueError,
                "Verification coverage mismatch",
            ):
                CHECK.check_requirement_ids(root, catalog)

    def test_requirement_contract_rejects_catalog_id_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "specification/core/actual.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                contract_document("core/wrong"),
                encoding="utf-8",
            )
            catalog = {
                "specs": [
                    catalog_spec("core/actual", "specification/core/actual.md")
                ]
            }
            with self.assertRaisesRegex(ValueError, "does not match"):
                CHECK.check_requirement_ids(root, catalog)

    def test_formal_specification_template_is_an_authoring_resource(self) -> None:
        template_path = ROOT / "specification/0000-template.md"
        template = template_path.read_text(encoding="utf-8")
        for marker in (
            "> **Status:** Development",
            "> **Catalog ID:**",
            "> **Routing:**",
            "## Applicability",
            "## Agent workflow",
            "## Requirements",
            "### AREA-TOPIC-001",
            "**Enforcement (mechanical | review | hybrid):**",
            "**Evidence:**",
            "## Approved patterns",
            "## Rejected patterns",
            "## Exceptions",
            "## Verification",
            "## Agent handoff",
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
