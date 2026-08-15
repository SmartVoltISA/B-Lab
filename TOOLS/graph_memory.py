"""Lossless canonical graph memory with integrity checks.

Nodes and edges are canonical data. Views are never treated as the source of truth.
A corrupted record fails closed; it is never presented as a valid graph.

Important: node identifiers may be canonicalized for deterministic storage, but
edge ORDER is semantic history and therefore must be preserved exactly.
"""

from __future__ import annotations

import hashlib
import json
import zlib
from dataclasses import dataclass

MAGIC = b"BLG1"


def _canonical(nodes: dict[str, dict], edges: list[tuple[str, str, str]]) -> bytes:
    # Node map order is canonicalized because node order is not semantic here.
    # Edge order is deliberately NOT sorted: it is part of the historical
    # structure and must survive pack -> unpack exactly.
    obj = {
        "nodes": [[k, nodes[k]] for k in sorted(nodes)],
        "edges": [list(e) for e in edges],
    }
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


@dataclass(frozen=True)
class GraphRecord:
    payload: bytes
    digest: bytes
    compressed: bool

    @property
    def stored_size(self) -> int:
        return len(MAGIC) + 1 + 32 + 4 + len(self.payload)


def seal(nodes: dict[str, dict], edges: list[tuple[str, str, str]]) -> bytes:
    for src, dst, _kind in edges:
        if src not in nodes or dst not in nodes:
            raise ValueError("edge references a missing node")
    raw = _canonical(nodes, edges)
    compressed = zlib.compress(raw, 9)
    use_compressed = len(compressed) < len(raw)
    payload = compressed if use_compressed else raw
    return MAGIC + bytes((1 if use_compressed else 0,)) + hashlib.sha256(raw).digest() + len(raw).to_bytes(4, "big") + payload


def open_graph(blob: bytes) -> tuple[dict[str, dict], list[tuple[str, str, str]]]:
    if len(blob) < 41 or blob[:4] != MAGIC:
        raise ValueError("invalid graph record")
    flag = blob[4]
    if flag not in (0, 1):
        raise ValueError("graph integrity check failed: invalid compression flag")
    expected = blob[5:37]
    raw_len = int.from_bytes(blob[37:41], "big")
    payload = blob[41:]
    try:
        raw = zlib.decompress(payload) if flag else payload
    except zlib.error as exc:
        raise ValueError("graph integrity check failed: corrupt compressed payload") from exc
    if len(raw) != raw_len or hashlib.sha256(raw).digest() != expected:
        raise ValueError("graph integrity check failed")
    try:
        obj = json.loads(raw.decode("utf-8"))
        nodes = {k: v for k, v in obj["nodes"]}
        edges = [tuple(e) for e in obj["edges"]]
    except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise ValueError("graph integrity check failed: invalid canonical payload") from exc
    for src, dst, _kind in edges:
        if src not in nodes or dst not in nodes:
            raise ValueError("graph integrity check failed: dangling edge")
    return nodes, edges
