"""B-Lab Recovery Organ v0.1.

Read-only orchestration primitives for recovery research. The organ never
writes to the source image/device. It works on an image/byte buffer and emits
an evidence graph plus a conservative recovery report.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Evidence:
    kind: str
    start: int
    end: int
    confidence: float
    reason: str
    sha256: str | None = None


@dataclass
class RecoveryGraph:
    nodes: list[Evidence] = field(default_factory=list)
    edges: list[tuple[int, int, str]] = field(default_factory=list)

    def add(self, evidence: Evidence) -> int:
        idx = len(self.nodes)
        self.nodes.append(evidence)
        return idx


def source_fingerprint(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def scan_signatures(data: bytes, signatures: dict[str, bytes]) -> list[Evidence]:
    """Find byte signatures without claiming that a complete file was found."""
    found: list[Evidence] = []
    for kind, sig in signatures.items():
        if not sig:
            continue
        start = 0
        while True:
            pos = data.find(sig, start)
            if pos < 0:
                break
            found.append(Evidence(kind, pos, pos + len(sig), 0.50, "signature_match"))
            start = pos + 1
    return found


def build_evidence_graph(evidence: list[Evidence], max_gap: int = 4096) -> RecoveryGraph:
    graph = RecoveryGraph()
    indexed = sorted(evidence, key=lambda e: (e.start, e.end, e.kind))
    for item in indexed:
        graph.add(item)
    for i, left in enumerate(graph.nodes):
        for j in range(i + 1, len(graph.nodes)):
            right = graph.nodes[j]
            if 0 <= right.start - left.end <= max_gap:
                graph.edges.append((i, j, "spatial_proximity"))
            if right.start < left.end and right.end > left.start:
                graph.edges.append((i, j, "overlap"))
    return graph


def trust_score(evidence: Evidence, *, checksum_ok: bool = False,
                parser_ok: bool = False, redundant_copy: bool = False) -> float:
    """Conservative additive score; it is evidence strength, not truth probability."""
    score = 0.20
    if evidence.kind:
        score += 0.10
    if checksum_ok:
        score += 0.35
    if parser_ok:
        score += 0.20
    if redundant_copy:
        score += 0.10
    return min(score, 0.95)


def recovery_report(source: bytes, graph: RecoveryGraph) -> dict:
    exact = [n for n in graph.nodes if n.confidence >= 0.95]
    covered = set()
    for n in exact:
        covered.update(range(n.start, min(n.end, len(source))))
    return {
        "source_sha256": source_fingerprint(source),
        "source_bytes": len(source),
        "evidence_nodes": len(graph.nodes),
        "evidence_edges": len(graph.edges),
        "exact_evidence_bytes": len(covered),
        "exact_coverage": len(covered) / len(source) if source else 1.0,
        "full_recovery": len(covered) == len(source),
        "claim": "exact_only_when_all_bytes_are_evidenced",
    }
