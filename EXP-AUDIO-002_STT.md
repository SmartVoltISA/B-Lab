# EXP-AUDIO-002 — STT accuracy and provider boundary

## Goal

Move Ω-AUDIO from an audio-only foundation toward measurable speech-to-text without coupling the laboratory core to one provider.

## Implemented

- optional local Faster-Whisper adapter;
- explicit transcript object with provider/model/language metadata;
- deterministic Word Error Rate (WER) metric;
- CI scoring benchmark without downloading a model;
- no-transcript/no-provider rule remains unchanged.

## External baseline considered

Faster-Whisper is a CTranslate2 reimplementation of Whisper and reports lower memory use and faster inference than the reference implementation under its published benchmark conditions. This is a candidate provider, not a claim that it is universally best.

## Scientific rule

Real STT accuracy is **not** claimed by the CI scoring benchmark. It requires a fixed audio corpus with human reference transcripts.

## Next experiment

Build a small fixed Russian-language corpus with clean speech, background noise, different speaking rates, and multiple speakers. Measure WER/CER, latency, CPU/RAM usage, and failure cases on the same model/settings.

## Status

🟡 STT adapter implemented; real corpus benchmark pending.
