# B-Lab Capability Matrix v1.0

## Purpose

Inventory what already exists, what is partially implemented, and what still needs to be built before deployment to Space hardware.

## Core

| Capability | Status | Next verification |
|---|---|---|
| Nodes/edges/graphs | 🟢 | integrity + recovery stress tests |
| Provenance/history | 🟢 | end-to-end provenance audit |
| Trust/confidence | 🟡 | calibration benchmark |
| Lossless structural archive | 🟡 | rerun after edge-order fix |
| Data compression | 🟡 | benchmark vs external compressors |
| User/Space memory boundary | 🟢 architecture | implementation + security tests |
| Permission gate | 🟡 | runtime enforcement |
| Memory deletion/isolation | 🟡 | deletion-cascade benchmark |

## Perception

| Capability | Status | Next verification |
|---|---|---|
| Text input | 🟢 | semantic error guard |
| Multilingual STT | 🟡 | real corpus benchmark |
| ASR error guard | 🟢 rule / 🟡 runtime | injected-error tests |
| JPEG/PNG vision intake | 🟢 | real image fixtures |
| Object detection | 🟢 benchmark | broader fixtures |
| Segmentation | 🟢 benchmark | masks/occlusion |
| Pose/keypoints | 🟢 benchmark | human/animal fixtures |
| Video tracking | 🟢 benchmark | identity consistency |
| OCR | ⚪ | build benchmark |
| Audio event recognition | ⚪ | build benchmark |
| Speaker identification | ⚪ | privacy-gated benchmark |
| Depth/spatial perception | ⚪ | build benchmark |
| Scene understanding | 🟡 architecture | graph benchmark |
| Object part decomposition | 🟡 architecture | implement graph extractor |
| Cross-modal linking | ⚪ | audio↔vision↔text experiment |

## Reasoning / action

| Capability | Status |
|---|---|
| Graph-based retrieval | 🟡 |
| Tool selection | 🟡 |
| Adaptive tool creation/selection | ⚪ |
| Planning | 🟡 |
| Verification loop | 🟢 principle / 🟡 runtime |
| Autonomous task execution | ⚪ |
| Web research with provenance | 🟡 |
| Code analysis/testing | 🟡 |
| Safe code/security testing | ⚪ — authorization boundary required |

## Security / legal

| Capability | Status |
|---|---|
| User-data isolation | 🟢 architecture |
| Encryption at rest | 🟡 |
| Encryption in transit | 🟡 |
| Access control | 🟡 |
| Consent records | 🟡 |
| Jurisdiction policy engine | ⚪ |
| Audit trail | 🟢 foundation / 🟡 full implementation |
| Data export/delete | ⚪ |
| Retention policies | ⚪ |

## Hardware / deployment

| Capability | Status |
|---|---|
| Phone microphone UI | 🟡 unfinished |
| Phone camera UI | ⚪ |
| Local inference | 🟡 |
| Model/resource management | ⚪ |
| Offline mode | ⚪ |
| Installable compact memory package | 🟡 architecture |
| Hardware benchmark | ⚪ |

## Rule

A capability is not marked 🟢 merely because a library or external product exists. It becomes 🟢 for B-Lab only after a reproducible local test passes and provenance is recorded.

External projects are references/benchmarks, not automatic dependencies.

## Priority order

1. Graph Core + provenance + trust.
2. Memory boundaries + permissions + deletion/security.
3. Vision object → parts → relations.
4. OCR and document perception.
5. Audio/STT error guard + multilingual corpus.
6. Cross-modal graph fusion.
7. Tool selection/planning.
8. Hardware/phone integration.
9. Legal policy engine by jurisdiction.
10. Full-system benchmark.
