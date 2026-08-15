"""Benchmark the adaptive lossless archive against common codecs."""

from __future__ import annotations

import bz2
import gzip
import hashlib
import json
import lzma
import random
from pathlib import Path

from TOOLS.lossless_archive import compress as archive_compress, decompress as archive_decompress, inspect


def random_bytes(n: int, seed: int) -> bytes:
    return random.Random(seed).randbytes(n)


DATASETS = {
    "text_like": (b"The archive must preserve structure, history, and meaning. " * 5000),
    "structured": bytes((i % 16) for i in range(100000)),
    "random": random_bytes(100000, 42),
}


def main() -> None:
    report = {"status": "ok", "datasets": {}}
    for name, data in DATASETS.items():
        archive = archive_compress(data)
        assert archive_decompress(archive) == data
        info = inspect(archive)
        candidates = {
            "adaptive_archive": len(archive),
            "gzip": len(gzip.compress(data, compresslevel=9, mtime=0)),
            "bz2": len(bz2.compress(data, compresslevel=9)),
            "xz": len(lzma.compress(data, preset=9, check=lzma.CHECK_SHA256)),
            "raw": len(data),
        }
        report["datasets"][name] = {
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "selected_codec": info.codec,
            "sizes": candidates,
            "archive_overhead_bytes": 54,
            "roundtrip": True,
        }
    Path("BENCHMARK/lossless_archive_results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
