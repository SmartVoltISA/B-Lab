# EXP-0028 — Perturbation Severity and Memory Reserve

## Status

**PASS — under the fixed toy model, recovery has a sharp memory-reserve threshold: with the repair threshold fixed at 0.9, preserving at least 90% of the structural trace permits repair, while erasing below 90% prevents it. Damage to one relation is recoverable; damage that removes both relations requires multiple independent repair events and has lower recovery probability.**

## Purpose

EXP-0027 showed repeated resilience under a single lesion type.

EXP-0028 varies lesion severity and directly measures how much structural memory remains when the recurrent relation is damaged.

The key question is:

**Is there a measurable memory reserve below which the structure can no longer reconstruct itself?**

## Fixed model

Initial topology:

A → B → C → D

Structural memory:

m(t+1) = 0.9 m(t)

Traversed relation reinforcement:

m(t+1) = min(1, 0.9 m(t) + 0.6)

After three A→B traversals:

m(A→B) = 1.0

Reverse relation B→A is initially created with probability 0.35.

Repair threshold:

m(A→B) >= 0.9

Repair probability:

0.35

Seeds:

10,000 per condition.

## Lesion classes

### L1 — delete B→A

The recurrent return relation is removed. A→B and its structural memory remain.

Recovery requires one repair event.

Observed recovery:

3519 / 10000 = 35.19%

This is close to the programmed repair probability of 35%.

### L2 — delete A→B

The forward relation is removed, while B→A may remain.

Recovery requires reconstruction of A→B. If it returns, the cycle can be restored.

Observed complete cycle recovery:

2084 / 10000 = 20.84%

### L3 — delete both A→B and B→A

Both relations are removed.

Two independent structural repairs are required.

Observed complete cycle recovery:

1276 / 10000 = 12.76%

### L4 — erase 50% of structural memory and delete B→A

Remaining memory:

m(A→B) = 0.50

This is below the fixed repair threshold of 0.90.

Observed recovery:

0 / 10000 = 0%

### L5 — erase all structural memory and delete B→A

Remaining memory:

m(A→B) = 0

Observed recovery:

0 / 10000 = 0%

## Memory-reserve sweep

A direct reserve sweep deleted B→A and varied the fraction of the A→B structural trace retained.

| Retained structural memory | Recovery |
|---:|---:|
| 0% | 0% |
| 25% | 0% |
| 50% | 0% |
| 75% | 0% |
| 89% | 0% |
| 90% | 35.7% |
| 99% | 35.7% |
| 100% | 35.7% |

The transition occurs exactly at the programmed threshold of 0.90.

## Main result

The experiment identifies a memory reserve threshold in this toy architecture.

Below m = 0.9, the repair mechanism cannot activate.

At or above m = 0.9, repair becomes possible with probability 0.35.

Therefore the result is not evidence for a naturally occurring universal 90% threshold. The threshold is a property of the registered model.

What is experimentally demonstrated is that structural memory quantity can control whether a recurrent structure remains reconstructible.

## Damage hierarchy

The measured recovery probabilities are:

- one-edge return deletion: 35.19%;
- forward-edge deletion: 20.84%;
- both-edge deletion: 12.76%;
- partial memory erase to 50%: 0%;
- complete memory erase: 0%.

This follows the increasing number of required reconstruction events and loss of memory reserve.

## Important control

The memory-reserve sweep is especially useful because topology and repair probability are unchanged.

Only the amount of retained structural memory is varied.

The observed transition from 0% to 35.7% occurs at the exact registered threshold of 0.90.

## What this establishes

Within this toy architecture:

1. Different forms of structural damage have measurably different recovery probabilities.
2. Preserving one relational trace is sufficient for single-edge repair under the model.
3. Removing both cycle edges requires multiple reconstruction events and reduces complete recovery.
4. Reducing stored structural memory below the repair threshold blocks recovery.
5. Structural memory therefore acts as a measurable reserve for reconstruction.

## What this does NOT establish

It does not establish:

- consciousness;
- subjective experience;
- free will;
- intelligence;
- biological homeostasis;
- universal resilience laws;
- that 90% is a natural threshold;
- that relational memory is sufficient for an organism;
- equivalence to biological repair.

## Current chain

relation
→ persistent state
→ plasticity
→ emergent loop
→ recurrence
→ memory
→ perturbation
→ repair
→ memory reserve
→ resilience threshold

## Next experiment

**EXP-0029 — remove the hard-coded repair threshold.**

Replace the binary rule m >= 0.9 with a continuous repair probability dependent on memory strength, then test whether recovery follows a smooth dose-response curve.

This is important because EXP-0028 deliberately contains a hard threshold. The next experiment should determine whether the observed resilience can emerge continuously from memory strength rather than being imposed by a step function.
