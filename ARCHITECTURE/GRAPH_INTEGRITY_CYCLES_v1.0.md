# GRAPH INTEGRITY & CYCLES v1.0

## Rule

Nodes, edges, graphs and intentional cycles are first-class system structure. Loss of any of these can change system behavior even when all individual files remain readable.

## Required invariants

1. Every edge endpoint references an existing node.
2. Node identifiers are unique.
3. Edge direction and edge type are preserved.
4. Graph membership is preserved.
5. Intentional feedback cycles are preserved.
6. Cycle loss is reported as structural damage, not silently normalized away.
7. A graph that reconstructs nodes but changes critical edges/cycles is not considered lossless.
8. Recovery must compare the reconstructed graph with the recorded provenance, not merely count nodes.

## Cycle classes

- control loops;
- feedback loops;
- dependency cycles;
- redundancy/failover loops;
- recovery loops.

Cycles are not automatically errors. A cycle is an error only when it violates the graph's declared topology or policy.

## Verification order

`nodes → edges → graph membership → connectivity → cycles → semantics → provenance`

## Failure response

If an invariant fails:

`detect → freeze affected graph → identify missing structure → recover from local history → compare trusted archive → query peer Space if authorized → mark unresolved loss`

Never silently invent a missing edge or cycle.

## Acceptance

The benchmark fixture must preserve:

`Space → Vision → Memory → Recovery → Space`

and

`Space ↔ Guardian`

as intentional feedback structures.

## Status

🟢 invariant specification fixed
🟢 executable benchmark added
🟡 integration with all graph-producing organs pending
🟡 damage-injection coverage pending
