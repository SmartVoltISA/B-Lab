"""EXP-AUDIO-004 protocol gate for multilingual corpus evaluation."""
from dataclasses import dataclass

LANGUAGES = (
    "ru", "kk", "en", "uk", "uz", "tr", "de", "fr", "es", "it",
    "ar", "zh", "ja", "ko", "hi", "mn", "pl",
)

@dataclass(frozen=True)
class CorpusSample:
    audio_id: str
    language: str
    text_reference: str
    audio_sha256: str
    condition: str
    language_variant: str | None = None


def validate_sample(sample: CorpusSample) -> None:
    if sample.language not in LANGUAGES:
        raise ValueError("language is not registered")
    if not sample.audio_id or not sample.audio_sha256:
        raise ValueError("audio provenance is required")
    if not sample.text_reference:
        raise ValueError("reference transcript is required")


def protocol_status() -> dict:
    return {
        "languages": list(LANGUAGES),
        "modes": ["manual", "auto", "mixed"],
        "conditions": ["clean", "noise", "fast", "slow", "multi_speaker"],
        "metrics": ["language_id_accuracy", "WER", "CER", "exact_match", "latency_ms", "memory_mb", "failure_rate"],
        "real_audio_required": True,
        "fabricated_transcripts_allowed": False,
    }


if __name__ == "__main__":
    print("MULTILINGUAL CORPUS PROTOCOL: READY")
    print(protocol_status())
