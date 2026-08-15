# EXP-0013 — Memory / graph reconstruction and portable deployment

## Objective

Verify that compression is subordinate to memory integrity: no node, edge, ordering or canonical state may disappear silently. A damaged archive must fail closed and require recovery from another trusted copy.

## Architecture

```text
                 SPACE
                   │
          canonical memory
                   │
        ┌──────────┼──────────┐
        ↓          ↓          ↓
     ACTIVE    TEMPORARY   LONG_TERM
        │          │          │
        └────── canonical ────┘
                   │
          minimal lossless form
                   │
          portable memory pack
                   │
       ┌───────────┴───────────┐
       ↓                       ↓
    phone/app                USB/disk
       ↓                       ↓
 materialize on demand    materialize on demand
```

## Integrity rules

- Nodes and edges are canonical data.
- Text, matrices, diagrams and graph visualizations are derived views.
- A dangling edge is rejected.
- A checksum mismatch is rejected.
- Corrupted data is never presented as valid memory.
- Recovery must come from another trusted canonical copy or archive snapshot.
- Compression is accepted only when exact reconstruction is possible.

## Prototype check

A deterministic three-node/two-edge graph was serialized, compressed and restored with exact node/edge equality. A deliberately corrupted payload failed the integrity check.

This validates the core mechanism, but it is **not yet a full production benchmark** of the complete repository corpus.

## Portable memory

The memory engine is designed so that a device can carry a compact canonical memory package and expand only the requested materialized views. This supports deployment on a phone, application bundle, USB device or disk while keeping persistent storage small.

The package is not required to keep every rendered text/graph copy. The canonical record remains the source of truth.

## Status

**PASS — core integrity/reconstruction mechanism.**

**NEXT:** run the complete corpus benchmark (project logs, text, binary state histories, graph histories) and report actual bytes, node/edge counts, round-trip equality and recovery results. No compression factor is declared until that benchmark is executed.
