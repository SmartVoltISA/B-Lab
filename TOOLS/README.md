# B-Lab Tools

## STRUCTURAL-BINARY-MEMORY v1.0
`compression_tool.py` + `bitpack.py`

Purpose: lossless compact representation of binary structural memory.

- Canonical logical state: initial value + ordered targets.
- Serialization: 1 bit per binary state.
- Exact recovery requires logical length metadata.
- No state, transition, or ordering information is discarded.
- Validated at 1k, 10k, and 100k symbols, including deterministic random data.

Measured result: 100,000 binary symbols occupy 12,500 packed bytes; with 4-byte logical length metadata, 12,504 bytes. Round-trip validation passed.

## ADAPTIVE-LOSSLESS-ARCHIVE v0.1
`lossless_archive.py`

Purpose: general byte-level lossless archival with integrity protection.

- Tests gzip, bz2, and xz and selects the smallest payload.
- Stores original length and SHA-256.
- Detects corrupted payloads.
- Exact byte-for-byte round-trip is mandatory.

Important: this is an adaptive archival container, not yet a new compression algorithm. Its measured purpose is safe lossless storage and codec selection. A future custom compressor must beat established codecs on a representative corpus before being promoted.

## GRAPH-MEMORY v1.0
`graph_memory.py`

Purpose: canonical graph memory with integrity protection.

- Nodes are canonical data.
- Edge order is preserved exactly because it can encode history.
- Dangling edges are rejected.
- SHA-256 protects the canonical payload.
- Corrupt payloads fail closed.

Latest CI confirmation: run #72 passed after the exact edge-order regression test was added.

## RECOVERY-ENGINE v0.1 — EXPERIMENTAL
`recovery_engine.py`

Purpose: read-only, evidence-first recovery of intact fragments from damaged data.

- Source is never modified.
- Fragments carry source SHA-256 provenance.
- Exact and inferred information are separated.
- Unknown gaps are not counted as recovered.
- Reconstructed buffers are never presented as original without independent validation.

This tool is experimental. Full damaged-file/image/video benchmarks have not yet been run. It is therefore **not** a production recovery utility.
