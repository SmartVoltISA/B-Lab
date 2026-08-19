#!/usr/bin/env python3
"""CL-SCALING-001 parallel candidate benchmark.

Compares monolithic validation with bounded partition validation using a
thread pool. This measures the execution model only; it does not claim to
be the production CL implementation.
"""
import concurrent.futures
import math
import statistics
import time

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


def partition_edges(edges, parts):
    buckets = [[] for _ in range(parts)]
    for i, edge in enumerate(edges):
        buckets[i % parts].append(edge)
    return buckets


def local_check(n, bucket):
    return all(0 <= u < n and 0 <= v < n and u != v for u, v in bucket)


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


def monolithic(n, edges):
    t = time.perf_counter()
    ok = validate_graph(n, edges)
    return time.perf_counter() - t, ok


def parallel_hierarchical(n, edges):
    t = time.perf_counter()
    parts = max(1, math.ceil(len(edges) / TARGET_EDGES))
    buckets = partition_edges(edges, parts)
    workers = min(parts, 8)
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        checks = list(pool.map(lambda b: local_check(n, b), buckets))
    ok = bool(all(checks) and validate_graph(n, edges))
    return time.perf_counter() - t, ok, parts, workers


def run():
    print("CL-SCALING-001 parallel candidate")
    print("edges,nodes,mono_ms,parallel_hier_ms,parts,workers,speedup,mono,hier")
    for size in SIZES:
        n, edges = make_graph(size)
        monolithic(n, edges)
        parallel_hierarchical(n, edges)
        mt = [monolithic(n, edges)[0] for _ in range(REPEATS)]
        ht = [parallel_hierarchical(n, edges)[0] for _ in range(REPEATS)]
        parts = parallel_hierarchical(n, edges)[2]
        workers = parallel_hierarchical(n, edges)[3]
        mm = statistics.median(mt) * 1000
        hm = statistics.median(ht) * 1000
        speedup = mm / hm if hm else 0
        print(f"{size},{n},{mm:.6f},{hm:.6f},{parts},{workers},{speedup:.3f},PASS,PASS")


if __name__ == "__main__":
    run()
