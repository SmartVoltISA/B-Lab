# EXP-0026 — Closed-Loop Persistence and Recovery After Perturbation

## Status

**PASS — under the fixed toy model, persistent structural memory can support recovery of a self-generated return relation after that relation is removed, while the same repair mechanism fails when structural memory is reset each step.**

## Purpose

EXP-0025 showed natural return without an external state reset.

EXP-0026 asks a stronger question:

**Does persistent memory merely record the recurrent structure, or can it help preserve/recover that structure after perturbation?**

Initial topology:

A → B → C → D

Structural plasticity can create B→A with probability 0.35 when the traversed A→B relation reaches the creation threshold.

After a cycle has formed, the system runs until a fixed perturbation time. If B→A exists at that time, it is removed.

The system then gets one opportunity to regenerate B→A from the A→B relation.

## Fixed rules

Structural memory decay:

m(t+1) = 0.9 m(t)

Traversed relation reinforcement:

m(t+1) = min(1, 0.9 m(t) + 0.6)

Initial reverse-edge creation threshold:

0.5

Post-perturbation repair threshold:

0.9

Reverse-edge creation/repair probability:

0.35

Seeds:

1000

Run length:

60 steps

Perturbation:

step 20

## Conditions

### A — persistent structural memory

Structural memory is retained and decays by 0.9.

### B — reset structural memory

Structural memory is reset to zero after every step.

All other rules are identical.

## Results

### Persistent structural memory

- self-generated B→A cycle: **358/1000 = 35.8%**
- cycles present at perturbation: same successful subset
- recovery of removed B→A: **101/1000 = 10.1%**
- recovery among runs that had formed a cycle: **101/358 = 28.2%**

### Reset structural memory control

- self-generated B→A cycle: **358/1000 = 35.8%**
- recovery after perturbation: **0/1000 = 0%**

The identical 35.8% initial cycle rate is expected because initial creation uses the same one-step threshold in both conditions.

The difference appears only after perturbation.

## Interpretation

The experiment separates two stages:

1. **formation** of the recurrent relation;
2. **maintenance/recovery** of that relation.

Initial formation does not require long-term persistence under this rule.

Recovery does.

With persistent memory, the A→B relation retains a strong structural trace after repeated cycling. When B→A is removed, that retained trace can satisfy the stricter repair threshold and recreate the reverse relation.

With reset memory, the same A→B relation has no accumulated structural history at the repair stage, so the repair threshold cannot be reached.

## Main result

The observed difference is:

persistent memory → **101 recoveries / 1000**

reset memory → **0 recoveries / 1000**

Thus, within this toy model:

**persistent relational state can function as a structural repair resource, not merely as a passive historical record.**

## Important qualification

The recovery probability is not 35.8%.

The 35.8% figure is the initial cycle-formation rate.

Only 101/358 cycle-forming runs recovered after the fixed perturbation, because the perturbation was applied at a fixed time and the repair opportunity depends on the system being at the appropriate state when the relation is removed.

Therefore the correct reported values are:

- cycle formation: **35.8% of all seeds**
- recovery: **10.1% of all seeds**
- recovery conditional on prior cycle formation: **28.2%**

## Control significance

The most informative comparison is not cycle formation but recovery:

```
persistent structural memory   → 101 recoveries
reset structural memory        →   0 recoveries
```

while initial cycle formation remains identical:

```
35.8% vs 35.8%
```

This isolates the effect of persistence on the post-perturbation stage.

## Current mechanism

The evidence chain now becomes:

initial distinction
→ relation
→ structure
→ persistent structural state
→ plasticity
→ emergent loop
→ natural recurrence
→ memory trace
→ perturbation
→ memory-assisted recovery
→ renewed recurrence

## What this establishes

Within the fixed toy architecture:

1. A recurrent relation can emerge from an initially acyclic graph.
2. The system can revisit a previous state without external reset.
3. Repeated recurrence strengthens a persistent relational trace.
4. Removing the recurrent relation does not necessarily erase its accumulated trace.
5. That trace can assist regeneration of the removed relation.
6. Resetting the trace removes the measured recovery effect.

## What this does NOT establish

It does not establish:

- consciousness;
- subjective experience;
- free will;
- intelligence;
- biological homeostasis;
- universal self-repair;
- that memory is always structural;
- that cycles are necessary for self-maintenance.

## Next experiment

**EXP-0027 — repeated perturbation / resilience curve.**

Apply multiple controlled lesions to the same recurrent relation and measure:

- probability of recovery after each lesion;
- recovery latency;
- memory level before each lesion;
- point at which repeated damage causes permanent loss;
- comparison with a no-memory control.

This will determine whether relational memory produces a measurable resilience curve rather than a single recovery event.
