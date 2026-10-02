# EXP-0023 — Separating Cycle Formation from Memory Read-Back

## Status

**PASS — cycle formation and later read-back can be separated experimentally by changing only probe-memory persistence/threshold while holding structural plasticity fixed.**

## Purpose

EXP-0022 showed that an initially acyclic chain can generate its own return relation and that an independent probe memory can read that relation later.

A remaining question is whether the measured read-back is merely a copy of cycle formation, or whether memory persistence introduces an independently tunable second stage.

EXP-0023 therefore keeps the structural mechanism fixed and varies only the probe-memory decay and probe threshold.

## Fixed structural mechanism

Initial topology:

```
A → B → C → D
```

Structural decay:

```
0.9
```

Structural reinforcement:

```
+0.6
```

Reverse-edge creation threshold:

```
0.5
```

Reverse-edge probability:

```
0.35
```

1000 deterministic seeds.

The structural mechanism therefore remains identical to EXP-0022.

## Probe protocol

The run is stopped at a fixed early probe time after three traversals.

The final visible state is externally set to A.

The probe reads:

```
B if probe_memory(B→A) >= threshold
STOP otherwise
```

Only probe-memory decay and threshold are varied.

## Results

The structural result was unchanged across probe settings:

**358/1000 = 35.8%** of seeds generated the B→A return relation.

The probe result changed independently.

### Probe decay = 0.5

| Threshold | Read-back B |
|---:|---:|
| 0.50 | 0/1000 |
| 0.55 | 0/1000 |
| 0.60 | 0/1000 |
| 0.70 | 0/1000 |

### Probe decay = 0.7

| Threshold | Read-back B |
|---:|---:|
| 0.50 | 0/1000 |
| 0.55 | 0/1000 |
| 0.60 | 0/1000 |
| 0.70 | 0/1000 |

### Probe decay = 0.9

| Threshold | Read-back B |
|---:|---:|
| 0.50 | 358/1000 |
| 0.55 | 0/1000 |
| 0.60 | 0/1000 |
| 0.70 | 0/1000 |

### Probe decay = 0.99

| Threshold | Read-back B |
|---:|---:|
| 0.50 | 358/1000 |
| 0.55 | 358/1000 |
| 0.60 | 0/1000 |
| 0.70 | 0/1000 |

## Interpretation

This gives two distinct stages:

```
structural plasticity
        ↓
cycle formation
        ↓
traversal history
        ↓
probe-memory persistence
        ↓
thresholded read-back
```

The cycle rate remains fixed at 35.8%, while the read-back rate changes from 0% to 35.8% solely because the probe-memory parameters change.

Therefore:

**cycle formation ≠ memory read-back.**

The two mechanisms are coupled causally in the experiment, but they are not the same measured variable.

## Important limitation

The 0.35 structural probability produces exactly one main opportunity for the B→A relation in this short protocol, so the structural cycle rate is essentially determined by that probability.

This experiment therefore does not yet characterize a rich memory-capacity curve. It demonstrates parameter separability.

A broader sweep over probe delay, decay, threshold, repeated returns, and competing memories would be needed to characterize retention quantitatively.

## Current evidence chain

After EXP-0019 → EXP-0020 → EXP-0021 → EXP-0022 → EXP-0023:

```
relation
  ↓
persistent relational state
  ↓
structural plasticity
  ↓
new relation
  ↓
emergent cycle
  ↓
self-generated recurrence
  ↓
independent memory trace
  ↓
history-dependent read-back
```

## What is now supported

Within the tested toy architecture:

1. A loop can exist without memory, but the loop alone does not produce the measured probe read-back.
2. Memory can be persistent independently of structural topology.
3. Structural plasticity can create a relation that was absent initially.
4. That relation can create recurrence.
5. Recurrence can generate additional traversal history.
6. Independent memory can preserve part of that history.
7. Persistence and threshold determine whether the stored history is later expressed as a different response.

## What remains unproven

This still does not establish:

- consciousness;
- subjective experience;
- free will;
- intelligence;
- semantics;
- biological equivalence;
- universality;
- that cycles are necessary for memory.

## Next experiment

**EXP-0024 — competing memories / interference.**

Create two independently stored relational histories and test whether a later probe can distinguish them after identical visible-state resets. The key question is whether relational memory can support more than a single scalar trace and whether interference/competition produces measurable hysteresis.
