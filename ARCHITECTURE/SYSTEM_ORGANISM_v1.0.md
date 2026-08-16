# B-Lab — System Organism Architecture v1.0

## Purpose

Define the whole Space as a structured organism of organs, sub-organs, communication channels, state transport, guardianship, redundancy and dependency relationships.

This is an architecture model, not a claim that Space literally has biological nervous or circulatory systems.

## Core law

Every subsystem is decomposable:

`whole -> graph -> nodes -> edges -> parts`

and reconstructible:

`parts -> edges -> nodes -> graph -> whole`

No subsystem is considered complete if its internal dependencies, interfaces, provenance and recovery path are unknown.

## Organ hierarchy

`Space`
- brain/core — reasoning, world model, planning, synthesis
- memory — working, temporary, long-term and archived state
- perception — text, audio, image, video, OCR, spatial sensing
- action/tools — external and local capabilities
- nervous system — low-latency coordination/control signals between organs
- information circulation — transport of state, artifacts, events and knowledge
- guardian — integrity, policy, anomaly detection, dependency protection and recovery coordination
- immune/security — isolation, authentication, authorization, threat handling
- energy/resource layer — compute, storage, bandwidth, model/runtime budgets
- interface — user/device/environment interaction

Each organ has the same recursive structure: organ -> sub-organs -> nodes -> edges -> graph.

## Nervous system

The nervous system is the control plane.

Responsibilities:
- route events and control signals;
- publish state changes;
- coordinate organs without forcing every organ to know every other organ;
- detect unavailable dependencies;
- trigger retries, fallback or safe shutdown;
- carry urgency/priority/deadline metadata;
- preserve provenance of control decisions.

It must not become an uncontrolled global mutable state.

## Information circulation

The information-circulation layer is the data/state plane.

It transports:
- observations;
- structured graph updates;
- artifacts;
- model outputs;
- confidence/trust;
- provenance;
- tasks/results;
- health/state snapshots.

Each message/artifact carries at minimum:
`id, source, destination, type, timestamp, version, provenance, confidence, integrity_hash, sensitivity_scope`.

This is analogous to circulation only as an engineering metaphor: it transports information/state rather than biological material.

## Guardian

Guardian is an independent oversight layer.

It monitors:
- organ health;
- communication failures;
- integrity violations;
- contradictory states;
- unexpected dependency loss;
- permission violations;
- memory contamination;
- resource exhaustion;
- suspicious tool behaviour.

Guardian must be able to observe the nervous and circulation layers without being dependent on the exact component it is supervising.

## Dependency graph

For every organ `A -> B`, store:
- dependency type: hard / soft / optional;
- function affected;
- minimum capability required;
- fallback capability;
- degradation mode;
- recovery procedure;
- whether A can operate independently;
- whether B can be replaced or migrated.

### Independence test

Never move or delete a duplicated capability merely because it appears duplicated.

Run:
1. isolate candidate capability;
2. execute organ A without it;
3. compare outputs and invariants;
4. execute dependent organ B without it;
5. measure information loss, latency, reliability and graph integrity;
6. restore and compare;
7. only then classify the dependency as removable, redundant, complementary or critical.

## Duplication / redundancy

Duplicates are not automatically waste.

Classify each duplicate as:
- exact duplicate — one can potentially be removed;
- complementary — both provide different information;
- redundant safety path — keep both;
- fallback — keep dormant/low-resource;
- conflicting duplicate — requires arbitration;
- unknown — do not delete until tested.

## Failure model

A failure in one organ must not silently become a fact in another organ.

Flow:
`failure -> observation -> quarantine -> diagnosis -> recovery/fallback -> verification -> graph update`.

Example: ASR returning `Бета` for spoken `это` is an observation error, not a new semantic node.

## Shared-state architecture

External research increasingly uses shared-state/blackboard patterns because sequential message passing can lose information between agents. Recent work reports materially higher information fidelity for shared structured state than message-only pipelines. This supports using a versioned graph/state fabric for Space, but does not by itself validate our implementation.

## Memory boundaries

`SPACE MEMORY` and `USER MEMORY` remain separate domains.

Crossing requires explicit permission, provenance, purpose and policy checks.

The nervous system may carry references to user data without copying the underlying private content into Space memory.

## Recursive organ contract

Every organ must expose:
- identity;
- purpose;
- inputs;
- outputs;
- internal graph;
- dependencies;
- health state;
- resource requirements;
- trust/confidence;
- provenance;
- fallback;
- recovery;
- security scope;
- tests;
- version.

## Current status

Architecture: 🟢 defined
Runtime nervous system: 🟡 not yet implemented
Information circulation: 🟡 partially represented by existing provenance/graph work
Guardian: 🟡 architectural concept; runtime implementation pending
Dependency/redundancy benchmark: ⚪ next experiment
Full organism health model: ⚪ next experiment

## Rule

Do not claim that an organ is independent, redundant, safe to remove, or replaceable without an isolation benchmark.
