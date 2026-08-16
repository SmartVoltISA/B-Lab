# EXP-0015 — Controlled Recovery Damage Sweep

## Purpose

Measure the baseline behavior of the evidence-first Recovery Engine as deterministic corruption increases.

This experiment is deliberately conservative: it measures **exact evidence coverage**, not guessed reconstruction.

## Fixed protocol

1. Generate one deterministic source containing five known signatures and four payload blocks.
2. Create six conditions: 0%, 1%, 5%, 10%, 25%, and 50% corruption.
3. Replace one contiguous interval with `?` bytes.
4. Scan only for the predefined signatures.
5. Build a provenance-checked report.
6. Reconstruct only evidence-backed fragments.
7. Compare the reconstruction digest with the original source digest.

## Metrics

- `damaged_bytes` — bytes actually changed.
- `exact_bytes` — bytes supported by verified evidence.
- `exact_ratio` — exact bytes / source size.
- `digest_match` — whether evidence-only reconstruction equals the original.

## Acceptance rules

- `inferred_bytes == 0` for this baseline engine.
- `recovered_bytes == exact_bytes`.
- If exact coverage is incomplete, the reconstruction digest must not equal the source digest.
- No damaged bytes may be silently counted as recovered.

## Interpretation

A PASS means the accounting remains honest as corruption increases. It does **not** mean the engine can reconstruct destroyed information.

The next engineering step is a parser/checksum-aware recovery experiment in which redundant or self-validating file structures can provide evidence beyond raw signatures.

## Status

Implemented in `BENCHMARK/recovery_damage_sweep.py` and executed by CI.
