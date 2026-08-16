"""Conservative filesystem metadata analyzer.

This first version analyzes a supplied metadata table rather than guessing a
filesystem. Unknown structures are reported as unknown.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FileExtent:
    path: str
    start: int
    length: int
    allocated: bool


def analyze_extents(extents: list[dict]) -> dict:
    parsed: list[FileExtent] = []
    for item in extents:
        path = str(item.get("path", ""))
        start = int(item.get("start", 0))
        length = int(item.get("length", 0))
        allocated = bool(item.get("allocated", False))
        if not path or start < 0 or length < 0:
            continue
        parsed.append(FileExtent(path, start, length, allocated))
    return {
        "files": len(parsed),
        "allocated": sum(x.allocated for x in parsed),
        "unallocated": sum(not x.allocated for x in parsed),
        "extents": [x.__dict__ for x in parsed],
        "claim": "metadata_only_no_filesystem_repair",
    }
