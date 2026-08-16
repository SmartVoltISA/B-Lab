"""B-Lab Audio Engine v0.1.

Provider-independent audio foundation. The laboratory core deliberately keeps
raw PCM/WAV evidence separate from optional STT/TTS providers. This version
implements deterministic WAV inspection, PCM energy VAD and lossless framing;
it does not pretend to perform speech recognition without an STT backend.
"""
from __future__ import annotations

import hashlib
import math
import struct
import wave
from dataclasses import dataclass


@dataclass(frozen=True)
class AudioEvidence:
    sample_rate: int
    channels: int
    sample_width: int
    frames: int
    duration_s: float
    sha256: str


@dataclass(frozen=True)
class SpeechSegment:
    start_s: float
    end_s: float
    rms: float


def inspect_wav(data: bytes) -> AudioEvidence:
    with wave.open(__import__("io").BytesIO(data), "rb") as wav:
        frames = wav.getnframes()
        rate = wav.getframerate()
        channels = wav.getnchannels()
        width = wav.getsampwidth()
    duration = frames / rate if rate else 0.0
    return AudioEvidence(rate, channels, width, frames, duration, hashlib.sha256(data).hexdigest())


def _pcm16_rms(chunk: bytes) -> float:
    if len(chunk) < 2:
        return 0.0
    count = len(chunk) // 2
    values = struct.unpack("<%dh" % count, chunk[: count * 2])
    return math.sqrt(sum(v * v for v in values) / count) / 32768.0


def vad_pcm16_mono(pcm: bytes, sample_rate: int, frame_ms: int = 30, threshold: float = 0.02) -> list[SpeechSegment]:
    """Return contiguous speech-like segments using deterministic RMS VAD.

    This is an intentionally conservative laboratory VAD, not a claim of
    production speech recognition quality.
    """
    if sample_rate <= 0 or frame_ms <= 0:
        raise ValueError("sample_rate and frame_ms must be positive")
    frame_bytes = max(2, int(sample_rate * frame_ms / 1000) * 2)
    active: list[tuple[int, float]] = []
    for offset in range(0, len(pcm), frame_bytes):
        chunk = pcm[offset:offset + frame_bytes]
        if len(chunk) < 2:
            continue
        rms = _pcm16_rms(chunk)
        if rms >= threshold:
            active.append((offset // 2, rms))
        else:
            active.append((-1, rms))

    segments: list[SpeechSegment] = []
    start = None
    values: list[float] = []
    for i, (sample, rms) in enumerate(active):
        if sample >= 0 and start is None:
            start = i
            values = []
        if sample >= 0:
            values.append(rms)
        elif start is not None:
            end = i
            segments.append(SpeechSegment(start * frame_ms / 1000, end * frame_ms / 1000, sum(values) / len(values)))
            start = None
    if start is not None:
        end = len(active)
        segments.append(SpeechSegment(start * frame_ms / 1000, end * frame_ms / 1000, sum(values) / len(values)))
    return segments


class STTAdapter:
    """Contract for optional speech-to-text providers.

    The core returns no invented transcript when no provider is attached.
    """
    def transcribe(self, audio: bytes, evidence: AudioEvidence) -> str:
        raise NotImplementedError


class TTSAdapter:
    """Contract for optional text-to-speech providers."""
    def synthesize(self, text: str) -> bytes:
        raise NotImplementedError


def audio_record(data: bytes, source: str = "unknown") -> dict:
    evidence = inspect_wav(data)
    return {
        "source": source,
        "evidence": evidence.__dict__,
        "transcript": None,
        "transcript_status": "not_configured",
        "raw_sha256": evidence.sha256,
    }
