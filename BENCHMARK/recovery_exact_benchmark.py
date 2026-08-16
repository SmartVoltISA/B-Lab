"""Strict exact-recovery benchmark: 100% evidence must round-trip byte-for-byte."""
from TOOLS.recovery_engine import build_report, reconstruct_exact, scan_fragments, sha256


def run() -> None:
    source = (
        b"HEADER-v1|" + b"A" * 4096 + b"|BLOCK-01|" + b"B" * 4096
        + b"|BLOCK-02|" + b"C" * 4096 + b"|FOOTER-v1"
    )

    # Baseline: complete evidence is supplied as one contiguous exact fragment.
    fragments = scan_fragments(source, source)
    report = build_report(source, fragments)
    rebuilt = reconstruct_exact(report)

    assert report.exact_bytes == len(source)
    assert report.exact_ratio == 1.0
    assert report.recovered_bytes == len(source)
    assert rebuilt == source
    assert sha256(rebuilt) == sha256(source)

    # Negative control: partial evidence must never be promoted to full recovery.
    partial = build_report(source, scan_fragments(source, b"HEADER-v1|"))
    try:
        reconstruct_exact(partial)
    except ValueError:
        pass
    else:
        raise AssertionError("partial evidence was incorrectly accepted as exact recovery")

    print("EXACT RECOVERY BENCHMARK: PASS")
    print(f"source_bytes={len(source)}")
    print(f"exact_bytes={report.exact_bytes}")
    print("exact_ratio=1.000000")
    print("digest_match=true")
    print("partial_evidence_rejected=true")
    print("roundtrip_claim=true")


if __name__ == "__main__":
    run()
