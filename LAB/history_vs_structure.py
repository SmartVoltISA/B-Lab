"""Compare temporal history with the relation it induces."""

from collections.abc import Iterable

from LAB.comparator import relation_from_transitions


def structural_relation(sequence: Iterable[int]) -> set[tuple[int, int]]:
    return relation_from_transitions(sequence)


def same_structure(first: Iterable[int], second: Iterable[int]) -> bool:
    return structural_relation(first) == structural_relation(second)


def history_is_distinct(first: Iterable[int], second: Iterable[int]) -> bool:
    return list(first) != list(second)
