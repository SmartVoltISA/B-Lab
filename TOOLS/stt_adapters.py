"""Optional STT adapters for Ω-AUDIO-1.

The laboratory core remains provider-independent. The Faster-Whisper adapter is
optional and imported only when used, so CI does not download models or silently
turn external services into a dependency.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Transcript:
    text: str
    language: str | None
    provider: str
    model: str | None


class FasterWhisperSTT:
    """Local Faster-Whisper adapter.

    Requires the optional `faster-whisper` package and a locally available model.
    Audio decoding is delegated to the provider; no audio is sent to a remote API.
    """

    def __init__(self, model: str = "small", device: str = "cpu", compute_type: str = "int8"):
        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:
            raise RuntimeError("Optional dependency 'faster-whisper' is not installed") from exc
        self.model_name = model
        self.model = WhisperModel(model, device=device, compute_type=compute_type)

    def transcribe(self, audio_path: str, language: str | None = None) -> Transcript:
        segments, info = self.model.transcribe(audio_path, language=language, vad_filter=True)
        text = " ".join(segment.text.strip() for segment in segments).strip()
        detected = getattr(info, "language", None)
        return Transcript(text=text, language=detected, provider="faster-whisper", model=self.model_name)


def word_error_rate(reference: str, hypothesis: str) -> float:
    """Standard Levenshtein WER over whitespace-tokenized words."""
    ref = reference.lower().split()
    hyp = hypothesis.lower().split()
    prev = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        cur = [i]
        for j, h in enumerate(hyp, 1):
            cur.append(min(cur[-1] + 1, prev[j] + 1, prev[j - 1] + (r != h)))
        prev = cur
    distance = prev[-1]
    return distance / len(ref) if ref else (0.0 if not hyp else 1.0)
