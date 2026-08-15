from TOOLS.recovery_engine import build_report, reconstruct, scan_fragments


def test_exact_fragment_recovery_and_provenance():
    source = b"HEADER" + b"X" * 32 + b"FOOTER"
    fragments = scan_fragments(source, b"HEADER") + scan_fragments(source, b"FOOTER")
    report = build_report(source, fragments)
    assert report.source_size == len(source)
    assert report.exact_bytes == 12
    assert report.inferred_bytes == 0
    assert report.recovered_ratio == 12 / len(source)
    rebuilt = reconstruct(report)
    assert rebuilt[:6] == b"HEADER"
    assert rebuilt[-6:] == b"FOOTER"


def test_unknown_gap_is_not_claimed_as_recovered():
    source = b"AAA" + b"UNKNOWN" + b"BBB"
    fragments = scan_fragments(source, b"AAA") + scan_fragments(source, b"BBB")
    report = build_report(source, fragments)
    assert report.exact_bytes == 6
    assert report.recovered_bytes == 6
    assert report.recovered_ratio < 1.0


def test_source_modification_after_scan_invalidates_provenance():
    source = b"MAGIC-DATA"
    fragments = scan_fragments(source, b"MAGIC")
    changed = b"MAGIX-DATA"
    try:
        build_report(changed, fragments)
    except ValueError as exc:
        assert "provenance" in str(exc)
    else:
        raise AssertionError("changed source must not accept stale recovery evidence")
