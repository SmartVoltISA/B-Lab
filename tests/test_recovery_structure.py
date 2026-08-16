from TOOLS.recovery_structure import encode_record, parse_records, recover_by_redundancy


def test_parser_accepts_only_checksum_valid_records():
    source = encode_record(1, b"alpha") + encode_record(2, b"beta")
    damaged = bytearray(source)
    # Damage payload of the second record; its checksum must reject it.
    second = source.index(b"beta")
    damaged[second] ^= 0xFF
    records = parse_records(bytes(damaged))
    assert [r.record_id for r in records] == [1]
    assert all(r.checksum_valid for r in records)


def test_redundancy_recovers_intact_duplicate():
    source = encode_record(7, b"original")
    damaged = bytearray(encode_record(7, b"corrupt"))
    damaged[12] ^= 0x01
    records = parse_records(bytes(damaged) + source)
    recovered = recover_by_redundancy(records)
    assert recovered[7].payload == b"original"


def test_no_evidence_means_no_recovery():
    damaged = bytearray(encode_record(9, b"lost"))
    damaged[-1] ^= 0xAA
    assert recover_by_redundancy(parse_records(bytes(damaged))) == {}
