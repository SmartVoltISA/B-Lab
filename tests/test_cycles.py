import pytest

from lab.cycles import detect_period, repeated_states, transitions, validate_binary


def test_detects_alternating_cycle():
    assert detect_period([0, 1, 0, 1, 0, 1]) == 2


def test_detects_constant_binary_state_as_period_one():
    assert detect_period([1, 1, 1, 1]) == 1


def test_non_periodic_prefix_has_no_whole_sequence_period():
    assert detect_period([0, 1, 1, 0, 1]) is None


def test_transitions_are_preserved_in_order():
    assert transitions([0, 1, 0]) == [(0, 1), (1, 0)]


def test_repeated_states_form_minimal_memory_observation():
    assert repeated_states([0, 1, 0, 1, 0]) == {0: 3, 1: 2}


def test_non_binary_data_is_rejected():
    with pytest.raises(ValueError):
        validate_binary([0, 1, 2])
