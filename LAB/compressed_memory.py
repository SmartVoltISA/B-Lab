"""Compressed temporal representation for contiguous binary histories."""

from collections.abc import Iterable


def compress_sequence(sequence: Iterable[int]) -> tuple[int, tuple[int, ...]]:
    values = list(sequence)
    if not values or any(v not in (0, 1) for v in values):
        raise ValueError("binary sequence required")
    return values[0], tuple(values[1:])


def decompress_sequence(initial: int, targets: Iterable[int]) -> list[int]:
    if initial not in (0, 1):
        raise ValueError("binary initial state required")
    values = list(targets)
    if any(v not in (0, 1) for v in values):
        raise ValueError("binary targets required")
    return [initial, *values]
