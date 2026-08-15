import pytest

from TOOLS.compression_tool import compress, compression_ratio, decompress


def test_round_trip():
    sequence = [0, 1, 0, 1, 0]
    memory = compress(sequence)
    assert memory == (0, [1, 0, 1, 0])
    assert decompress(*memory) == sequence


def test_zero_self_loop_is_preserved():
    memory = compress([0, 0, 1])
    assert memory == (0, [0, 1])
    assert decompress(*memory) == [0, 0, 1]


def test_invalid_values_are_rejected():
    with pytest.raises(ValueError):
        compress([0, 2, 1])


def test_empty_sequence_is_rejected():
    with pytest.raises(ValueError):
        compress([])


def test_logical_symbol_count_is_not_misrepresented_as_physical_bytes():
    assert compression_ratio([0, 1, 0, 1]) == 1.0
