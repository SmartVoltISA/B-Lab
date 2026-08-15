from LAB.temporal_memory import temporal_record, temporal_signature


def test_temporal_record_keeps_observation_index():
    assert temporal_record([0, 1, 0]) == [(0, 0, 1), (1, 1, 0)]


def test_same_relation_different_history_has_different_temporal_signature():
    first = temporal_signature([0, 1, 0])
    second = temporal_signature([0, 1, 0, 1, 0])
    assert first != second


def test_temporal_layer_does_not_add_a_third_state():
    record = temporal_record([0, 1, 0, 1])
    assert {source for _, source, _ in record} <= {0, 1}
    assert {target for _, _, target in record} <= {0, 1}


def test_zero_transitions_remain_explicit():
    assert temporal_record([0, 0, 1]) == [(0, 0, 0), (1, 0, 1)]
