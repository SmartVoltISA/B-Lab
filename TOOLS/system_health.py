"""Deterministic, dependency-light runtime health check for B-Lab."""

from __future__ import annotations

import importlib
import pathlib
import py_compile
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

MODULES = [
    "LAB.binary_relations", "LAB.comparator", "LAB.compressed_memory",
    "LAB.cycles", "LAB.derived_views", "LAB.history_vs_structure",
    "LAB.reconstruct_transitions", "LAB.representations", "LAB.temporal_memory",
    "TOOLS.bitpack", "TOOLS.compression_tool", "TOOLS.filesystem_analyzer",
    "TOOLS.format_validators", "TOOLS.graph_memory", "TOOLS.lossless_archive",
    "TOOLS.memory_engine", "TOOLS.recovery_engine", "TOOLS.recovery_organ",
    "TOOLS.recovery_structure", "TOOLS.stt_adapters", "TOOLS.tool_queue",
]


def main() -> int:
    failures: list[str] = []

    for module in MODULES:
        try:
            importlib.import_module(module)
        except Exception as exc:  # pragma: no cover
            failures.append(f"IMPORT {module}: {type(exc).__name__}: {exc}")

    # Compile every repository Python file. This catches syntax errors in tests,
    # benchmarks and optional backends without importing optional dependencies.
    files = sorted(
        p for p in ROOT.rglob("*.py")
        if ".git" not in p.parts and "__pycache__" not in p.parts
    )
    for path in files:
        if path.name == "system_health.py":
            continue
        try:
            py_compile.compile(str(path), doraise=True)
        except Exception as exc:  # pragma: no cover
            failures.append(f"COMPILE {path.relative_to(ROOT)}: {type(exc).__name__}: {exc}")

    print(f"python={sys.version.split()[0]}")
    print(f"modules_checked={len(MODULES)}")
    print(f"python_files_compiled={len(files) - 1}")
    print(f"failures={len(failures)}")
    for failure in failures:
        print(failure)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
