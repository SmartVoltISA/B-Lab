"""EXP-AUDIO-002 protocol gate for real STT evaluation.

No fabricated transcripts: real WER is reported only when a fixed reference
corpus and an actual STT provider are supplied.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class STTCase:
    case_id: str
    reference: str
    audio_sha256: str
    language: str = "ru"

def word_error_rate(reference: str, hypothesis: str) -> float:
    ref, hyp = reference.split(), hypothesis.split()
    prev = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        cur = [i]
        for j, h in enumerate(hyp, 1):
            cur.append(min(cur[-1] + 1, prev[j] + 1, prev[j - 1] + (r != h)))
        prev = cur
    return prev[-1] / len(ref) if ref else (0.0 if not hyp else 1.0)

def evaluate_case(case: STTCase, hypothesis: str) -> dict:
    return {
        "case_id": case.case_id,
        "language": case.language,
        "wer": word_error_rate(case.reference, hypothesis),
        "exact": case.reference == hypothesis,
        "audio_sha256": case.audio_sha256,
    }

def protocol_status() -> dict:
    return {
        "real_stt_required": True,
        "language": "ru",
        "metrics": ["WER", "exact_match", "latency", "memory"],
        "conditions": ["clean", "noise", "fast_speech", "slow_speech", "multiple_speakers"],
        "fabricated_transcripts_allowed": False,
    }

if __name__ == "__main__":
    print("AUDIO STT PROTOCOL: READY")
    print(protocol_status())
