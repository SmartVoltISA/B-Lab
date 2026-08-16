# EXP-AUDIO-004 — Multilingual Language Corpus

## Purpose

Build a controlled corpus for language identification and speech-to-text evaluation without claiming quality before real audio is measured.

## Reference design

The corpus follows a proven community-data pattern: collect sentences, record speech, validate clips, retain metadata, and keep rejected/uncertain material traceable. Mozilla Common Voice uses scripted speech, spontaneous speech, community validation and language variants; its current project reports public speech datasets in 130+ languages. This experiment uses those practices as an external reference, not as a copy of their dataset.

## Initial languages

ru, kk, en, uk, uz, tr, de, fr, es, it, ar, zh, ja, ko, hi, mn, pl.

The registry remains extensible. Language support means the pipeline can accept and route that language; it does not mean equal recognition quality.

## Corpus strata

Each language should contain:

1. scripted read speech;
2. spontaneous speech;
3. clean microphone recordings;
4. controlled background noise;
5. fast speech;
6. slow speech;
7. multiple speakers;
8. optional dialect/variant labels;
9. code-switching samples where linguistically appropriate.

## Record schema

Each sample must preserve:

- `audio_id`
- `language`
- `language_variant`
- `speaker_id` (pseudonymous)
- `text_reference`
- `audio_sha256`
- `duration_ms`
- `sample_rate`
- `channels`
- `condition`
- `noise_level`
- `speaking_rate`
- `validation_status`
- `transcript`
- `language_confidence`
- `wer`
- `cer`
- `latency_ms`
- `memory_mb`

## Language identification rule

Manual language selection and automatic language identification are separate modes.

- `manual`: the requested language is fixed before STT;
- `auto`: language ID produces a candidate language and confidence;
- `mixed`: segments may carry different language labels.

A low-confidence language decision must remain low-confidence. The system must not silently replace it with a stronger claim.

## Evaluation

For each language:

- Language-ID accuracy;
- WER where word segmentation is meaningful;
- CER for character-oriented evaluation;
- exact-match rate;
- latency;
- memory usage;
- failure rate;
- noise degradation;
- speaker variation;
- mixed-language performance.

## Controls

No synthetic transcript is accepted as an STT result. Every measured transcript must reference a real audio sample and a fixed human/reference transcript.

External datasets may be used as evaluation/training sources only after license, provenance, language, speaker metadata and split contamination are checked.

## Status

🟡 Protocol fixed. Real multilingual corpus and hardware benchmark pending.

## External references

- Mozilla Common Voice: public community speech-data workflow and validation model.
- OpenAI Whisper model card: multilingual ASR training and evidence that per-language performance depends on the amount of training data for that language.
