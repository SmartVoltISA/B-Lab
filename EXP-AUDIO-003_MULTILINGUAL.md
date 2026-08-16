# EXP-AUDIO-003 — Multilingual voice input

## Goal

Make language selection a first-class part of Ω-AUDIO instead of hard-coding Russian.

## Initial language set

Russian (`ru`), Kazakh (`kk`), English (`en`), German (`de`), French (`fr`), Spanish (`es`), Italian (`it`), Portuguese (`pt`), Dutch (`nl`), Polish (`pl`), Ukrainian (`uk`), Belarusian (`be`), Czech (`cs`), Slovak (`sk`), Bulgarian (`bg`), Serbian (`sr`), Croatian (`hr`), Romanian (`ro`), Hungarian (`hu`), Turkish (`tr`), Arabic (`ar`), Persian (`fa`), Hebrew (`he`), Hindi (`hi`), Bengali (`bn`), Urdu (`ur`), Chinese (`zh`), Japanese (`ja`), Korean (`ko`), Vietnamese (`vi`), Thai (`th`), Indonesian (`id`), Malay (`ms`), Uzbek (`uz`), Mongolian (`mn`) and additional Whisper-supported languages can be added without changing the core.

Whisper's multilingual models cover a broad language set; English-only `.en` models must not be used for non-English speech. Explicit language selection is preferred for controlled benchmarks because it avoids language-detection overhead and possible short-clip misclassification. citeturn0search2turn0search4

## Runtime rule

- user selects language → use that language;
- `auto` → language detection is allowed and detected language must be recorded;
- unsupported code → reject;
- no provider/model → no transcript;
- never silently translate unless translation is explicitly requested.

## Benchmark

Each language must eventually have fixed reference audio and human transcript. Measure WER/CER, latency, memory, noise robustness and failure cases under identical conditions. Do not infer quality from model language support alone.

## Status

🟡 multilingual registry and validation implemented; real multilingual audio corpus pending.
