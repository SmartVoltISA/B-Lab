"""Minimal temporal layer for B-Lab."""

from collections.abc import Iterable


def temporal_record(sequence: Iterable[int]) -> list[tuple[int, int, int]]:
    values = list(sequence)
    if not values or any(v not in (0, 1) for v in values):
        raise ValueError("binary sequence required")
    return [(t, values[t], values[t + 1]) for t in range(len(values) - 1)]


def temporal_signature(sequence: Iterable[int]) -> tuple[tuple[int, int, int], ...]:
    return tuple(temporal_record(sequence))
