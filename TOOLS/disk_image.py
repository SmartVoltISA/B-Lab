"""Read-only disk-image abstraction for Recovery Organ.

No device writing is performed here. The production adapter must open a
forensic image or block device read-only and record a source fingerprint.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class ImageInfo:
    source: str
    size: int
    sha256: str
    read_only: bool = True


def fingerprint_bytes(source: bytes, label: str = "memory-image") -> ImageInfo:
    return ImageInfo(label, len(source), hashlib.sha256(source).hexdigest(), True)


def chunk_ranges(size: int, block_size: int = 4096) -> list[tuple[int, int]]:
    if size < 0 or block_size <= 0:
        raise ValueError("invalid image size or block size")
    return [(start, min(start + block_size, size)) for start in range(0, size, block_size)]
