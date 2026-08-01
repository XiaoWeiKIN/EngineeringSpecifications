#!/usr/bin/env python3
"""Run the canonical EngineeringSpecifications repository checks."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent.parent
SPEC_ID_RE = re.compile(
    r"^[a-z0-9][a-z0-9._-]*(?:/[a-z0-9][a-z0-9._-]*)*$"
)
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIREMENT_HEADING_RE = re.compile(
    r"^### ([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+-[0-9]{3}) — \S.*$"
)
STATUS_RE = re.compile(
    r"^> \*\*Status:\*\* (Development|Stable|Deprecated)$",
    re.MULTILINE,
)
CATALOG_ID_LINE_RE = re.compile(
    r"^> \*\*Catalog ID:\*\* `([^`]+)`$",
    re.MULTILINE,
)
SELECTION_RE = re.compile(
    r"^> \*\*Selection:\*\* (Required|Detected|Explicit)$",
    re.MULTILINE,
)
ENFORCEMENT_RE = re.compile(
    r"\*\*Enforcement \((mechanical|review|hybrid)\):\*\*"
)
VERIFICATION_ROW_RE = re.compile(
    r"^\| `([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+-[0-9]{3})` \| \S.*\|$"
)
MAX_ACTIVATION_SUMMARY_LENGTH = 180


def expect_object(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{label}: expected an object")
    return value


def expect_exact_keys(
    value: dict[str, object],
    *,
    required: set[str],
    optional: set[str] | None = None,
    label: str,
) -> None:
    allowed = required | (optional or set())
    missing = sorted(required - set(value))
    unknown = sorted(set(value) - allowed)
    if missing:
        raise ValueError(f"{label}: missing keys: {', '.join(missing)}")
    if unknown:
        raise ValueError(f"{label}: unknown keys: {', '.join(unknown)}")


def expect_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}: expected a non-empty string")
    return value


def expect_string_list(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{label}: expected an array")
    values = tuple(
        expect_string(item, f"{label}[{index}]")
        for index, item in enumerate(value)
    )
    if len(values) != len(set(values)):
        raise ValueError(f"{label}: duplicate values are not allowed")
    return values


def safe_relative(value: object, label: str) -> str:
    text = expect_string(value, label)
    if "\\" in text:
        raise ValueError(f"{label}: backslashes are not portable")
    path = PurePosixPath(text)
    if path.is_absolute() or not path.parts:
        raise ValueError(f"{label}: expected a relative path")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError(f"{label}: path traversal is not allowed")
    return path.as_posix()


def digest_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_catalog(root: Path) -> dict[str, object]:
    catalog_path = root / "catalog.json"
    if catalog_path.is_symlink() or not catalog_path.is_file():
        raise ValueError("catalog.json: expected a non-symlink regular file")
    try:
        data = expect_object(
            json.loads(catalog_path.read_text(encoding="utf-8")),
            "catalog",
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"catalog.json: invalid JSON: {exc}") from exc
    expect_exact_keys(
        data,
        required={
            "schema_version",
            "catalog_id",
            "catalog_version",
            "specs",
        },
        label="catalog",
    )
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ValueError("catalog.schema_version: expected 1")
    expect_string(data["catalog_id"], "catalog.catalog_id")
    version = expect_string(data["catalog_version"], "catalog.catalog_version")
    if not SEMVER_RE.fullmatch(version):
        raise ValueError("catalog.catalog_version: expected MAJOR.MINOR.PATCH")
    raw_specs = data["specs"]
    if not isinstance(raw_specs, list) or not raw_specs:
        raise ValueError("catalog.specs: expected a non-empty array")

    ids: set[str] = set()
    dependencies: dict[str, tuple[str, ...]] = {}
    paths: set[str] = set()
    for index, raw in enumerate(raw_specs):
        label = f"catalog.specs[{index}]"
        item = expect_object(raw, label)
        expect_exact_keys(
            item,
            required={
                "id",
                "version",
                "path",
                "sha256",
                "required",
                "requires",
                "applies_to",
                "description",
            },
            optional={"detection"},
            label=label,
        )
        spec_id = expect_string(item["id"], f"{label}.id")
        if not SPEC_ID_RE.fullmatch(spec_id):
            raise ValueError(f"{label}.id: invalid specification ID")
        if spec_id in ids:
            raise ValueError(f"{label}.id: duplicate ID: {spec_id}")
        ids.add(spec_id)
        spec_version = expect_string(item["version"], f"{label}.version")
        if not SEMVER_RE.fullmatch(spec_version):
            raise ValueError(f"{label}.version: expected MAJOR.MINOR.PATCH")
        relative = safe_relative(item["path"], f"{label}.path")
        if not relative.endswith(".md"):
            raise ValueError(f"{label}.path: expected Markdown")
        if relative in paths:
            raise ValueError(f"{label}.path: duplicate path: {relative}")
        paths.add(relative)
        declared = expect_string(item["sha256"], f"{label}.sha256")
        if not SHA256_RE.fullmatch(declared):
            raise ValueError(f"{label}.sha256: expected lowercase SHA-256")
        if type(item["required"]) is not bool:
            raise ValueError(f"{label}.required: expected a Boolean")
        dependencies[spec_id] = expect_string_list(
            item["requires"],
            f"{label}.requires",
        )
        scopes = expect_string_list(
            item["applies_to"],
            f"{label}.applies_to",
        )
        if not scopes:
            raise ValueError(f"{label}.applies_to: at least one scope required")
        description = expect_string(
            item["description"],
            f"{label}.description",
        )
        if not description.startswith("Load when "):
            raise ValueError(
                f"{label}.description: expected an activation summary "
                "starting with 'Load when '"
            )
        if len(description) > MAX_ACTIVATION_SUMMARY_LENGTH:
            raise ValueError(
                f"{label}.description: activation summary exceeds "
                f"{MAX_ACTIVATION_SUMMARY_LENGTH} characters"
            )
        if "detection" in item:
            detection = expect_object(
                item["detection"],
                f"{label}.detection",
            )
            expect_exact_keys(
                detection,
                required={"filenames", "extensions"},
                label=f"{label}.detection",
            )
            filenames = expect_string_list(
                detection["filenames"],
                f"{label}.detection.filenames",
            )
            extensions = expect_string_list(
                detection["extensions"],
                f"{label}.detection.extensions",
            )
            if not filenames and not extensions:
                raise ValueError(
                    f"{label}.detection: at least one rule required"
                )
        source = root
        for component in PurePosixPath(relative).parts:
            source = source / component
            if source.is_symlink():
                raise ValueError(f"{label}.path: symbolic links are forbidden")
        if not source.is_file():
            raise ValueError(f"{label}.path: missing file: {relative}")
        actual = digest_file(source)
        if actual != declared:
            raise ValueError(
                f"{label}.sha256: digest mismatch for {relative}: "
                f"expected {declared}, got {actual}"
            )

    for spec_id, requires in dependencies.items():
        missing = sorted(set(requires) - ids)
        if missing:
            raise ValueError(
                f"{spec_id}: missing dependencies: {', '.join(missing)}"
            )

    visiting: list[str] = []
    visited: set[str] = set()

    def visit(spec_id: str) -> None:
        if spec_id in visiting:
            cycle = " -> ".join((*visiting, spec_id))
            raise ValueError(f"catalog: dependency cycle: {cycle}")
        if spec_id in visited:
            return
        visiting.append(spec_id)
        for dependency in dependencies[spec_id]:
            visit(dependency)
        visiting.pop()
        visited.add(spec_id)

    for spec_id in sorted(ids):
        visit(spec_id)
    return data


def check_markdown_links() -> None:
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        for target in pattern.findall(path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "#")):
                continue
            relative = target.split("#", 1)[0]
            if not relative:
                continue
            resolved = (path.parent / relative).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError as exc:
                raise ValueError(
                    f"{path.relative_to(ROOT)}: link escapes repository: "
                    f"{target}"
                ) from exc
            if not resolved.exists():
                raise ValueError(
                    f"{path.relative_to(ROOT)}: broken link: {target}"
                )


def single_metadata_value(
    pattern: re.Pattern[str],
    content: str,
    relative: str,
    label: str,
) -> str:
    matches = pattern.findall(content)
    if len(matches) != 1:
        raise ValueError(
            f"{relative}: expected exactly one {label} metadata marker"
        )
    return matches[0]


def markdown_section(
    content: str,
    heading: str,
    relative: str,
) -> list[str]:
    lines = content.splitlines()
    positions = [index for index, line in enumerate(lines) if line == heading]
    if len(positions) != 1:
        raise ValueError(
            f"{relative}: expected exactly one {heading} section"
        )
    start = positions[0] + 1
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return lines[start:end]


def expected_selection(spec: dict[str, object]) -> str:
    if spec["required"] is True:
        return "Required"
    if "detection" in spec:
        return "Detected"
    return "Explicit"


def check_requirement_ids(
    root: Path,
    catalog: dict[str, object],
) -> tuple[str, ...]:
    seen: dict[str, str] = {}
    for raw_spec in catalog["specs"]:
        spec = expect_object(raw_spec, "catalog.spec")
        spec_id = expect_string(spec["id"], "catalog.spec.id")
        relative = safe_relative(spec["path"], f"{spec_id}.path")
        path = root / relative
        content = path.read_text(encoding="utf-8")

        single_metadata_value(STATUS_RE, content, relative, "Status")
        document_id = single_metadata_value(
            CATALOG_ID_LINE_RE,
            content,
            relative,
            "Catalog ID",
        )
        if document_id != spec_id:
            raise ValueError(
                f"{relative}: Catalog ID {document_id!r} does not match "
                f"{spec_id!r}"
            )
        selection = single_metadata_value(
            SELECTION_RE,
            content,
            relative,
            "Selection",
        )
        expected = expected_selection(spec)
        if selection != expected:
            raise ValueError(
                f"{relative}: Selection {selection!r} does not match "
                f"Catalog behavior {expected!r}"
            )
        if content.count("> **Routing:**") != 1:
            raise ValueError(
                f"{relative}: expected exactly one Routing metadata marker"
            )
        if content.count("> **Catalog metadata:**") != 1:
            raise ValueError(
                f"{relative}: expected exactly one Catalog metadata marker"
            )

        markdown_section(content, "## Purpose", relative)
        markdown_section(content, "## Applicability", relative)
        markdown_section(content, "## Agent workflow", relative)
        requirement_lines = markdown_section(
            content,
            "## Requirements",
            relative,
        )
        verification_lines = markdown_section(
            content,
            "## Verification",
            relative,
        )
        markdown_section(content, "## Agent handoff", relative)
        markdown_section(
            content,
            "## Compatibility and migration",
            relative,
        )

        headings: list[tuple[int, str]] = []
        for index, line in enumerate(requirement_lines):
            if not line.startswith("### "):
                continue
            match = REQUIREMENT_HEADING_RE.fullmatch(line)
            if match is None:
                raise ValueError(
                    f"{relative}: malformed Requirement heading: {line}"
                )
            headings.append((index, match.group(1)))
        if not headings:
            raise ValueError(
                f"{relative}: Requirements section has no stable IDs"
            )

        local_ids: list[str] = []
        for heading_index, (start, requirement_id) in enumerate(headings):
            end = (
                headings[heading_index + 1][0]
                if heading_index + 1 < len(headings)
                else len(requirement_lines)
            )
            block = "\n".join(requirement_lines[start:end])
            markers = {
                "Rationale": block.count("**Rationale (non-normative):**"),
                "Evidence": block.count("**Evidence:**"),
            }
            for label, count in markers.items():
                if count != 1:
                    raise ValueError(
                        f"{relative}: {requirement_id} requires exactly one "
                        f"{label} marker"
                    )
            enforcement = ENFORCEMENT_RE.findall(block)
            if len(enforcement) != 1:
                raise ValueError(
                    f"{relative}: {requirement_id} requires exactly one "
                    "Enforcement class"
                )
            previous = seen.get(requirement_id)
            if previous is not None:
                raise ValueError(
                    f"{relative}: duplicate Requirement ID {requirement_id}; "
                    f"already declared in {previous}"
                )
            seen[requirement_id] = relative
            local_ids.append(requirement_id)

        verification_ids: list[str] = []
        for line in verification_lines:
            match = VERIFICATION_ROW_RE.fullmatch(line)
            if match is not None:
                verification_ids.append(match.group(1))
                continue
            if line.startswith("| `"):
                raise ValueError(
                    f"{relative}: malformed Verification row: {line}"
                )
        duplicate_verification = sorted(
            requirement_id
            for requirement_id in set(verification_ids)
            if verification_ids.count(requirement_id) > 1
        )
        if duplicate_verification:
            raise ValueError(
                f"{relative}: duplicate Verification IDs: "
                + ", ".join(duplicate_verification)
            )
        missing = sorted(set(local_ids) - set(verification_ids))
        unknown = sorted(set(verification_ids) - set(local_ids))
        if missing or unknown:
            details: list[str] = []
            if missing:
                details.append("missing " + ", ".join(missing))
            if unknown:
                details.append("unknown " + ", ".join(unknown))
            raise ValueError(
                f"{relative}: Verification coverage mismatch: "
                + "; ".join(details)
            )
    return tuple(sorted(seen))


def run_tests() -> None:
    subprocess.run(
        [
            sys.executable,
            "-B",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(ROOT / "tests"),
            "-p",
            "test_*.py",
        ],
        cwd=ROOT,
        check=True,
    )


def main() -> int:
    try:
        catalog = load_catalog(ROOT)
        check_requirement_ids(ROOT, catalog)
        check_markdown_links()
        run_tests()
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        print(f"CHECK_FAILED: {exc}", file=sys.stderr)
        return 1
    print(
        "CHECK_OK: "
        f"{catalog['catalog_id']}@{catalog['catalog_version']} "
        f"({len(catalog['specs'])} specifications)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
