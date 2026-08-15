from LAB.compressed_memory import compress_sequence, decompress_sequence


def test_round_trip():
    for sequence in ([0, 1, 0, 1, 0], [1, 1, 0], [0, 0, 1]):
        initial, targets = compress_sequence(sequence)
        assert decompress_sequence(initial, targets) == list(sequence)


def test_zero_self_loop_remains_explicit():
    initial, targets = compress_sequence([0, 0, 1])
    assert initial == 0
    assert targets == (0, 1)


def test_empty_sequence_is_rejected():
    try:
        compress_sequence([])
    except ValueError:
        pass
    else:
        raise AssertionError("empty sequence must be rejected")


def test_non_binary_values_are_rejected():
    try:
        compress_sequence([0, 2, 1])
    except ValueError:
        pass
    else:
        raise AssertionError("non-binary state must be rejected")
