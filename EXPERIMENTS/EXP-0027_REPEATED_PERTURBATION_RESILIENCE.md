# EXP-0027 — Repeated Perturbation and Relational Resilience

## Status

**PASS — in the fixed toy model, persistent relational memory permits repeated recovery from lesions, producing a measurable resilience curve; resetting the memory removes recovery.**

## Purpose

EXP-0026 demonstrated one recovery after a recurrent relation was removed.

EXP-0027 applies repeated controlled lesions to the same recurrent relation.

Question: Does persistent relational memory provide measurable resilience under repeated damage?

## Model

Initial topology:

A → B → C → D

Structural plasticity can create B→A with probability 0.35 after the A→B relation reaches the creation threshold.

Structural memory:

m(t+1) = 0.9 m(t)

Traversed relation reinforcement:

m(t+1) = min(1, 0.9 m(t) + 0.6)

A cycle-forming run is then exposed to repeated lesions of B→A.

Before each lesion, the system receives three A→B traversals, allowing the structural memory of A→B to reach the repair threshold.

Repair condition:

m(A→B) >= 0.9

If the condition is met, B→A is regenerated with probability 0.35.

After recovery, the next lesion is applied.

## Conditions

### A — persistent structural memory

The A→B structural trace persists between traversals and lesions.

### B — reset structural memory

The structural trace is reset after each step. All other rules remain the same.

Seeds: 10,000

Maximum lesions per run: 8

## Results

Initial cycle formation was identical in both conditions:

3,570 / 10,000 = 35.7%

### Persistent-memory condition

| Recovery number | Runs still recovered | Fraction of all seeds |
|---:|---:|---:|
| 1 | 1251 | 12.51% |
| 2 | 443 | 4.43% |
| 3 | 161 | 1.61% |
| 4 | 50 | 0.50% |
| 5 | 20 | 0.20% |
| 6 | 7 | 0.07% |
| 7 | 2 | 0.02% |
| 8 | 0 | 0% |

Conditional on having formed a cycle:

- first recovery: 1251 / 3570 = 35.0%
- two consecutive recoveries: 443 / 3570 = 12.4%
- three: 161 / 3570 = 4.51%
- four: 50 / 3570 = 1.40%
- five: 20 / 3570 = 0.56%
- six: 7 / 3570 = 0.20%
- seven: 2 / 3570 = 0.056%
- eight: 0 / 3570 = 0%

### Reset-memory control

Initial cycle formation:

3,570 / 10,000 = 35.7%

Recovery after the first lesion:

0 / 10,000 = 0%

No run survived even the first recovery.

## Main result

The important comparison is:

same initial cycle formation
→ persistent memory: repeated recovery possible
→ reset memory: recovery impossible

The first-recovery probability among cycle-forming runs is approximately the programmed 0.35 repair probability: 35.0% observed vs 35% rule probability.

Subsequent recoveries decline approximately as repeated independent repair opportunities would predict.

This provides a controlled resilience curve rather than a single recovery observation.

## Interpretation

The result supports a distinction between:

1. structural formation — creating the recurrent relation;
2. memory persistence — retaining the relational trace;
3. repair — regenerating a removed relation;
4. resilience — surviving repeated perturbations.

Within this model, persistent relational memory functions as a prerequisite resource for the repair mechanism.

## Important limitation

The decreasing survival curve is strongly influenced by the fixed repair probability of 0.35.

Therefore the experiment does not demonstrate a universal biological resilience law.

It demonstrates that, under this architecture, repeated lesions generate a predictable survival curve when persistent relational memory supplies the repair condition.

Also, the repair mechanism is deliberately simple and local. It is not equivalent to biological tissue repair or immune regulation.

## Current evidence chain

relation
→ persistent relational state
→ structural plasticity
→ new relation
→ self-generated cycle
→ natural recurrence
→ memory trace
→ perturbation
→ memory-assisted repair
→ repeated perturbation
→ measurable resilience curve

## What this establishes

Within the tested toy architecture:

- recurrence can generate persistent structural traces;
- those traces can survive removal of a relation;
- persistent traces can enable relation regeneration;
- repeated perturbation produces measurable survival statistics;
- removing persistence eliminates the observed repair mechanism.

## What this does NOT establish

It does not establish:

- consciousness;
- subjective experience;
- free will;
- intelligence;
- biological homeostasis;
- universal self-repair;
- that relational memory is sufficient for an organism;
- that this toy resilience mechanism is equivalent to biological resilience.

## Next experiment

EXP-0028 — perturbation severity and memory reserve.

Instead of always deleting the same single relation, vary damage severity:

1. delete B→A;
2. delete A→B;
3. delete both;
4. temporarily suppress the relation;
5. erase part of structural memory;
6. erase all structural memory.

Measure recovery probability and recovery latency as a function of remaining relational memory.

The key question is whether there is a measurable memory reserve threshold below which recurrent structure can no longer reconstruct itself.
