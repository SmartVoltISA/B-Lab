from LAB.derived_views import (
    adjacency_matrix_from_memory,
    graph_edges_from_memory,
    relation_from_memory,
    transitions_from_memory,
)


def test_all_views_derive_from_compact_memory():
    memory = (0, [1, 0, 1, 0])
    assert transitions_from_memory(*memory) == [
        (0, 1), (1, 0), (0, 1), (1, 0)
    ]
    assert relation_from_memory(*memory) == {(0, 1), (1, 0)}
    assert graph_edges_from_memory(*memory) == {(0, 1), (1, 0)}
    assert adjacency_matrix_from_memory(*memory) == [[0, 1], [1, 0]]


def test_zero_self_loop_survives_all_views():
    memory = (0, [0, 1])
    assert relation_from_memory(*memory) == {(0, 0), (0, 1)}
    assert adjacency_matrix_from_memory(*memory) == [[1, 1], [0, 0]]
    assert graph_edges_from_memory(*memory) == {(0, 0), (0, 1)}
