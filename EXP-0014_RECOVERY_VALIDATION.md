# EXP-0014 — Recovery Validation

## Purpose

Validate the current B-Lab Recovery Engine under controlled synthetic corruption.
The experiment tests whether the tool distinguishes **verified surviving fragments** from unknown or damaged regions.

## Fixed rule

The engine must not claim full reconstruction when only fragments are evidenced. Unknown gaps remain unknown. Exact recovery is limited to evidence-backed bytes.

## Procedure

1. Generate a deterministic source containing four known signatures and three data blocks.
2. Corrupt 512 bytes inside `BLOCK-01`, including its signature.
3. Scan the damaged source for all four signatures.
4. Build a provenance-checked recovery report.
5. Reconstruct only the verified fragments.
6. Assert that the damaged interval is not counted as recovered.
7. Assert that `exact_ratio < 1.0` and `inferred_bytes == 0`.

## Expected result

- The corrupted signature is not accepted.
- Surviving signatures are accepted as exact fragments.
- Unknown bytes are not silently converted into recovered data.
- The reconstruction output is explicitly **not** treated as the original source.

## Status

Implemented in `BENCHMARK/recovery_benchmark.py` and executed by CI.

A passing benchmark validates the evidence accounting, not magical recovery of destroyed information. Further recovery work requires experiments with real file formats, checksums, redundancy, and controlled damage models.
