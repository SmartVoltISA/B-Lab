# B-Lab — Canonical Memory Architecture v1.0

## Goal

Store the minimum sufficient representation of information and reconstruct richer views only when they are needed.

The principle is:

```text
input
  ↓
canonical representation
  ↓
minimal lossless encoding
  ↓
ACTIVE / TEMPORARY / LONG_TERM
  ↓
materialize on demand
  ↓
text / relations / graph / analysis
```

## Three memory tiers

### ACTIVE

Hot working memory. Contains the canonical records currently needed by the running process. Derived views are disposable.

### TEMPORARY

Intermediate workspace for experiments, transformations, pending analysis and short-lived materializations. It may be safely rebuilt from canonical memory.

### LONG_TERM

Persistent archive. Stores canonical lossless records and metadata required for exact reconstruction. Duplicate rendered text, graphs and analysis views are not stored unless explicitly promoted to canonical evidence.

## Compression rule

The engine tests multiple lossless representations and selects the smallest representation available to it. If an encoding is not smaller, the raw representation is retained.

Current native modes:

- `RAW` — exact bytes, no transformation.
- `RLE` — deterministic run-length encoding for repetitive bytes.
- `BITS` — eight binary states per byte for 0/1 state sequences.

No third-party compression dependency is required by the core memory engine.

## Important limitation

There is no universal lossless transform that can make every possible input smaller. The laboratory therefore measures actual stored size rather than claiming a theoretical compression gain for arbitrary data.

For binary state histories, the native bit representation provides the direct 8× packing gain demonstrated by the laboratory. For repetitive text/data, RLE can provide additional reduction. Future experiments may add stronger native codecs, but each must pass exact round-trip and size benchmarks before adoption.

## Reconstruction principle

The long-term record is the source of truth. Text, relations, graphs, matrices and analytical views are reconstructed from it when requested. This prevents memory growth caused by storing the same information in several derived forms.

```text
ONE CANONICAL RECORD
        │
        ├── text view
        ├── relation view
        ├── graph view
        ├── matrix view
        └── analysis view
```

The architecture therefore separates **memory** from **presentation**.
