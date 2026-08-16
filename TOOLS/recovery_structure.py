"""B-Lab Recovery Structure v0.1 — parser, checksum and redundancy evidence.

This module handles a deliberately simple framed record format for laboratory
validation. It does not claim to recover arbitrary real-world file formats.
Only records with valid framing and SHA-256 are accepted as exact. When the
same logical record exists more than once, an intact duplicate can provide
redundancy-backed recovery evidence.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass

MAGIC = b"BLAB1"
HEADER_SIZE = len(MAGIC) + 2 + 4
DIGEST_SIZE = 32


@dataclass(frozen=True)
class Record:
    record_id: int
    payload: bytes
    offset: int
    checksum_valid: bool
    evidence: tuple[str, ...]


def checksum(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def encode_record(record_id: int, payload: bytes) -> bytes:
    if not 0 <= record_id <= 0xFFFF:
        raise ValueError("record_id out of range")
    if len(payload) > 0xFFFFFFFF:
        raise ValueError("payload too large")
    return MAGIC + record_id.to_bytes(2, "big") + len(payload).to_bytes(4, "big") + payload + checksum(payload)


def parse_records(source: bytes) -> list[Record]:
    """Parse intact framed records; malformed/corrupt records are skipped."""
    records: list[Record] = []
    pos = 0
    while pos + HEADER_SIZE + DIGEST_SIZE <= len(source):
        start = source.find(MAGIC, pos)
        if start < 0 or start + HEADER_SIZE + DIGEST_SIZE > len(source):
            break
        record_id = int.from_bytes(source[start + len(MAGIC):start + len(MAGIC) + 2], "big")
        length = int.from_bytes(source[start + len(MAGIC) + 2:start + HEADER_SIZE], "big")
        end = start + HEADER_SIZE + length + DIGEST_SIZE
        if end > len(source):
            pos = start + 1
            continue
        payload_start = start + HEADER_SIZE
        payload = source[payload_start:payload_start + length]
        expected = source[payload_start + length:end]
        valid = checksum(payload) == expected
        if valid:
            records.append(Record(record_id, payload, start, True, ("frame_match", "sha256_match")))
        pos = end if valid else start + 1
    return records


def recover_by_redundancy(records: list[Record]) -> dict[int, Record]:
    """Choose one checksum-valid copy per logical record ID.

    This is evidence-backed selection, not invention: no ID is created unless
    at least one intact checksum-valid record exists.
    """
    chosen: dict[int, Record] = {}
    for record in records:
        if record.checksum_valid and record.record_id not in chosen:
            chosen[record.record_id] = record
    return chosen
