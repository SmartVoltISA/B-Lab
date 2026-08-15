from LAB.representations import round_trip


def test_zero_one_cycle_survives_all_representations():
    result = round_trip([0, 1, 0])
    assert result["relation"] == {(0, 1), (1, 0)}
    assert result["matrix"] == [[0, 1], [1, 0]]
    assert result["edges"] == {(0, 1), (1, 0)}
    assert result["final_relation"] == result["relation"]
    assert result["preserved"] is True


def test_zero_self_loop_is_not_lost():
    result = round_trip([0, 0])
    assert result["relation"] == {(0, 0)}
    assert result["matrix"] == [[1, 0], [0, 0]]
    assert result["final_relation"] == {(0, 0)}
    assert result["preserved"] is True


def test_one_self_loop_is_distinct_from_zero_self_loop():
    zero = round_trip([0, 0])
    one = round_trip([1, 1])
    assert zero["relation"] != one["relation"]
    assert zero["matrix"] != one["matrix"]
