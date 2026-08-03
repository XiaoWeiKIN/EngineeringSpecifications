#!/usr/bin/env python3
"""Validate an EngineeringSpecifications Catalog release identity."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import check


ROOT = Path(__file__).resolve().parent.parent


def changelog_has_release(root: Path, version: str) -> bool:
    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    pattern = re.compile(
        rf"^## \[{re.escape(version)}\] - \d{{4}}-\d{{2}}-\d{{2}}$",
        re.MULTILINE,
    )
    return pattern.search(changelog) is not None


def git_output(root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
        timeout=20,
    )
    return completed.stdout.strip()


def tag_commit(root: Path, version: str) -> str | None:
    tag = f"refs/tags/v{version}"
    completed = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", f"{tag}^{{commit}}"],
        cwd=root,
        check=False,
        text=True,
        capture_output=True,
        timeout=20,
    )
    if completed.returncode == 1:
        return None
    if completed.returncode != 0:
        detail = completed.stderr.strip() or "git rev-parse failed"
        raise ValueError(f"release tag resolution failed: {detail}")
    commit = completed.stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("release tag did not resolve to a full commit")
    return commit


def tagged_catalog_version(root: Path, commit: str) -> str:
    raw = git_output(root, "show", f"{commit}:catalog.json")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"tagged catalog.json is invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("tagged catalog.json: expected an object")
    version = data.get("catalog_version")
    if not isinstance(version, str):
        raise ValueError("tagged catalog.json: missing catalog_version")
    return version


def validate_release(
    root: Path,
    version: str,
    *,
    require_tag: bool,
) -> tuple[str, str | None]:
    if not check.SEMVER_RE.fullmatch(version):
        raise ValueError("version: expected MAJOR.MINOR.PATCH")
    catalog = check.load_catalog(root)
    actual = catalog["catalog_version"]
    if actual != version:
        raise ValueError(
            f"catalog version mismatch: requested {version}, found {actual}"
        )
    if not changelog_has_release(root, version):
        raise ValueError(
            f"CHANGELOG.md: missing release heading for {version}"
        )

    commit = tag_commit(root, version)
    if commit is None:
        if require_tag:
            raise ValueError(f"missing release tag: v{version}")
        return version, None
    tagged_version = tagged_catalog_version(root, commit)
    if tagged_version != version:
        raise ValueError(
            f"release tag v{version} contains Catalog {tagged_version}"
        )
    return version, commit


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate Catalog SemVer, Changelog, and release tag",
    )
    parser.add_argument("version", help="Catalog version MAJOR.MINOR.PATCH")
    parser.add_argument(
        "--require-tag",
        action="store_true",
        help="fail unless the matching immutable release tag exists",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        version, commit = validate_release(
            ROOT,
            args.version,
            require_tag=args.require_tag,
        )
    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        print(f"RELEASE_CHECK_FAILED: {exc}", file=sys.stderr)
        return 1
    if commit is None:
        print(f"RELEASE_READY: v{version} (tag not published)")
    else:
        print(f"RELEASE_OK: v{version} ({commit})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
