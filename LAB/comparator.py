"""Structural comparator for binary relations."""

from collections.abc import Iterable

PAIR_SET = {(0, 0), (0, 1), (1, 0), (1, 1)}


def relation_from_transitions(sequence: Iterable[int]) -> set[tuple[int, int]]:
    values = list(sequence)
    if not values or any(v not in (0, 1) for v in values):
        raise ValueError("binary sequence required")
    return set(zip(values, values[1:]))


def compare_relations(observed: Iterable[tuple[int, int]], model: Iterable[tuple[int, int]]) -> str:
    observed_set = set(observed)
    model_set = set(model)
    if not observed_set <= PAIR_SET or not model_set <= PAIR_SET:
        return "UNRESOLVED"
    if observed_set == model_set:
        return "MATCH"
    if observed_set < model_set:
        return "PARTIAL_MATCH"
    if observed_set - model_set:
        return "DIFFERENCE"
    return "UNRESOLVED"


def adjacency_matrix(relation: Iterable[tuple[int, int]]) -> list[list[int]]:
    relation_set = set(relation)
    if not relation_set <= PAIR_SET:
        raise ValueError("binary relation required")
    return [[int((source, target) in relation_set) for target in (0, 1)] for source in (0, 1)]
