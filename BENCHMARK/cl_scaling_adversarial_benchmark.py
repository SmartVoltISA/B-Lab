#!/usr/bin/env python3
"""CL-SCALING-001 adversarial/diagnostic benchmark.

Tests localization rather than speed alone: isolated invalid edge, broken
cross-partition boundary, and forward/reverse disagreement. No claim is made
about the production CL implementation.
"""
from dataclasses import dataclass


@dataclass
class Case:
    name: str
    edges: list
    partitions: int


def partition(edges, parts):
    buckets = [[] for _ in range(parts)]
    for i, e in enumerate(edges):
        buckets[i % parts].append(e)
    return buckets


def local_ok(n, edges):
    return all(0 <= u < n and 0 <= v < n and u != v for u, v in edges)


def diagnose(n, edges, parts):
    buckets = partition(edges, parts)
    results = []
    for i, bucket in enumerate(buckets):
        results.append((i, local_ok(n, bucket)))
    failures = [i for i, ok in results if not ok]
    return failures, results


def reverse_edges(edges):
    return [(v, u) for u, v in edges]


def run():
    n = 100
    base = [(i, i + 1) for i in range(n - 1)]
    cases = [
        Case("clean", base, 8),
        Case("isolated_bad_edge", base + [(n + 1, 2)], 8),
        Case("cross_partition_bad_edge", base + [(-1, 7)], 8),
    ]
    print("case,forward_failures,reverse_failures,forward_reverse_same")
    for case in cases:
        ff, _ = diagnose(n, case.edges, case.partitions)
        rf, _ = diagnose(n, reverse_edges(case.edges), case.partitions)
        print(f"{case.name},{ff},{rf},{set(ff)==set(rf)}")


if __name__ == "__main__":
    run()
