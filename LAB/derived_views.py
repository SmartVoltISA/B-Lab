"""Reconstruct structural views from the compact temporal memory."""

from collections.abc import Iterable

from LAB.reconstruct_transitions import reconstruct_transitions


def transitions_from_memory(initial: int, targets: Iterable[int]) -> list[tuple[int, int]]:
    return reconstruct_transitions(initial, targets)


def relation_from_memory(initial: int, targets: Iterable[int]) -> set[tuple[int, int]]:
    return set(transitions_from_memory(initial, targets))


def adjacency_matrix_from_memory(initial: int, targets: Iterable[int]) -> list[list[int]]:
    relation = relation_from_memory(initial, targets)
    matrix = [[0, 0], [0, 0]]
    for source, target in relation:
        matrix[source][target] = 1
    return matrix


def graph_edges_from_memory(initial: int, targets: Iterable[int]) -> set[tuple[int, int]]:
    return relation_from_memory(initial, targets)
