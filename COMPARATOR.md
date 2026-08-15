# B-Lab — Comparator

## Purpose

Compare an experimentally observed binary structure with independently registered formal mathematical models.

The Comparator does not decide in advance which side is correct.

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
 MATCH / PARTIAL_MATCH / DIFFERENCE / UNRESOLVED
   ↓
 visualization
   ↓
 archive
```

## Binary relation representation

For states `{0,1}`, a directed relation is represented as:

`R ⊆ {0,1} × {0,1}`

Possible directed pairs:

- `(0,0)`
- `(0,1)`
- `(1,0)`
- `(1,1)`

The Comparator distinguishes a relation from the sequence that produced observations of that relation.

## Comparison rules

- Exact structural correspondence → `MATCH`.
- Experimental relation is a proper subset of the registered model → `PARTIAL_MATCH`.
- A measured relation contains a pair absent from the registered model → `DIFFERENCE`.
- Structure cannot currently be represented → `UNRESOLVED`.
- Structural correspondence is required.
- Names and labels are not evidence.
- A mismatch is a valid result.
- The exact experiment and formal-model versions are recorded.
- Visualization supports inspection but does not constitute proof.

## No semantic leakage

The Comparator must not assume that `0` means false, absence, negative or low, or that `1` means true, presence, positive or high. Such meanings belong to separately registered models.

## Visualization

The first visual comparison should show the same relation as both:

1. adjacency matrix;
2. directed graph;
3. transition sequence.

This is for structural inspection, not proof.

## Independence rule

Known mathematics is a comparison target, not an answer key. A discrepancy is preserved and may become the input to a new laboratory experiment.

## First comparison target

For `EXP-0001`, compare minimal deterministic two-state transition systems against their formal relation and graph representations.
