import pytest

from LAB.binary_relations import BinaryRelation, adjacency_matrix, validate_state


def test_phase_zero_accepts_only_two_states():
    assert validate_state(0) == 0
    assert validate_state(1) == 1
    with pytest.raises(ValueError):
        validate_state(2)
    with pytest.raises(ValueError):
        validate_state(-1)


def test_minimal_four_directed_relations_are_representable():
    relation = BinaryRelation(frozenset({(0, 0), (0, 1), (1, 0), (1, 1)}))
    assert relation.states == frozenset({0, 1})
    assert relation.matrix() == ((1, 1), (1, 1))


def test_empty_relation_has_no_observed_state():
    relation = BinaryRelation(frozenset())
    assert relation.states == frozenset()
    assert relation.matrix() == ((0, 0), (0, 0))


def test_adjacency_matrix_is_deterministic():
    edges = {(0, 1), (1, 0)}
    assert adjacency_matrix(edges) == ((0, 1), (1, 0))
