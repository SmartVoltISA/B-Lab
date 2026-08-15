"""Small, deterministic tool for compact binary temporal memory.

The tool keeps one canonical representation: initial state + ordered targets.
Derived history/relations/views should be generated on demand instead of stored twice.
"""

from collections.abc import Iterable


def validate_memory(initial: int, targets: Iterable[int]) -> tuple[int, list[int]]:
    targets = list(targets)
    if initial not in (0, 1):
        raise ValueError("initial must be 0 or 1")
    if any(value not in (0, 1) for value in targets):
        raise ValueError("targets must contain only 0 or 1")
    return initial, targets


def compress(sequence: Iterable[int]) -> tuple[int, list[int]]:
    values = list(sequence)
    if not values:
        raise ValueError("sequence must not be empty")
    validate_memory(values[0], values[1:])
    return values[0], values[1:]


def decompress(initial: int, targets: Iterable[int]) -> list[int]:
    initial, targets = validate_memory(initial, targets)
    return [initial, *targets]


def compression_ratio(sequence: Iterable[int]) -> float:
    values = list(sequence)
    if not values:
        raise ValueError("sequence must not be empty")
    # Logical symbol count, excluding implementation overhead.
    return len(values) / (1 + len(values) - 1)
