# B-Lab — Architecture

## Core loop

```text
state
  ↓
distinction
  ↓
transition / relation
  ↓
observation
  ↓
memory
  ↓
structure
  ↓
comparison
  ↓
archive
  ↺
```

## Layers

```text
B-Lab
├── Foundation
│   └── 0 / 1
├── Generator
│   └── states and transitions
├── Observer
│   └── relations, repetitions, cycles
├── Memory
│   └── local history / confirmed observations
├── Structure
│   └── nodes, edges, graphs, cycles
├── Comparator
│   └── experiment ↔ formal mathematics
├── Visualization
│   └── matrices / graphs / transition diagrams
└── Archive
    └── immutable experimental history
```

## Independence rule

Experimental generation and formal mathematical comparison are separate layers.

The generator must not use the formal model to manufacture its own result. The comparator receives the result after the experiment has completed.

## First implementation boundary

Phase 0 does not attempt to create an autonomous learning system. It creates a reproducible laboratory where increasingly complex binary structures can be generated, observed, compared and archived.
