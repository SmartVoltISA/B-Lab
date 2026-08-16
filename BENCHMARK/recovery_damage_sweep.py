"""EXP-0015 baseline: controlled corruption sweep for evidence-first recovery."""
from TOOLS.recovery_engine import build_report, reconstruct, scan_fragments, sha256

SIGNATURES = [b"HEADER-v1|", b"|BLOCK-01|", b"|BLOCK-02|", b"|BLOCK-03|", b"|FOOTER-v1"]
DAMAGE_FRACTIONS = (0.00, 0.01, 0.05, 0.10, 0.25, 0.50)


def make_source() -> bytes:
    return (
        SIGNATURES[0] + b"A" * 4096 + SIGNATURES[1] + b"B" * 4096
        + SIGNATURES[2] + b"C" * 4096 + SIGNATURES[3] + b"D" * 4096
        + SIGNATURES[4]
    )


def corrupt(source: bytes, fraction: float) -> bytes:
    if not 0.0 <= fraction <= 1.0:
        raise ValueError("fraction must be between 0 and 1")
    n = int(len(source) * fraction)
    if n == 0:
        return source
    start = (len(source) - n) // 2
    damaged = bytearray(source)
    damaged[start:start + n] = b"?" * n
    return bytes(damaged)


def measure(source: bytes, damaged: bytes) -> tuple[int, float, bool]:
    fragments = []
    for signature in SIGNATURES:
        fragments.extend(scan_fragments(damaged, signature))
    report = build_report(damaged, fragments)
    rebuilt = reconstruct(report)
    digest_match = sha256(rebuilt) == sha256(source)
    assert report.inferred_bytes == 0
    assert report.recovered_bytes == report.exact_bytes
    if report.exact_ratio < 1.0:
        assert not digest_match
    return report.exact_bytes, report.exact_ratio, digest_match


def run() -> None:
    source = make_source()
    print("RECOVERY DAMAGE SWEEP: START")
    print("fraction,damaged_bytes,exact_bytes,exact_ratio,digest_match")
    for fraction in DAMAGE_FRACTIONS:
        damaged = corrupt(source, fraction)
        exact_bytes, exact_ratio, digest_match = measure(source, damaged)
        damaged_bytes = sum(a != b for a, b in zip(source, damaged))
        print(f"{fraction:.2f},{damaged_bytes},{exact_bytes},{exact_ratio:.6f},{str(digest_match).lower()}")
    print("RECOVERY DAMAGE SWEEP: PASS")
    print("claim=baseline_evidence_only")


if __name__ == "__main__":
    run()
