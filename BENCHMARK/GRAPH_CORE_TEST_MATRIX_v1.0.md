# Graph Core Test Matrix v1.0

| Test | Expected |
|---|---|
| create node | node_id + provenance present |
| create edge | endpoints + relation + provenance present |
| graph round-trip | all nodes/edges preserved |
| direction preservation | every directed edge unchanged |
| relation preservation | edge semantics unchanged |
| provenance preservation | source chain recoverable |
| scope isolation | USER data cannot appear in SPACE scope without permission |
| session isolation | SESSION data cannot leak across sessions |
| contradiction | old state retained, supersession explicit |
| uncertain observation | cannot silently promote to durable fact |
| ASR substitution | `это` vs `Бета` remains an observation/error until verified |
| vision decomposition | object and part nodes linked with typed relations |
| cross-modal link | audio/image/text nodes link through explicit provenance |
| deletion cascade | derived representations are identified and tested for residual leakage |
| corruption detection | modified graph fails integrity verification |
| recovery | valid graph reconstructs semantically identical structure |

## Gate

No green status without an executed reproducible test.

## Priority

P0: round-trip, provenance, scope isolation, corruption detection.
P1: contradiction, uncertain observation, deletion cascade.
P2: cross-modal links and performance.
