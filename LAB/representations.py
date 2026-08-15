"""Equivalent structural representations used by EXP-0003."""

from collections.abc import Iterable


def sequence_to_relation(sequence: Iterable[int]) -> set[tuple[int, int]]:
    values = list(sequence)
    if not values or any(v not in (0, 1) for v in values):
        raise ValueError("binary sequence required")
    return set(zip(values, values[1:]))


def relation_to_adjacency(relation: Iterable[tuple[int, int]]) -> list[list[int]]:
    relation_set = set(relation)
    if not relation_set <= {(0, 0), (0, 1), (1, 0), (1, 1)}:
        raise ValueError("binary relation required")
    return [[int((s, t) in relation_set) for t in (0, 1)] for s in (0, 1)]


def adjacency_to_relation(matrix: list[list[int]]) -> set[tuple[int, int]]:
    if matrix != [list(row) for row in matrix] or len(matrix) != 2 or any(len(row) != 2 for row in matrix):
        raise ValueError("2x2 adjacency matrix required")
    if any(value not in (0, 1) for row in matrix for value in row):
        raise ValueError("binary adjacency matrix required")
    return {(s, t) for s in (0, 1) for t in (0, 1) if matrix[s][t] == 1}


def relation_to_edges(relation: Iterable[tuple[int, int]]) -> set[tuple[int, int]]:
    return set(relation)


def edges_to_relation(edges: Iterable[tuple[int, int]]) -> set[tuple[int, int]]:
    return set(edges)


def round_trip(sequence: Iterable[int]) -> dict[str, object]:
    relation = sequence_to_relation(sequence)
    matrix = relation_to_adjacency(relation)
    recovered_relation = adjacency_to_relation(matrix)
    edges = relation_to_edges(recovered_relation)
    final_relation = edges_to_relation(edges)
    return {
        "relation": relation,
        "matrix": matrix,
        "edges": edges,
        "final_relation": final_relation,
        "preserved": relation == final_relation,
    }
