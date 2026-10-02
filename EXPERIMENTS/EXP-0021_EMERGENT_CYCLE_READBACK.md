# EXP-0021 — Emergent Cycle → Independent Read-Back Probe

## Status

**PASS — under the preregistered toy rule, emergent cycle formation can create additional self-generated traversal history that changes an independent probe action.**

## Purpose

EXP-0020 showed that a cycle can emerge from structural plasticity, but its action policy was confounded with the same memory used to create the cycle.

EXP-0021 separates:

1. structural memory — controls whether a reverse relation can emerge;
2. probe memory — records traversal history and is read only at the final probe.

## Initial topology

```text
A → B → C → D
A → D
```

No directed cycle exists initially.

## Fixed rules

Structural memory:

```text
m_struct(t+1) = 0.9*m_struct(t)
```

For the traversed relation:

```text
m_struct(t+1) = min(1, 0.9*m_struct(t) + 0.6)
```

When structural memory reaches 0.5, the reverse relation is added with probability 0.35 if absent.

Independent probe memory uses the same decay/reinforcement law, but **does not participate in topology changes**.

During autonomous dynamics:

- first transition is forced A→B;
- at B, if B→A has emerged, the system returns to A; otherwise it follows B→C;
- C follows C→D;
- D follows D→A only if that relation has emerged; otherwise it remains at D.

At a fixed final probe time, the visible state is externally set to A in both the plastic and frozen-topology conditions. The probe then chooses:

```text
B if probe_memory(A→B) >= 0.5
D otherwise
```

The final external probe input is therefore identical.

## Conditions

### A — dynamic topology + persistent probe memory

Structural plasticity enabled. Probe memory persistent.

### B — frozen topology + persistent probe memory

Structural plasticity disabled. Probe memory persistent.

### C — dynamic topology + no probe memory

Structural plasticity enabled. Probe memory reset/disabled.

### D — frozen topology + no probe memory

Both mechanisms disabled.

## Results

1000 deterministic seeds per condition.

### A — dynamic + persistent probe memory

- emergent cycle: **723/1000 = 72.3%**
- matched final probe action differed from the frozen-topology control in **358/1000 = 35.8%** of seeds.

In those cases the dynamic system had acquired additional self-generated traversal history before the final probe.

### B — frozen topology + persistent probe memory

- emergent cycle: **0/1000**
- no topology-generated return path;
- no corresponding plasticity-induced change in the matched probe action.

### C — dynamic topology + no probe memory

- emergent cycle: **723/1000 = 72.3%**
- matched probe action difference: **0/1000**.

This is the critical memory control: cycle formation alone did not change the final probe when the probe memory was absent.

### D — frozen topology + no probe memory

- emergent cycle: **0/1000**
- matched probe action difference: **0/1000**.

## Main result

The cleanest causal chain supported by this experiment is:

```text
acyclic relation structure
        ↓
structural plasticity
        ↓
emergent directed cycle
        ↓
additional self-generated traversal
        ↓
persistent independent probe memory
        ↓
changed response to the same final visible state/input
```

For 35.8% of matched seeds, the dynamic system and frozen-topology control reached the same externally imposed probe state A but produced different probe actions because their histories differed.

## What this establishes

Within this toy model:

- cycles can be generated rather than pre-installed;
- an emergent cycle can create additional internally generated experience/traversal;
- an independent persistent memory can retain that difference;
- the retained difference can alter later behavior under the same visible probe condition.

This is a stronger result than EXP-0019 because the cycle itself is no longer supplied as part of the initial topology, and the probe memory is separated from the structural mechanism.

## What this does NOT establish

It does not establish:

- consciousness;
- subjective experience;
- free will;
- intelligence;
- semantic understanding;
- that cycles are necessary for all forms of memory;
- that this mechanism is universal.

## Important model dependence

The 35.8% figure is specific to the fixed topology, thresholds, decay/learning values, structural plasticity probability, deterministic policy and 1000-seed sweep used here. It is an effect size for this model, not a universal constant.

## Next experiment

**EXP-0022 — Remove the pre-existing route A→D.**

Test whether the same mechanism can generate its own alternative route and then use the newly generated relational structure to alter behavior, rather than relying on a pre-existing fallback edge. Keep the same separation between structural memory and probe memory.
