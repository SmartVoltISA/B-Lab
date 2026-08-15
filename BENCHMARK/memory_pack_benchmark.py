"""Safe end-to-end memory-pack benchmark.

This benchmark never mutates source files. It creates temporary in-memory packs,
round-trips them, and reports physical sizes plus node/edge preservation.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from TOOLS.graph_memory import open_graph, seal
from TOOLS.memory_engine import MemoryTier, load, store


def file_corpus(root: Path) -> bytes:
    parts = []
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts:
            continue
        parts.append(path.read_bytes())
    return b"\n".join(parts)


def graph_case() -> tuple[dict[str, dict], list[tuple[str, str, str]]]:
    nodes = {f"N{i}": {"tier": "long_term", "i": i} for i in range(100)}
    edges = [(f"N{i}", f"N{i+1}", "next") for i in range(99)]
    edges += [(f"N{i}", f"N{(i + 7) % 100}", "cross") for i in range(100)]
    return nodes, edges


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    corpus = file_corpus(root)
    packed = store(corpus, MemoryTier.LONG_TERM)
    _, restored = load(packed)
    assert restored == corpus

    nodes, edges = graph_case()
    graph_blob = seal(nodes, edges)
    restored_nodes, restored_edges = open_graph(graph_blob)
    assert restored_nodes == nodes
    assert restored_edges == edges

    print("MEMORY PACK BENCHMARK")
    print(f"corpus_raw_bytes={len(corpus)}")
    print(f"corpus_pack_bytes={len(packed)}")
    print(f"corpus_sha256={hashlib.sha256(corpus).hexdigest()}")
    print(f"corpus_roundtrip=PASS")
    print(f"graph_raw_nodes={len(nodes)}")
    print(f"graph_raw_edges={len(edges)}")
    print(f"graph_pack_bytes={len(graph_blob)}")
    print(f"graph_roundtrip=PASS")
    print(f"graph_nodes_preserved={len(restored_nodes) == len(nodes)}")
    print(f"graph_edges_preserved={len(restored_edges) == len(edges)}")


if __name__ == "__main__":
    main()
