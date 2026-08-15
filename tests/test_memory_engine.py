from TOOLS.memory_engine import (
    MemoryTier,
    compress_text,
    decompress_text,
    load,
    pack_bits,
    store,
    unpack_bits,
)


def test_bit_round_trip_and_8x_logical_reduction():
    states = [i % 2 for i in range(1000)]
    packed = pack_bits(states)
    assert len(packed) == 125
    assert unpack_bits(packed, len(states)) == states


def test_text_round_trip():
    text = "Связь → память → структура. " * 100
    blob = compress_text(text, MemoryTier.LONG_TERM)
    assert decompress_text(blob) == text


def test_rle_selected_for_repetitive_data():
    data = b"A" * 1000
    blob = store(data, MemoryTier.TEMPORARY)
    tier, restored = load(blob)
    assert tier is MemoryTier.TEMPORARY
    assert restored == data


def test_tiers_are_preserved():
    data = b"active data"
    for tier in MemoryTier:
        tier2, restored = load(store(data, tier))
        assert tier2 is tier
        assert restored == data
