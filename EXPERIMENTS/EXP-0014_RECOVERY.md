# EXP-0014 — Evidence-First Data Recovery

## Objective

Test whether B-Lab can recover intact fragments from damaged data without presenting guesses as original information.

## Safety model

- Source data is read-only.
- Recovery records carry source SHA-256 provenance.
- Exact evidence and inferred information are separate quantities.
- Unknown gaps are not counted as recovered.
- A reconstructed buffer is never equivalent to an original file unless independent validation proves it.

## Current implementation

`TOOLS/recovery_engine.py`

Capabilities in v0.1:

1. read-only signature scanning;
2. fragment provenance;
3. exact-byte accounting;
4. overlap rejection;
5. source-integrity validation;
6. explicit recovery ratio;
7. reconstruction of verified fragments only.

## Current status

🟢 Unit-level recovery invariants implemented.
🟡 Full corpus benchmark not yet run.
🔴 No claim of complete file/image/video recovery.

## Required next benchmark

Create controlled damaged copies of known source files and measure:

- byte recovery;
- object/file recovery;
- structural recovery;
- graph/node/edge recovery;
- semantic recovery where independently verifiable;
- false-positive rate;
- exact confidence calibration.

Classes:

A — intact control;
B — single contiguous damage;
C — multiple damage regions;
D — reordered fragments;
E — missing fragments;
F — adversarial/random corruption.

The original source remains the ground truth and is never modified.
