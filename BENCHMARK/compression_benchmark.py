"""Reproducible benchmark for structural binary memory and lossless codecs."""

from __future__ import annotations

import json
import random
import shutil
import statistics
import subprocess
import time
from pathlib import Path

from TOOLS.bitpack import pack_memory, unpack_memory
from TOOLS.compression_tool import compress, decompress

REPEATS = 3


def make_random(length: int, seed: int) -> list[int]:
    rng = random.Random(seed)
    return [rng.getrandbits(1) for _ in range(length)]


DATASETS = {
    "alternating_1k": [0, 1] * 500,
    "zero_run_1k": [0] * 500 + [1] * 500,
    "mixed_1k": [0, 1, 1, 0, 0, 1, 0, 1] * 125,
    "random_1k": make_random(1000, 1),
    "alternating_10k": [0, 1] * 5000,
    "zero_run_10k": [0] * 5000 + [1] * 5000,
    "mixed_10k": [0, 1, 1, 0, 0, 1, 0, 1] * 1250,
    "random_10k": make_random(10000, 2),
    "alternating_100k": [0, 1] * 50000,
    "zero_run_100k": [0] * 50000 + [1] * 50000,
    "mixed_100k": [0, 1, 1, 0, 0, 1, 0, 1] * 12500,
    "random_100k": make_random(100000, 3),
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
    packed = pack_memory(initial, targets)
    recovered = unpack_memory(packed, len(sequence))
    assert recovered == (initial, targets)
    assert decompress(*recovered) == sequence
    return packed


def run_codec(command: list[str], payload: bytes) -> tuple[int, float]:
    timings = []
    size = 0
    for _ in range(REPEATS):
        start = time.perf_counter()
        result = subprocess.run(command, input=payload, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        size = len(result.stdout)
        timings.append(time.perf_counter() - start)
    return size, statistics.median(timings)


def main() -> None:
    report: dict = {"status": "ok", "repeats": REPEATS, "datasets": {}, "codecs": {}}
    for name, sequence in DATASETS.items():
        raw = raw_bytes(sequence)
        structural = structural_bytes(sequence)
        report["datasets"][name] = {
            "logical_symbols": len(sequence),
            "raw_bytes": len(raw),
            "structural_packed_bytes": len(structural),
            "structural_ratio_to_raw": len(structural) / len(raw),
            "logical_length_metadata_bytes": 4,
            "structural_total_with_length": len(structural) + 4,
            "roundtrip": True,
        }
        for codec, command in CODECS.items():
            if shutil.which(command[0]) is None:
                report["codecs"].setdefault(codec, {"status": "SKIP", "reason": "not installed"})
                continue
            for representation, payload in (("raw", raw), ("structural", structural)):
                size, elapsed = run_codec(command, payload)
                report["codecs"].setdefault(codec, {"status": "PASS", "results": {}})["results"].setdefault(name, {})[representation] = {
                    "bytes": size,
                    "seconds_median": elapsed,
                    "ratio_to_raw": size / len(raw),
                }
    Path("BENCHMARK/results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
