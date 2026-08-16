# EXP-0016 — Structural Recovery: Parser + Checksum + Redundancy

## Purpose

Test whether Recovery can move beyond signature-only evidence by using three stronger forms of evidence:

1. explicit file framing / parser structure;
2. SHA-256 checksum validation of payloads;
3. redundant copies of the same logical record.

## Scope

This is a controlled laboratory format, not a claim of arbitrary filesystem or media recovery.

## Fixed rule

A record is exact only when its framing parses and its checksum validates. A logical record may be recovered from an intact redundant copy when another copy is corrupted. No record is invented when all available copies fail validation.

## Controls

- one corrupted copy + one intact duplicate → recovery expected;
- all copies of a logical record corrupted → recovery must fail for that record;
- parser must reject checksum-invalid payloads;
- no full-loss reconstruction claim is allowed.

## Result interpretation

A passing benchmark validates structural parsing, checksum evidence, and redundancy selection. It does **not** establish recovery of arbitrary damaged JPEG, MP4, database, filesystem, or raw-disk data.

## Status

Implemented as `TOOLS/recovery_structure.py`, tested by `tests/test_recovery_structure.py`, benchmarked by `BENCHMARK/recovery_structure_benchmark.py`, and connected to CI.
