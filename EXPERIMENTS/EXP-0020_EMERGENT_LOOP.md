# EXP-0020 — Emergent Loop Formation

## Status

**PASS for emergent cycle formation under the tested plasticity rule. MEMORY→BEHAVIOR coupling remains UNRESOLVED.**

## Question

Can a directed cycle appear when no cycle is present initially, if relations are allowed to change according to a local rule?

## Initial topology

Acyclic directed graph with equal controls:

```text
A → B → C → D
A → D
```

No directed cycle exists at t=0.

Each relation has a persistent memory value.

## Plasticity rule

After traversing an edge u→v, its memory is reinforced:

```text
m_uv(t+1) = min(1, 0.9*m_uv(t) + 0.6)
```

Other memories decay by 0.9.

When the just-traversed relation reaches memory >= 0.5, the system may create the reverse relation v→u with probability 0.35 if that relation is absent.

This rule was fixed before the sweep.

## Controls

A — dynamic topology + persistent memory

B — frozen topology + persistent memory

C — dynamic topology + memory reset/decay without persistence

D — frozen topology + no persistent memory

## Sweep

1000 independent seeds per condition.

### A — dynamic topology + persistent memory

- cycle appeared in **723/1000 runs = 72.3%**
- mean final edge count: **4.723**
- mean first cycle-creation time among successful runs: **1.69 steps**

### B — frozen topology + persistent memory

- cycle: **0/1000**
- mean edges: **4.0**

### C — dynamic topology + memory reset

- cycle: **0/1000**
- mean edges: **4.0**

### D — frozen topology + no persistent memory

- cycle: **0/1000**
- mean edges: **4.0**

## Result

Under this particular plasticity rule, cycle formation required both:

1. structural plasticity;
2. persistent edge state reaching the creation threshold.

The frozen-topology control confirms that the cycle was not present initially.

The memory-reset control confirms that the tested plasticity mechanism did not form cycles without persistent relational state.

## Important negative result

The experiment did **not** yet demonstrate that the newly formed cycle automatically produces history-dependent behavior.

The current action policy selects the outgoing edge with the highest memory. Because the same reinforcement mechanism also determines the action, the policy can remain locked to the same strongest relation. Therefore the experiment does not cleanly isolate:

```text
cycle formation → changed future action
```

This is a confound, not a failure of the cycle-formation result.

## Interpretation

The current evidence supports:

```text
acyclic structure
  +
local structural plasticity
  +
persistent relational state
→
emergent directed cycle
```

It does not yet establish that an emergent cycle is sufficient for self-reference.

## Next experiment

**EXP-0021 — Emergent Cycle → Independent Read-Back Probe**

Separate structural plasticity from action selection.

The system should form a cycle using one memory variable, while a second, independent probe reads relational memory to choose between two actions.

Required comparison:

- same visible probe state;
- same external input;
- different prior histories;
- cycle absent vs cycle present;
- memory present vs reset.

Primary metric:

```text
H = P(action_t differs | same visible state + same input, different history)
```

This will test whether the emergent cycle is merely a structural loop or becomes a causal self-reference mechanism.
