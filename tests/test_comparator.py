from LAB.comparator import adjacency_matrix, compare_relations, relation_from_transitions


def test_relation_is_derived_from_observed_transitions():
    assert relation_from_transitions([0, 1, 0]) == {(0, 1), (1, 0)}


def test_zero_self_loop_is_preserved():
    assert relation_from_transitions([0, 0]) == {(0, 0)}


def test_zero_and_one_are_distinct_states():
    assert relation_from_transitions([0, 1]) == {(0, 1)}
    assert relation_from_transitions([1, 0]) == {(1, 0)}


def test_exact_relation_is_match():
    model = {(0, 1), (1, 0)}
    assert compare_relations(model, model) == "MATCH"


def test_subset_is_partial_match():
    observed = {(0, 1)}
    model = {(0, 1), (1, 0)}
    assert compare_relations(observed, model) == "PARTIAL_MATCH"


def test_unexpected_pair_is_difference():
    observed = {(0, 1), (1, 1)}
    model = {(0, 1)}
    assert compare_relations(observed, model) == "DIFFERENCE"


def test_adjacency_matrix_is_deterministic():
    assert adjacency_matrix({(0, 1), (1, 0)}) == [[0, 1], [1, 0]]


def test_zero_row_and_column_are_not_lost():
    assert adjacency_matrix({(0, 0)}) == [[1, 0], [0, 0]]
