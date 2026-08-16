# EXP-AUDIO-005 — ASR Error Guard

## Incident

A live voice test produced a semantic substitution: the user said `это`, while speech recognition returned `Бета`. The assistant then incorrectly treated the ASR output as a factual architectural term and built reasoning from it.

## Finding

ASR output is an observation, not a fact. A transcription error must never automatically create, modify, or strengthen a memory node, graph edge, user fact, or architectural rule.

## Required pipeline

`audio → ASR → confidence/alternatives → semantic plausibility check → confirmation when needed → graph/memory`

## Guard rules

1. Preserve raw ASR output exactly as an observation.
2. Keep ASR confidence and alternatives when available.
3. Do not promote low-confidence or semantically disruptive substitutions to memory.
4. If a single word changes the meaning of the request materially, request confirmation or use a second recognition pass.
5. Keep user-provided content separate from Space-derived knowledge.
6. Record provenance: audio/session, ASR engine, model/version, language, timestamp, confidence, and verification status.
7. Never silently rewrite a user's intended term because another term looks more plausible to the model.
8. Benchmark this guard with deliberate homophone/near-word and multilingual errors.

## Acceptance test

Input intent: `это`.

Injected ASR output: `Бета`.

Expected:
- raw observation = `Бета`;
- intended user term is not assumed to be `Бета`;
- no new `Бета` architecture node is created;
- system requests/requires confirmation before semantic promotion;
- incident is archived as an ASR failure case.

## Status

🟢 Rule defined and archived.
🟡 Runtime enforcement and benchmark integration pending.
