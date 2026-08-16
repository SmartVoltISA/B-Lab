# SPACE IDENTITY + RECOVERY ARCHITECTURE v1.0

## Purpose
Define how Spaces identify one another, communicate, verify state, detect loss, recover information, and report recovery results without relying on human support for routine failures.

## Space identity
Every Space has a stable cryptographic identity, separate from a display name.

Required identity fields:
- `space_id` — stable unique identifier;
- `key_id` — identifier of the active public-key credential;
- `owner_scope` — ownership/administrative scope;
- `capabilities` — explicitly granted capabilities;
- `trust_state` — current trust status;
- `created_at` / `rotated_at` — lifecycle metadata.

A display label such as `Sasha`, `GPT`, `Vasya`, or `Petya` is metadata only and must never be used as the security identity.

Space-to-Space communication must authenticate the peer and verify message integrity before accepting state or instructions.

## Separate roles

### SPACE
Executes authorized cognitive and application work. It may request recovery, compare state, and exchange verified information with another Space.

### GUARDIAN
Independently observes integrity, identity, dependencies, recovery operations, and authority boundaries. Guardian receives recovery telemetry and produces health/recovery reports for Space.

### RECOVERY ORGAN
A dedicated recovery subsystem performs diagnosis and reconstruction. It reports evidence and confidence; it does not silently declare uncertain reconstruction to be original data.

Flow:

`SPACE ↔ SPACE`

`ORGANS → RECOVERY → GUARDIAN → SPACE`

`RECOVERY ↔ VERIFIED PEER SPACE / ARCHIVE / ROOT SOURCE`

## Recovery pipeline

1. Inventory expected nodes, edges, files, indexes, metadata, and checksums.
2. Compare current state against the last known valid manifest.
3. Classify every difference:
   - present and valid;
   - missing;
   - corrupted;
   - inconsistent;
   - unknown.
4. Attempt local reconstruction from redundant information and archived history.
5. If unresolved, search the root/archive source.
6. If still unresolved, request comparison from an authenticated peer Space where policy permits.
7. Reconstruct only when evidence supports it.
8. Verify reconstructed state against hashes, graph constraints, provenance, and dependency rules.
9. Mark unresolved information explicitly as `UNKNOWN/LOST`, never as recovered fact.
10. Produce a recovery report.

## Recovery report

Every run must report at minimum:

- total objects inspected;
- valid objects;
- missing objects;
- corrupted objects;
- repaired objects;
- reconstructed objects;
- unrecoverable objects;
- nodes recovered;
- edges recovered;
- graphs recovered;
- files/bytes recovered;
- provenance completeness;
- confidence of reconstruction;
- sources used;
- operations performed;
- unresolved dependencies;
- final integrity status.

Example:

`Inspected: 10,000 nodes`
`Recovered: 9,970`
`Unrecoverable: 30`
`Edges restored: 99.8%`
`Provenance complete: 99.6%`
`Status: DEGRADED — 30 nodes unresolved`

Numbers must be measured, never estimated for presentation.

## Graph recovery

A graph is considered lossless only when all required node identities, edge identities, edge direction/type, attributes, provenance, and ordering constraints defined by the graph contract are restored.

If a graph can be semantically reconstructed but not exactly restored, the result must be classified separately:

- `EXACT_RECOVERY`
- `STRUCTURAL_RECOVERY`
- `SEMANTIC_RECOVERY`
- `PARTIAL_RECOVERY`
- `UNRECOVERABLE`

This prevents semantic similarity from being falsely reported as exact recovery.

## Peer Space comparison

A Space may ask another authenticated Space for comparison data when local recovery fails and policy permits.

Peer exchange must use:
- authenticated Space identity;
- scoped request;
- provenance of supplied data;
- integrity verification;
- explicit trust decision;
- audit record.

A peer Space is an evidence source, not an unquestioned authority.

Conflicting peer results must remain separate until independently verified.

## Root-source escalation

Recovery priority:

`local redundant state → local archive/history → root source → authenticated peer Space → human escalation`

Human support is the final escalation path, not the normal recovery mechanism.

## Safety rules

- Never overwrite original surviving evidence during recovery.
- Never convert a guess into a trusted node.
- Preserve damaged input for forensic comparison.
- Every reconstruction has provenance.
- Recovery cannot silently modify User Memory.
- Guardian can quarantine a failed recovery result.
- Space cannot suppress a recovery failure report.
- Guardian cannot fabricate successful recovery.

## Planned benchmark

Failure injection must test:
- missing node;
- missing edge;
- damaged graph;
- corrupted file;
- deleted index;
- broken provenance;
- conflicting peer Space;
- unavailable root archive;
- partial disk failure;
- interrupted recovery.

Acceptance requires measured recovery percentage and correct classification of unresolved information.

## Status

🟢 Space identity model defined
🟢 peer authentication concept defined
🟢 recovery escalation path defined
🟢 recovery reporting contract defined
🟢 exact vs structural vs semantic recovery separated
🟡 runtime implementation pending
🟡 cryptographic key lifecycle implementation pending
🟡 failure-injection benchmark pending
