"""Minimal binary cycle detection for B-Lab EXP-0002."""

from collections.abc import Iterable


def validate_binary(sequence: Iterable[int]) -> list[int]:
    values = list(sequence)
    if not values or any(value not in (0, 1) for value in values):
        raise ValueError("B-Lab phase 1 accepts only non-empty binary sequences")
    return values


def transitions(sequence: Iterable[int]) -> list[tuple[int, int]]:
    values = validate_binary(sequence)
    return list(zip(values, values[1:]))


def detect_period(sequence: Iterable[int], max_period: int | None = None) -> int | None:
    """Return the shortest repeating period if the whole sequence is periodic."""
    values = validate_binary(sequence)
    limit = len(values) // 2
    if max_period is not None:
        limit = min(limit, max_period)
    for period in range(1, limit + 1):
        if all(values[i] == values[i % period] for i in range(len(values))):
            return period
    return None


def repeated_states(sequence: Iterable[int]) -> dict[int, int]:
    values = validate_binary(sequence)
    return {state: values.count(state) for state in (0, 1)}
