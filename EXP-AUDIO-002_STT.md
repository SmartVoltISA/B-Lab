# EXP-AUDIO-002 — Real STT evaluation

## Goal
Measure actual speech-to-text quality instead of testing only the adapter contract.

## Primary metrics
- WER (word error rate)
- exact-match rate
- latency / real-time factor
- RAM / VRAM
- failure rate

## Corpus
Russian speech with fixed audio SHA-256 and fixed human reference transcript.

## Conditions
1. clean speech;
2. background noise;
3. fast speech;
4. slow speech;
5. multiple speakers / overlap.

## Candidate
First local candidate: faster-whisper. Its upstream project publishes WER and speed/memory benchmarks, but those numbers are not transferred to B-Lab; B-Lab must measure its own corpus and hardware.

## Rule
No transcript is accepted as evidence unless it comes from an actual configured STT provider. Missing provider = `null`, never an invented transcript.

## Status
Protocol registered. Real Russian corpus execution remains a hardware/model experiment and is not claimed by CI until actually run.
