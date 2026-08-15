"""Minimal binary relation primitives for B-Lab Phase 0."""

from __future__ import annotations

from dataclasses import dataclass

State = int
Edge = tuple[State, State]

VALID_STATES = frozenset({0, 1})


def validate_state(state: State) -> State:
    if state not in VALID_STATES:
        raise ValueError(f"B-Lab Phase 0 accepts only 0 or 1, got {state!r}")
    return state


def validate_edge(edge: Edge) -> Edge:
    a, b = edge
    return validate_state(a), validate_state(b)


def adjacency_matrix(edges: set[Edge] | list[Edge] | tuple[Edge, ...]) -> tuple[tuple[int, int], tuple[int, int]]:
    matrix = [[0, 0], [0, 0]]
    for edge in edges:
        a, b = validate_edge(edge)
        matrix[a][b] = 1
    return tuple(tuple(row) for row in matrix)


@dataclass(frozen=True)
class BinaryRelation:
    edges: frozenset[Edge]

    def __post_init__(self) -> None:
        for edge in self.edges:
            validate_edge(edge)

    @property
    def states(self) -> frozenset[State]:
        return frozenset(s for edge in self.edges for s in edge)

    def matrix(self) -> tuple[tuple[int, int], tuple[int, int]]:
        return adjacency_matrix(self.edges)
