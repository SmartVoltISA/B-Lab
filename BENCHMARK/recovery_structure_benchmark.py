"""EXP-0016: structural recovery with parser, checksum and redundancy."""
from TOOLS.recovery_structure import encode_record, parse_records, recover_by_redundancy


def run() -> None:
    records = [(1, b"HEADER"), (2, b"IMAGE-BLOCK-A"), (3, b"IMAGE-BLOCK-B"), (4, b"FOOTER")]
    intact = b"".join(encode_record(i, p) for i, p in records)
    duplicate = encode_record(3, records[2][1])

    # First copy of record 3 is corrupted; an intact duplicate remains later.
    source = bytearray(intact + duplicate)
    marker = source.index(b"IMAGE-BLOCK-B")
    source[marker] ^= 0x01
    damaged = bytes(source)

    parsed = parse_records(damaged)
    recovered = recover_by_redundancy(parsed)

    assert recovered[1].payload == b"HEADER"
    assert recovered[2].payload == b"IMAGE-BLOCK-A"
    assert recovered[3].payload == b"IMAGE-BLOCK-B"
    assert recovered[4].payload == b"FOOTER"
    assert len(recovered) == 4

    # Control: corrupt every copy of record 2. No checksum-valid evidence remains.
    fully_corrupt = bytearray(intact + duplicate)
    marker = fully_corrupt.index(b"IMAGE-BLOCK-A")
    fully_corrupt[marker] ^= 0x01
    recovered_without_2 = recover_by_redundancy(parse_records(bytes(fully_corrupt)))
    assert 2 not in recovered_without_2

    print("RECOVERY STRUCTURE BENCHMARK: PASS")
    print(f"source_bytes={len(damaged)}")
    print(f"parsed_valid_records={len(parsed)}")
    print(f"recovered_logical_records={len(recovered)}")
    print("checksum_validation=true")
    print("redundancy_recovery=true")
    print("full_loss_recovery=false")


if __name__ == "__main__":
    run()
