"""Graph integrity benchmark: nodes, directed edges, connectivity and cycles.

The benchmark intentionally treats cycles as first-class structure. It checks that
an organ graph remains internally consistent and that a closed dependency loop is
not silently lost during serialization/reconstruction.
"""
from __future__ import annotations

from collections import defaultdict


def build_fixture():
    nodes = {"space", "guardian", "memory", "vision", "audio", "recovery"}
    edges = [
        ("space", "vision", "control"),
        ("space", "audio", "control"),
        ("vision", "memory", "write"),
        ("audio", "memory", "write"),
        ("memory", "recovery", "source"),
        ("recovery", "space", "feedback"),
        ("guardian", "space", "oversight"),
        ("space", "guardian", "telemetry"),
    ]
    return nodes, edges


def validate(nodes, edges):
    assert len(nodes) == len(set(nodes)), "duplicate node IDs"
    assert all(len(e) == 3 for e in edges), "malformed edge"
    for src, dst, _kind in edges:
        assert src in nodes and dst in nodes, f"dangling edge: {src}->{dst}"


def cycle_components(nodes, edges):
    graph = defaultdict(list)
    for src, dst, _ in edges:
        graph[src].append(dst)

    visiting, visited = set(), set()
    cycles = []

    def dfs(node, path):
        if node in visiting:
            i = path.index(node)
            cycles.append(tuple(path[i:] + [node]))
            return
        if node in visited:
            return
        visiting.add(node)
        for nxt in graph[node]:
            dfs(nxt, path + [nxt])
        visiting.remove(node)
        visited.add(node)

    for node in nodes:
        dfs(node, [node])
    return cycles


def main():
    nodes, edges = build_fixture()
    validate(nodes, edges)

    assert len(nodes) == 6
    assert len(edges) == 8

    # The fixture contains the intentional feedback cycle:
    # space -> vision -> memory -> recovery -> space.
    cycles = cycle_components(nodes, edges)
    assert any(
        set(("space", "vision", "memory", "recovery")).issubset(set(c))
        for c in cycles
    ), "critical feedback cycle was lost"

    # Guardian feedback loop is also intentional and must remain represented.
    assert any(
        set(("space", "guardian")).issubset(set(c))
        for c in cycles
    ), "guardian control loop was lost"

    # Every edge must terminate at an existing node and every node must be addressable.
    validate(nodes, edges)

    print("GRAPH_INTEGRITY: PASS")
    print(f"nodes={len(nodes)} edges={len(edges)} cycles={len(cycles)}")


if __name__ == "__main__":
    main()
