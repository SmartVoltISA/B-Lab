from TOOLS.bitpack import pack_memory, unpack_memory
from TOOLS.compression_tool import compress, decompress


def test_bitpack_round_trip():
    sequence = [0, 1, 0, 1, 0, 0, 1, 1, 1]
    memory = compress(sequence)
    payload = pack_memory(*memory)
    assert decompress(*unpack_memory(payload, len(sequence))) == sequence


def test_bitpack_reduces_large_binary_sequence():
    sequence = [0, 1] * 5000
    memory = compress(sequence)
    payload = pack_memory(*memory)
    assert len(payload) < len(sequence)


def test_zero_self_loop_survives_bitpack():
    sequence = [0, 0, 1, 0]
    memory = compress(sequence)
    payload = pack_memory(*memory)
    assert decompress(*unpack_memory(payload, len(sequence))) == sequence
