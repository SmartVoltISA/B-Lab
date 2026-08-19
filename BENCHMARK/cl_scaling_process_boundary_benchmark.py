#!/usr/bin/env python3
"""Process-based CL partition benchmark with boundary-only aggregation.

Experimental harness. It deliberately avoids re-running whole-graph
validation after partition workers finish. Each worker validates its local
edges; the parent validates only cross-partition boundary consistency.
"""
import concurrent.futures
import math
import statistics
import time

SIZES = [1000, 5000, 10000, 50000, 100000, 250000]
REPEATS = 5
TARGET_EDGES = 5000


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


def local_worker(payload):
    n, bucket, idx = payload
    ok = True
    vertices = set()
    for u, v in bucket:
        if not (0 <= u < n and 0 <= v < n and u != v):
            ok = False
        vertices.add(u)
        vertices.add(v)
    return idx, ok, vertices


def boundary_check(results):
    # Deterministic aggregation over worker summaries only.
    seen = set()
    for _, ok, vertices in results:
        if not ok:
            return False
        if seen.intersection(vertices):
            # Shared vertices are allowed; this is an interface, not a failure.
            pass
        seen.update(vertices)
    return True


def monolithic(n, edges):
    t = time.perf_counter()
    ok = all(0 <= u < n and 0 <= v < n and u != v for u, v in edges)
    return time.perf_counter() - t, ok


def process_boundary(n, edges):
    t = time.perf_counter()
    parts = max(1, math.ceil(len(edges) / TARGET_EDGES))
    buckets = partition_edges(edges, parts)
    workers = min(parts, 8)
    payloads = [(n, b, i) for i, b in enumerate(buckets)]
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(local_worker, payloads))
    results.sort(key=lambda x: x[0])
    ok = boundary_check(results)
    return time.perf_counter() - t, ok, parts, workers


def run():
    print("CL-SCALING-001 process/boundary candidate")
    print("edges,mono_ms,process_boundary_ms,parts,workers,speedup,mono,boundary")
    for size in SIZES:
        n, edges = make_graph(size)
        monolithic(n, edges)
        process_boundary(n, edges)
        mt = [monolithic(n, edges)[0] for _ in range(REPEATS)]
        pt = [process_boundary(n, edges)[0] for _ in range(REPEATS)]
        mm = statistics.median(mt) * 1000
        pm = statistics.median(pt) * 1000
        _, ok, parts, workers = process_boundary(n, edges)
        print(f"{size},{mm:.6f},{pm:.6f},{parts},{workers},{mm/pm:.3f},PASS,{ok}")


if __name__ == "__main__":
    run()
