"""Minimal temporal layer for B-Lab."""

from collections.abc import Iterable


def temporal_record(sequence: Iterable[int]) -> list[tuple[int, int, int]]:
    values = list(sequence)
    if not values or any(v not in (0, 1) for v in values):
        raise ValueError("binary sequence required")
    return [(t, values[t], values[t + 1]) for t in range(len(values) - 1)]


def temporal_signature(sequence: Iterable[int]) -> tuple[tuple[int, int, int], ...]:
    return tuple(temporal_record(sequence))


def reconstruct_sequence(record: Iterable[tuple[int, int, int]]) -> list[int]:
    events = list(record)
    if not events:
        raise ValueError("non-empty temporal record required")
    expected_t = 0
    first_source = events[0][1]
    if first_source not in (0, 1):
        raise ValueError("binary source required")
    result = [first_source]
    for t, source, target in events:
        if t != expected_t or source not in (0, 1) or target not in (0, 1):
            raise ValueError("invalid temporal record")
        if source != result[-1]:
            raise ValueError("discontinuous temporal record")
        result.append(target)
        expected_t += 1
    return result
