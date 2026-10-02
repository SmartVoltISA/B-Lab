# EXP-0024 — Competing Relational Memories and Hysteresis

## Status

**PASS — under the fixed toy model, two independently stored relational traces can compete at the same visible probe state, and the probe response depends on recent history rather than only on the current state.**

## Purpose

Previous experiments established that persistent relational memory can alter later behavior after an emergent cycle.

EXP-0024 tests a stronger property: **two relational memories can coexist and compete**.

The key question is whether the same visible state can produce different probe actions depending on which relational history was reinforced most recently.

## Initial topology

Two initially acyclic branches:

```
A → B → C
A → D → E
```

No return relation is initially present.

Structural plasticity can independently create:

```
B → A
D → A
```

with probability 0.35 after the corresponding forward relation reaches the structural threshold.

## Structural result

10000 deterministic seeds were used.

Both return relations B→A and D→A emerged in:

**1237 / 10000 = 12.37%**

This is consistent with the independent 0.35 × 0.35 opportunities in this construction.

Thus the system can contain two independently generated return routes:

```
A ↔ B
A ↔ D
```

## Independent probe memory

Two memory channels are maintained independently:

- m(B→A)
- m(D→A)

For each reinforcement event:

```
m_i(t+1) = 0.9 m_i(t)
```

and the selected relation receives:

```
+0.6
```

capped at 1.

At the final probe the visible state is always externally reset to **A**.

The probe chooses:

```
B if m(B→A) > m(D→A)
D if m(D→A) > m(B→A)
tie otherwise
```

## History-dependence tests

### Sequence 1

Three B-return reinforcements followed by one D-return reinforcement:

```
B B B D
```

Final memory:

```
m(B→A) = 0.90
m(D→A) = 0.60
```

Probe result: **B**

### Sequence 2

The exact opposite history:

```
D D D B
```

Final memory:

```
m(B→A) = 0.60
m(D→A) = 0.90
```

Probe result: **D**

The final visible state is A in both cases.

Therefore:

```
same current state
+
different relational history
→
different response
```

## Hysteresis test

Longer reinforcement pulses were also tested.

### B-dominant history

```
B B B B B D D
```

Final:

```
m(B→A) = 0.81
m(D→A) = 1.00
```

Probe: **D**

### D-dominant history

```
D D D D D B B
```

Final:

```
m(B→A) = 1.00
m(D→A) = 0.81
```

Probe: **B**

Thus a later short pulse can overcome a previously reinforced relation depending on the preceding history.

## Main result

EXP-0024 demonstrates, within this toy model:

**relational memory is not merely a record of the current state.**

Two memories can coexist, decay, compete, and determine which relation is expressed at a later probe.

The system therefore exhibits a minimal form of **history-dependent selection**.

## Combined evidence chain

EXP-0019:

```
persistent relational memory
→
history-dependent behavior
```

EXP-0020:

```
persistent structural memory + plasticity
→
emergent cycle
```

EXP-0021:

```
emergent cycle
→
additional self-generated traversal
→
independent memory read-back
```

EXP-0022:

```
pre-installed fallback route not required
```

EXP-0023:

```
cycle formation
≠
memory read-back
```

EXP-0024:

```
multiple relational memories
→
competition
→
history-dependent selection
→
hysteresis-like behavior
```

## What this establishes

Within the tested architecture:

1. Relations can acquire persistent state.
2. Structural plasticity can create relations that were absent initially.
3. Newly created relations can close directed loops.
4. Loops can create additional self-generated traversal.
5. Traversal history can be stored independently of structural memory.
6. Multiple relational traces can coexist.
7. Their relative strength can determine later behavior.
8. The same visible state can therefore produce different responses after different histories.

## What this does NOT establish

It does not establish:

- consciousness;
- subjective experience;
- free will;
- intelligence;
- semantic understanding;
- biological equivalence;
- universality;
- that loops are necessary for memory;
- that hysteresis in this toy memory is equivalent to biological hysteresis.

## Important model dependence

The numerical values are properties of this specific model:

- decay = 0.9;
- reinforcement = 0.6;
- structural reverse-edge probability = 0.35;
- 10000 structural seeds;
- two-branch topology;
- selected probe rule.

The experiment demonstrates the mechanism, not a universal quantitative law.

## Next experiment

**EXP-0025 — memory without externally imposed reset.**

Remove the artificial final reset to A and test whether the system itself can return to a previously visited state and use the stored relational history there. This will test whether the same mechanism survives when the probe state is generated internally rather than imposed by the experimenter.
