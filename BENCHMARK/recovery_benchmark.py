"""B-Lab recovery benchmark: corruption, evidence, and exact-coverage accounting."""
from TOOLS.recovery_engine import build_report, reconstruct, scan_fragments


def run() -> None:
    source = (
        b"HEADER-v1|"
        + b"A" * 4096
        + b"|BLOCK-01|"
        + b"B" * 4096
        + b"|BLOCK-02|"
        + b"C" * 4096
        + b"|FOOTER-v1"
    )

    # Simulate damage in the middle of BLOCK-01 while preserving other regions.
    damaged = bytearray(source)
    damage_start = source.index(b"|BLOCK-01|") + 3
    damage_end = damage_start + 512
    damaged[damage_start:damage_end] = b"?" * (damage_end - damage_start)
    damaged = bytes(damaged)

    magic = [b"HEADER-v1|", b"|BLOCK-01|", b"|BLOCK-02|", b"|FOOTER-v1"]
    fragments = []
    for signature in magic:
        fragments.extend(scan_fragments(damaged, signature))

    report = build_report(damaged, fragments)
    rebuilt = reconstruct(report)

    assert report.source_size == len(source)
    assert report.exact_bytes == sum(len(f.data) for f in report.fragments)
    assert report.inferred_bytes == 0
    assert report.exact_bytes < report.source_size
    assert report.recovered_bytes == report.exact_bytes

    # The damaged source must not be reported as fully recovered.
    assert report.exact_ratio < 1.0
    # Recovery output contains only evidence-backed fragments; unknown gaps stay zero.
    assert rebuilt[damage_start:damage_end] == b"\x00" * (damage_end - damage_start)

    print("RECOVERY BENCHMARK: PASS")
    print(f"source_bytes={report.source_size}")
    print(f"exact_bytes={report.exact_bytes}")
    print(f"exact_ratio={report.exact_ratio:.6f}")
    print(f"fragments={len(report.fragments)}")
    print("roundtrip_claim=false")
    print("evidence_only=true")


if __name__ == "__main__":
    run()
