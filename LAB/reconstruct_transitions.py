"""Reconstruct transition pairs from initial state and ordered targets."""

from collections.abc import Iterable


def reconstruct_transitions(initial: int, targets: Iterable[int]) -> list[tuple[int, int]]:
    if initial not in (0, 1):
        raise ValueError("binary initial state required")
    values = list(targets)
    if any(v not in (0, 1) for v in values):
        raise ValueError("binary targets required")
    source = initial
    transitions: list[tuple[int, int]] = []
    for target in values:
        transitions.append((source, target))
        source = target
    return transitions
