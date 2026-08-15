# B-Lab — Comparator

## Purpose

Compare an experimentally observed binary structure with independently registered formal mathematical models.

The comparator does not decide in advance which side is correct.

## Flow

```text
experiment
   ↓
 frozen result
   ↓
 normalization
   ↓
 Comparator
   ├── binary relations
   ├── directed graphs
   ├── transition systems
   ├── adjacency matrices
   └── explicitly registered Boolean structures
   ↓
 MATCH / DIFFERENCE / UNRESOLVED
   ↓
 visualization
   ↓
 archive
```

## Comparison rules

- Structural correspondence is required.
- Names and labels are not evidence.
- A mismatch is a valid result.
- An unexplained structure remains unresolved.
- The exact experiment and formal-model versions are recorded.
- Visualization supports inspection but does not constitute proof.

## First comparison target

For `EXP-0001`, compare minimal deterministic two-state transition systems against their formal relation and graph representations.
