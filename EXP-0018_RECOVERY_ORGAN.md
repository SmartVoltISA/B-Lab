# EXP-0018 — Recovery Organ Integration

## Goal

Assemble the recovery components into one conservative organ without granting it authority to modify a source device/image.

## Organ

```text
SOURCE IMAGE (read-only)
        ↓
FINGERPRINT
        ↓
FILESYSTEM METADATA ─────┐
        ↓                │
RAW SIGNATURE SCAN       │
        ↓                │
FORMAT VALIDATION         │
        ↓                │
EVIDENCE GRAPH ←──────────┘
        ↓
TRUST / EVIDENCE SCORE
        ↓
RECOVERY REPORT
```

## Components

- `TOOLS/disk_image.py` — immutable source fingerprint and chunk ranges.
- `TOOLS/filesystem_analyzer.py` — conservative extent metadata analysis.
- `TOOLS/format_validators.py` — basic container/header evidence.
- `TOOLS/recovery_organ.py` — evidence graph and report orchestration.
- `TOOLS/recovery_report.py` — stable JSON report output.

## Safety boundary

The current organ accepts bytes/metadata fixtures and has no write path to a source device. A future physical-device adapter must be explicitly read-only and must operate on a forensic image/copy where possible. Established recovery tools likewise recommend avoiding writes to the source filesystem because writes can overwrite recoverable data. citeturn0search0turn0search3

## Validation boundary

A header match is not semantic validation. A trust score is evidence strength, not a probability that the reconstruction is true. Full recovery is claimed only by the exact-recovery layer when complete byte coverage and digest equality are demonstrated.

## External comparison

TestDisk/PhotoRec provide mature filesystem recovery and signature-based carving. PhotoRec can recover files from corrupted filesystems but does not preserve original filenames or directory structure. The B-Lab organ therefore treats carving as one evidence source and adds explicit graph/history/trust layers rather than claiming to replace established recovery utilities. citeturn0search4turn0search5

## Status

Implemented as an experimental organ and connected to CI through `BENCHMARK/recovery_organ_benchmark.py`. It is not yet certified for arbitrary physical disks or arbitrary damaged file formats.
