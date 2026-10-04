"""Exercise the exact documented fragment, not a consumer conformance claim."""
from __future__ import annotations

import re
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]


class RecordingRepository:
    def __init__(self) -> None:
        self.write_count = 0

    def write(self, command: object) -> None:
        self.write_count += 1


class RecordingPublisher:
    def __init__(self) -> None:
        self.message_count = 0

    def publish(self, command: object) -> None:
        self.message_count += 1


def boundary_entry(shape, repository, publisher):
    """Illustrative domain: a decoded mapping with positive retention days."""
    days = shape.get("retention_days")
    if type(days) is not int or days <= 0:
        return SimpleNamespace(
            command=None, error=SimpleNamespace(field="retention_days")
        )
    command = {"retention_days": days}
    repository.write(command)
    publisher.publish(command)
    return SimpleNamespace(command=command, error=None)


def run_documented_fragment(entry, invalid_transport) -> dict:
    text = (ROOT / "specification/core/data-boundaries.md").read_text(
        encoding="utf-8"
    )
    examples = text.split("## Approved patterns\n", 1)[1].split(
        "## Rejected patterns\n", 1
    )[0]
    fragments = re.findall(r"^```python\n(.*?)^```$", examples, re.M | re.S)
    if len(fragments) != 1:
        raise AssertionError("Expected exactly one documented Python fragment")
    namespace = {
        "recording_repository": RecordingRepository,
        "recording_publisher": RecordingPublisher,
        "boundary_entry": entry,
        "invalid_transport": invalid_transport,
    }
    # The versioned local example is test code. No remotely loaded Specification
    # is executed, and these fakes perform no network, process, or file effects.
    exec(compile(fragments[0], "data-boundaries.md example", "exec"), namespace)
    return namespace


class DocumentationExampleTests(unittest.TestCase):
    def test_documented_rejection_fragment_exercises_the_boundary(self) -> None:
        for shape in ({}, {"retention_days": 0}, {"retention_days": -1},
                      {"retention_days": False}, {"retention_days": "7"}):
            with self.subTest(shape=shape):
                calls = []

                def observed_entry(value, repository, publisher):
                    calls.append(value)
                    return boundary_entry(value, repository, publisher)

                run_documented_fragment(observed_entry, shape)
                self.assertEqual(calls, [shape])

    def test_valid_input_control_reaches_both_recording_spies(self) -> None:
        repository, publisher = RecordingRepository(), RecordingPublisher()
        outcome = boundary_entry({"retention_days": 7}, repository, publisher)
        self.assertIsNone(outcome.error)
        self.assertEqual(outcome.command, {"retention_days": 7})
        self.assertEqual(repository.write_count, 1)
        self.assertEqual(publisher.message_count, 1)

    def test_same_fragment_detects_a_write_before_rejection(self) -> None:
        def broken_entry(shape, repository, publisher):
            repository.write(shape)
            return boundary_entry(shape, repository, publisher)

        with self.assertRaises(AssertionError):
            run_documented_fragment(broken_entry, {"retention_days": 0})

    def test_same_fragment_detects_publication_before_rejection(self) -> None:
        def broken_entry(shape, repository, publisher):
            publisher.publish(shape)
            return boundary_entry(shape, repository, publisher)

        with self.assertRaises(AssertionError):
            run_documented_fragment(broken_entry, {"retention_days": 0})


if __name__ == "__main__":
    unittest.main()
