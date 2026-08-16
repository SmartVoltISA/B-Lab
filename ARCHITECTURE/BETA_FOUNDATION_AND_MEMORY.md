# BETA — Foundation, Graph, Memory and Data Boundaries

## Status

🟡 Architectural foundation fixed.

This document defines a non-negotiable architectural rule for B-Lab / Ω-Space: every higher capability is constructed from small verified elements and their relations. Memory is split into Space knowledge and user-private knowledge. No user-private memory becomes Space knowledge without explicit permission and a legally valid basis.

---

## 1. BETA — the foundation

`BETA` is the minimal structural layer from which the system grows.

Core principle:

`small → relation → node → graph → whole`

and the reverse reconstruction:

`whole → graph → nodes → relations → parts`

The system must support both directions continuously.

A whole is never treated as an indivisible truth. It can be decomposed into constituent elements and relations. Elements can then be recombined into larger structures.

### Non-negotiable rule

**Nothing higher in the stack is allowed to bypass the graph.**

Perception, reasoning, memory, learning, user context, hypotheses and derived knowledge must have a structural representation in nodes and relations where applicable.

---

## 2. The universal cycle

The base cycle is:

`observe → decompose → identify elements → connect → build graph → form whole → test → decompose again → compare → update`

The cycle is not a one-time pipeline. It is recurrent.

Every new observation may:

- confirm an existing node;
- create a new node;
- modify a relation;
- invalidate a relation;
- split one node into several nodes;
- merge several nodes into a higher-level whole;
- create a new hypothesis;
- change confidence without rewriting historical evidence.

Historical observations must remain distinguishable from later interpretations.

---

## 3. Graph as the common structural language

The graph is the primary integration layer.

### Node

A node represents an identifiable element, observation, state, concept, object, event, user-private fact, hypothesis, model result, or other explicitly typed entity.

### Edge

An edge represents a relation between nodes.

Every important edge should carry, where applicable:

- relation type;
- source and target;
- confidence;
- provenance;
- creation time;
- last verification time;
- status (`active`, `uncertain`, `invalidated`, `superseded`);
- scope (`space`, `user`, `shared/consented`);
- evidence reference.

### Graph

A graph is not merely a database format. It is the system's structural representation of how elements belong together.

---

## 4. Two memory domains

The system must maintain two logically and operationally separated memory domains.

### A. SPACE MEMORY

Contains knowledge belonging to the Space itself, including:

- system-derived structural knowledge;
- verified experiments;
- models and model behaviour;
- reusable algorithms;
- general hypotheses;
- validated patterns;
- architecture;
- lessons derived from non-private evidence;
- provenance and verification history.

Space Memory must not silently absorb personal user data.

### B. USER MEMORY

Contains information belonging specifically to a user, including:

- personal facts;
- personal preferences;
- personal history;
- private projects;
- private conversations where retained;
- personal relationships;
- private documents and observations;
- user-specific graphs and associations.

User Memory is private by default.

**User Memory and Space Memory are different trust domains.**

---

## 5. Boundary between the domains

Default rule:

`USER MEMORY ≠ SPACE MEMORY`

No automatic promotion is permitted.

A user-private fact may influence the user's own Space instance when permitted, but that does not make it global Space knowledge.

Promotion from User Memory into reusable Space knowledge requires an explicit consent event and must preserve the required legal/provenance metadata.

Conceptually:

`user data → permission gate → legal/purpose gate → de-identification/minimization where required → validation → Space-derived knowledge`

If any gate fails, the data remains in User Memory or is excluded.

---

## 6. Permission must be granular

A single permanent "allow everything" switch is not sufficient as the architectural target.

Consent should be capable of being scoped by:

- purpose;
- data category;
- experiment/project;
- retention period;
- jurisdiction;
- whether the data may improve the Space;
- whether derived/non-identifying information may be reused;
- withdrawal status.

The system must be able to record the consent event and its version.

Withdrawal must stop future use and trigger the applicable downstream handling rules. Previously produced aggregate or irreversible derived results require separate legal/technical treatment and must not be falsely represented as erasable when they are not.

---

## 7. Security boundary

User Memory requires stronger isolation than ordinary Space knowledge.

Target architecture:

`identity → authorization → memory scope → encrypted storage → audit trail → controlled retrieval`

At minimum the design must account for:

- encryption in transit and at rest;
- least-privilege access;
- separation of user identifiers from reusable analytical data where feasible;
- audit logging;
- retention and deletion policies;
- backup lifecycle;
- export and portability;
- breach response;
- model/training access controls;
- administrator access controls.

Security claims must be verified by implementation and testing. Documentation alone is not evidence of security.

---

## 8. Legal layer — jurisdiction aware

Legal compliance is a separate architectural layer, not a paragraph added after implementation.

The system must maintain a jurisdiction registry rather than assuming one global rule.

Conceptual structure:

`jurisdiction → applicable law → data categories → lawful basis/consent rules → rights → retention → transfer rules → security obligations → operational controls`

The initial implementation should be designed to support country/region-specific policy modules.

Examples of jurisdictions that require dedicated treatment include:

- Kazakhstan;
- European Union / EEA;
- United Kingdom;
- United States, including state-level regimes;
- Canada;
- Australia;
- Brazil;
- China;
- India;
- Japan;
- South Korea;
- other jurisdictions as deployment expands.

This list is not a legal conclusion and is not exhaustive.

Before deployment in a jurisdiction, the applicable requirements must be verified against current primary legal sources and, where appropriate, qualified legal counsel.

---

## 9. Legal design principles

The architecture should be capable of implementing, where applicable:

- purpose limitation;
- data minimization;
- transparency;
- lawful processing basis;
- consent management;
- access rights;
- correction;
- deletion/erasure;
- restriction/objection;
- portability;
- retention limits;
- security safeguards;
- data-transfer controls;
- children's data protections;
- sensitive/special-category data controls;
- automated decision-making safeguards where applicable;
- records of processing and auditability.

Exact obligations depend on jurisdiction, data type, role of the operator, processing purpose and deployment model.

---

## 10. Provenance is mandatory

Every persistent semantic claim should be traceable to its origin.

Minimum conceptual chain:

`source → observation → transformation → inference → node/edge → memory`

The system must distinguish:

- observed fact;
- model prediction;
- derived relation;
- hypothesis;
- verified conclusion;
- user-provided fact;
- Space-generated knowledge.

A prediction must never silently become a fact merely because it was stored.

---

## 11. No destructive rewriting of knowledge

When knowledge changes, the preferred operation is versioning rather than erasure of history.

Example:

`relation R = probable`

→ new evidence

`relation R = confirmed`

or:

`relation R = invalidated`

The historical state remains available for reproducibility and audit where legally permitted.

User deletion requirements remain authoritative over technical convenience.

---

## 12. Development order

The system should be grown in the following order:

1. BETA structural primitives.
2. Nodes.
3. Typed relations.
4. Graph construction.
5. Graph decomposition/reconstruction cycle.
6. Evidence and provenance.
7. Space Memory.
8. User Memory isolation.
9. Permission/consent gate.
10. Security controls.
11. Jurisdiction policy layer.
12. Learning/promotion pipeline.
13. Higher semantic capabilities.

Do not build higher layers by bypassing an unverified lower layer.

---

## 13. Test requirements

Each layer requires a positive and negative test.

Examples:

- Can a graph be reconstructed from nodes and edges?
- Can a whole be decomposed without losing provenance?
- Can User Memory be retrieved without exposing another user's memory?
- Can a user deny Space reuse while retaining their private memory?
- Can consent be withdrawn?
- Can a Space model distinguish user-provided facts from general knowledge?
- Can an invalidated relation remain historically traceable without being treated as active?
- Can jurisdiction policy change without rewriting the underlying graph?

A layer is not considered complete until its failure modes have also been tested.

---

## 14. Core invariant

> **The Space grows from relations. Memory preserves the relations. User privacy defines the boundary. Permission controls crossing that boundary. Law defines the operating envelope.**

This invariant applies to vision, reasoning, learning, memory, agents and future organs of the system.
