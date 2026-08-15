from LAB.reconstruct_transitions import reconstruct_transitions


def test_reconstructs_sources_from_initial_and_targets():
    assert reconstruct_transitions(0, [1, 0, 1, 0]) == [
        (0, 1), (1, 0), (0, 1), (1, 0)
    ]


def test_both_initial_states():
    assert reconstruct_transitions(0, [0, 1]) == [(0, 0), (0, 1)]
    assert reconstruct_transitions(1, [1, 0]) == [(1, 1), (1, 0)]


def test_zero_self_loop_is_preserved():
    assert reconstruct_transitions(0, [0]) == [(0, 0)]


def test_non_binary_values_rejected():
    try:
        reconstruct_transitions(0, [1, 2])
    except ValueError:
        pass
    else:
        raise AssertionError("non-binary target must be rejected")
