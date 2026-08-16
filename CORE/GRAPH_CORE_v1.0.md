# B-Lab Graph Core v1.0

## Purpose

Provide one structural contract for every B-Lab organ: text, audio, vision, video, memory, tools, and future sensors.

## Fundamental cycle

`whole -> parts -> nodes -> edges -> graph -> whole`

The reverse direction is mandatory. A graph is not only an output format; it is the recoverable structure that allows the system to reconstruct a whole from verified parts and relations.

## Node contract

Every node MUST have:

- `node_id`
- `type`
- `value`
- `source_id`
- `created_at`
- `status`
- `confidence`
- `trust`
- `provenance`
- `memory_scope`

## Edge contract

Every edge MUST have:

- `edge_id`
- `from`
- `relation`
- `to`
- `source_id`
- `confidence`
- `trust`
- `provenance`
- `created_at`
- `status`

## Provenance

No node or edge may become durable knowledge without a trace to its source observation, derivation, or explicit user input.

Sources may include:

- microphone/audio
- camera/image/video
- text/user input
- external document
- web source
- tool result
- previous graph state
- verified inference

## Observation vs knowledge

Raw perception is an observation. It is not automatically a fact.

`observation -> validation -> verified node/edge -> memory`

An uncertain ASR result, detector output, OCR result, or model inference MUST remain marked as an observation until validation rules allow promotion.

## Contradiction handling

Contradictory observations are retained as history. The system MUST NOT silently overwrite the previous state. A later verified observation may supersede an earlier one while preserving the complete chain.

## Memory scopes

- `SPACE`: system-derived architecture, experiments, verified general knowledge.
- `USER:<id>`: private user data and user-specific memory.
- `SESSION:<id>`: temporary working context.
- `SHARED:<scope>`: explicitly authorized shared knowledge.

Cross-scope promotion requires an explicit permission record and provenance.

## Integrity

Graph serialization MUST preserve:

1. every node;
2. every edge;
3. edge direction;
4. edge relation;
5. node/edge identifiers;
6. provenance;
7. memory scope;
8. ordering metadata where ordering is semantically meaningful.

Exact byte ordering is not required unless declared part of the source contract; semantic graph equivalence is required. If the source contract explicitly declares edge order meaningful, that order becomes part of the integrity test.

## Verification

A graph can be promoted to durable memory only when:

`integrity PASS + provenance PASS + scope PASS + trust threshold PASS`

If any gate fails, preserve the failed state and do not present it as verified.

## Organ interface

Each organ must expose the same conceptual operations:

`observe -> normalize -> create/update graph -> verify -> store -> retrieve -> explain`

This allows Audio, Vision, OCR, Video, and future organs to exchange structure without requiring one another to share implementation details.

## Status

Architecture contract created. Runtime implementation and benchmark remain separate work items and must not be marked complete until executed tests pass.
