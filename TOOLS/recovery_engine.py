"""B-Lab Recovery Engine v0.1 — read-only, evidence-first recovery primitives.

This tool never modifies a source image/file. It extracts intact fragments and
builds a provenance graph. It deliberately separates exact recovery from
inference: only bytes verified by a parser/signature/checksum are marked exact.

No claim is made that deleted or physically destroyed data can be reconstructed.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Fragment:
    offset: int
    data: bytes
    source_sha256: str
    confidence: float = 1.0
    evidence: tuple[str, ...] = ()

    @property
    def end(self) -> int:
        return self.offset + len(self.data)


@dataclass(frozen=True)
class RecoveryReport:
    source_size: int
    recovered_bytes: int
    exact_bytes: int
    inferred_bytes: int
    fragments: tuple[Fragment, ...]
    sha256: str

    @property
    def exact_ratio(self) -> float:
        return self.exact_bytes / self.source_size if self.source_size else 1.0

    @property
    def recovered_ratio(self) -> float:
        return self.recovered_bytes / self.source_size if self.source_size else 1.0


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def scan_fragments(source: bytes, magic: bytes) -> list[Fragment]:
    """Find intact occurrences of a known signature without modifying source."""
    if not magic:
        raise ValueError("magic signature must not be empty")
    result: list[Fragment] = []
    start = 0
    source_digest = sha256(source)
    while True:
        pos = source.find(magic, start)
        if pos < 0:
            break
        result.append(Fragment(pos, source[pos:pos + len(magic)], source_digest,
                               confidence=1.0, evidence=("signature_match",)))
        start = pos + 1
    return result


def build_report(source: bytes, fragments: list[Fragment]) -> RecoveryReport:
    # Merge only non-overlapping, evidence-backed fragments. Unknown gaps are
    # never silently counted as recovered data.
    ordered = sorted(fragments, key=lambda f: f.offset)
    accepted: list[Fragment] = []
    covered = 0
    exact = 0
    for f in ordered:
        if f.offset < 0 or f.end > len(source):
            raise ValueError("fragment outside source bounds")
        if f.source_sha256 != sha256(source):
            raise ValueError("fragment provenance does not match source")
        if accepted and f.offset < accepted[-1].end:
            continue
        accepted.append(f)
        covered += len(f.data)
        if f.confidence >= 1.0:
            exact += len(f.data)
    inferred = max(0, covered - exact)
    return RecoveryReport(len(source), covered, exact, inferred,
                          tuple(accepted), sha256(source))


def reconstruct(report: RecoveryReport) -> bytes:
    """Reconstruct only verified fragments; unknown gaps are zero-filled.

    This is intentionally NOT presented as original data. Callers must inspect
    the report's coverage/confidence before treating the result as recovered.
    """
    out = bytearray(report.source_size)
    for f in report.fragments:
        out[f.offset:f.end] = f.data
    return bytes(out)
