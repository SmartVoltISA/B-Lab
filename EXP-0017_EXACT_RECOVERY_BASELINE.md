# EXP-0017 — Exact Recovery Baseline

## Purpose

Establish a strict positive control for recovery: when evidence covers 100% of the source bytes contiguously and every fragment is exact, the recovery engine must reproduce the source byte-for-byte.

## Hypothesis

**H1:** Complete exact evidence is sufficient for deterministic byte-exact reconstruction.

## Controls

- Positive control: one exact fragment covering the complete source.
- Negative control: only the header signature is supplied; exact reconstruction must be rejected.
- Integrity control: SHA-256 of rebuilt bytes must equal SHA-256 of the source.

## Acceptance criteria

1. `exact_bytes == source_size`.
2. `exact_ratio == 1.0`.
3. Rebuilt bytes equal source bytes exactly.
4. Rebuilt SHA-256 equals source SHA-256.
5. Partial evidence raises an error instead of filling or guessing unknown bytes.

## Scope boundary

This experiment proves the **identity/round-trip path**, not recovery from damage. EXP-0015 remains the controlled damage sweep for evidence-only recovery. A successful EXP-0017 run must not be interpreted as proof that destroyed bytes can be reconstructed.

## Status

Implemented in `BENCHMARK/recovery_exact_benchmark.py` and enforced by CI.
