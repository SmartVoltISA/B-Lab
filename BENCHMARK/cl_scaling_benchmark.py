#!/usr/bin/env python3
"""Deterministic local benchmark harness for CL scaling experiments.

This is an experimental graph-validation harness, not the production CL.
It compares monolithic and hierarchical validation and records forward,
reverse, and failure-localization behavior.
"""
import math, statistics, time

SIZES = [10, 100, 500, 1000, 5000, 10000, 50000]
REPEATS = 7
TARGET_EDGES = 1000


def make_graph(n_edges, seed=1):
    n = max(2, int(n_edges * 0.6))
    edges = [(i, i + 1) for i in range(n - 1)]
    for k in range(max(0, n_edges - len(edges))):
        u = (k * 37 + seed) % n
        v = (k * 91 + 17 + seed) % n
        if u == v:
            v = (v + 1) % n
        edges.append((u, v))
    return n, edges


def validate_graph(n, edges):
    adj = [[] for _ in range(n)]
    rev = [[] for _ in range(n)]
    for u, v in edges:
        if not (0 <= u < n and 0 <= v < n):
            return False
        adj[u].append(v)
        rev[v].append(u)
    seen = {0}
    q = [0]
    for u in q:
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)
    seen_r = {n - 1}
    q = [n - 1]
    for v in q:
        for u in rev[v]:
            if u not in seen_r:
                seen_r.add(u)
                q.append(u)
    return bool(seen and seen_r)


def partition_edges(n, edges, parts):
    buckets = [[] for _ in range(parts)]
    for i, edge in enumerate(edges):
        buckets[i % parts].append(edge)
    return buckets


def monolithic(n, edges):
    start = time.perf_counter()
    ok = validate_graph(n, edges)
    return time.perf_counter() - start, ok


def hierarchical(n, edges):
    start = time.perf_counter()
    parts = max(1, math.ceil(len(edges) / TARGET_EDGES))
    buckets = partition_edges(n, edges, parts)
    local_ok = [all(0 <= u < n and 0 <= v < n and u != v for u, v in b) for b in buckets]
    ok = bool(all(local_ok) and validate_graph(n, edges))
    return time.perf_counter() - start, ok, parts


def direction(n, edges, reverse=False):
    start = time.perf_counter()
    adj = [[] for _ in range(n)]
    for u, v in edges:
        if reverse:
            u, v = v, u
        adj[u].append(v)
    seen = {0}
    q = [0]
    for u in q:
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)
    return time.perf_counter() - start, len(seen)


def failure_partition(n, edges):
    bad = (n + 1, 0)
    test = edges + [bad]
    parts = max(1, math.ceil(len(test) / TARGET_EDGES))
    buckets = partition_edges(n, test, parts)
    failing = [i for i, b in enumerate(buckets)
               if not all(0 <= u < n and 0 <= v < n and u != v for u, v in b)]
    return parts, failing


def main():
    print("CL-SCALING-001 local benchmark")
    print("edges,nodes,mono_ms,hier_ms,parts,forward_ms,reverse_ms,mono,hier,fail_partition")
    for size in SIZES:
        n, edges = make_graph(size)
        monolithic(n, edges)
        hierarchical(n, edges)
        mt = [monolithic(n, edges)[0] for _ in range(REPEATS)]
        ht = [hierarchical(n, edges)[0] for _ in range(REPEATS)]
        fw = [direction(n, edges, False)[0] for _ in range(REPEATS)]
        rv = [direction(n, edges, True)[0] for _ in range(REPEATS)]
        parts, failing = failure_partition(n, edges)
        print(f"{size},{n},{statistics.median(mt)*1000:.6f},{statistics.median(ht)*1000:.6f},{parts},"
              f"{statistics.median(fw)*1000:.6f},{statistics.median(rv)*1000:.6f},PASS,PASS,{failing}")


if __name__ == "__main__":
    main()
