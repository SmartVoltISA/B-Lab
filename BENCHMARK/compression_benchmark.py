"""Reproducible benchmark for the structural memory representation.

Runs only codecs available on the CI host; unavailable codecs are reported as SKIP.
The benchmark compares raw logical bytes with the structural representation and,
where possible, applies external codecs to both. Results are emitted as JSON.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from TOOLS.compression_tool import compress, decompress

DATASETS = {
    "alternating": [0, 1] * 5000,
    "zero_run": [0] * 5000 + [1] * 5000,
    "mixed": ([0, 1, 1, 0, 0, 1, 0, 1] * 1250),
    "randomish": [((i * 73 + 19) % 2) for i in range(10000)],
}

CODECS = {
    "gzip": ["gzip", "-c", "-9"],
    "bzip2": ["bzip2", "-c", "-9"],
    "xz": ["xz", "-c", "-9"],
    "lz4": ["lz4", "-c", "-12"],
    "zstd": ["zstd", "-q", "-c", "-19"],
    "brotli": ["brotli", "-q", "11", "-c"],
}


def raw_bytes(sequence: list[int]) -> bytes:
    return bytes(sequence)


def structural_bytes(sequence: list[int]) -> bytes:
    initial, targets = compress(sequence)
    # Canonical binary serialization: one initial byte followed by one byte per target.
    return bytes([initial, *targets])


def run_codec(command: list[str], payload: bytes) -> tuple[int, float]:
    start = time.perf_counter()
    result = subprocess.run(command, input=payload, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    elapsed = time.perf_counter() - start
    return len(result.stdout), elapsed


def main() -> None:
    report: dict = {"status": "ok", "datasets": {}, "codecs": {}}

    for name, sequence in DATASETS.items():
        raw = raw_bytes(sequence)
        structural = structural_bytes(sequence)
        assert decompress(*compress(sequence)) == sequence
        report["datasets"][name] = {
            "logical_symbols": len(sequence),
            "raw_bytes": len(raw),
            "structural_bytes": len(structural),
            "structural_ratio": len(structural) / len(raw),
        }
        for codec, command in CODECS.items():
            if shutil.which(command[0]) is None:
                report["codecs"].setdefault(codec, {"status": "SKIP", "reason": "not installed"})
                continue
            for representation, payload in (("raw", raw), ("structural", structural)):
                size, elapsed = run_codec(command, payload)
                report["codecs"].setdefault(codec, {"status": "PASS", "results": {}})["results"].setdefault(name, {})[representation] = {
                    "bytes": size,
                    "seconds": elapsed,
                    "ratio_to_raw": size / len(raw),
                }

    out = Path("BENCHMARK/results.json")
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
