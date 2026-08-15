"""Reproducible compression benchmark harness.

The harness never treats an unavailable codec as a failure: it records SKIP.
It compares physical serialized size, not only logical symbol counts.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from TOOLS.compression_tool import compress, decompress

CODECS = {
    "zstd": ["zstd", "-q", "-c"],
    "lz4": ["lz4", "-q", "-c"],
    "brotli": ["brotli", "-q", "-c"],
    "xz": ["xz", "-q", "-c"],
}


def corpus() -> list[list[int]]:
    return [
        [0],
        [0, 1],
        [0, 1, 0, 1] * 32,
        [0] * 256,
        [0, 1] * 1024,
        [(i * 17 + 3) % 2 for i in range(2048)],
    ]


def structural_bytes(sequence: list[int]) -> bytes:
    initial, targets = compress(sequence)
    # Explicit deterministic serialization for physical-size measurement.
    return bytes([initial, *targets])


def raw_bytes(sequence: list[int]) -> bytes:
    return bytes(sequence)


def run_codec(name: str, payload: bytes) -> tuple[str, int, float]:
    command = CODECS[name]
    if shutil.which(command[0]) is None:
        return "SKIP", 0, 0.0
    start = time.perf_counter()
    proc = subprocess.run(command, input=payload, capture_output=True, check=True)
    elapsed = time.perf_counter() - start
    return "OK", len(proc.stdout), elapsed


def main() -> None:
    rows: list[str] = []
    rows.append("| corpus | representation | input bytes | codec | status | output bytes | encode seconds |")
    rows.append("|---|---|---:|---|---|---:|---:|")
    for idx, sequence in enumerate(corpus(), 1):
        for representation, encoder in (("RAW", raw_bytes), ("STRUCTURAL", structural_bytes)):
            payload = encoder(sequence)
            for codec in CODECS:
                status, size, elapsed = run_codec(codec, payload)
                rows.append(f"| C{idx} | {representation} | {len(payload)} | {codec} | {status} | {size} | {elapsed:.6f} |")
    Path("BENCHMARK/results.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
