# EXP-AUDIO-001 — Audio Foundation

## Goal
Build a provider-independent audio organ for voice input and later speech output while preserving the original audio as evidence.

## Current scope
- deterministic WAV inspection;
- SHA-256 fingerprint of raw audio;
- PCM16 mono energy-based VAD;
- explicit STT adapter contract;
- explicit TTS adapter contract;
- no transcript invention when STT is absent.

## Fixed architecture

`microphone/source → raw audio → fingerprint → VAD → STT adapter → text → memory`

Future output path:

`text → TTS adapter → audio response`

## Integrity rule
The raw audio record remains the source of truth. Any transcript must be linked to the source SHA-256 and provider metadata. If transcription is unavailable, the transcript field stays null.

## Benchmark
Synthetic WAV contains silence followed by a deterministic tone. The benchmark verifies metadata, stable SHA-256, VAD detection, and explicit refusal to invent a transcript.

## Not yet proven
- real microphone capture on target hardware;
- speech recognition accuracy;
- noisy-room robustness;
- speaker diarization;
- TTS quality;
- end-to-end voice conversation.

Those require separate controlled experiments and, where applicable, external STT/TTS adapters.
