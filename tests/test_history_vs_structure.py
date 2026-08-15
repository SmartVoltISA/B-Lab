from LAB.history_vs_structure import history_is_distinct, same_structure


def test_different_histories_can_have_same_relation():
    first = [0, 1, 0]
    second = [1, 0, 1]
    assert history_is_distinct(first, second)
    assert same_structure(first, second)


def test_repetition_can_change_history_without_changing_relation():
    first = [0, 1, 0]
    second = [0, 1, 0, 1, 0]
    assert history_is_distinct(first, second)
    assert same_structure(first, second)


def test_zero_self_loop_remains_structurally_distinct():
    assert not same_structure([0, 0], [1, 1])


def test_zero_is_not_erased_from_structure():
    assert same_structure([0, 0, 1], [0, 1, 0, 1]) is True
