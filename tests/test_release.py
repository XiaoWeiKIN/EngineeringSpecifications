from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
MODULE_SPEC = importlib.util.spec_from_file_location(
    "engineering_spec_release_check",
    ROOT / "scripts" / "check_release.py",
)
assert MODULE_SPEC is not None and MODULE_SPEC.loader is not None
RELEASE = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(RELEASE)
CURRENT_VERSION = RELEASE.check.load_catalog(ROOT)["catalog_version"]


def write_release_fixture(repository: Path) -> None:
    subprocess.run(
        ["git", "init", "-b", "main"],
        cwd=repository,
        check=True,
        capture_output=True,
    )
    (repository / "catalog.json").write_bytes(
        (ROOT / "catalog.json").read_bytes()
    )
    for item in RELEASE.check.load_catalog(ROOT)["specs"]:
        relative = item["path"]
        target = repository / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / relative).read_bytes())
    (repository / "CHANGELOG.md").write_text(
        (
            "# Changelog\n\n"
            f"## [{CURRENT_VERSION}] - 2026-08-03\n"
        ),
        encoding="utf-8",
    )


class ReleaseCheckTestCase(unittest.TestCase):
    def test_prepared_release_is_ready_before_tag_publication(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            write_release_fixture(repository)
            version, commit = RELEASE.validate_release(
                repository,
                CURRENT_VERSION,
                require_tag=False,
            )
            self.assertEqual(version, CURRENT_VERSION)
            self.assertIsNone(commit)

    def test_release_rejects_invalid_version(self) -> None:
        with self.assertRaisesRegex(ValueError, "MAJOR.MINOR.PATCH"):
            RELEASE.validate_release(ROOT, "main", require_tag=False)

    def test_release_rejects_catalog_version_mismatch(self) -> None:
        with self.assertRaisesRegex(ValueError, "catalog version mismatch"):
            RELEASE.validate_release(ROOT, "9.9.9", require_tag=False)

    def test_release_requires_published_tag_when_requested(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            write_release_fixture(repository)
            with self.assertRaisesRegex(ValueError, "missing release tag"):
                RELEASE.validate_release(
                    repository,
                    CURRENT_VERSION,
                    require_tag=True,
                )


if __name__ == "__main__":
    unittest.main()
