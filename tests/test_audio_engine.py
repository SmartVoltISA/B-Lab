import io
import math
import wave

from TOOLS.audio_engine import audio_record, inspect_wav, vad_pcm16_mono


def make_wav(samples, rate=8000):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        raw = b"".join(int(max(-1, min(1, x)) * 32767).to_bytes(2, "little", signed=True) for x in samples)
        w.writeframes(raw)
    return buf.getvalue()


def test_wav_evidence_is_deterministic():
    data = make_wav([0.0] * 800)
    e = inspect_wav(data)
    assert e.sample_rate == 8000
    assert e.channels == 1
    assert e.frames == 800
    assert e.duration_s == 0.1
    assert len(e.sha256) == 64


def test_vad_detects_silence_and_tone():
    rate = 8000
    silence = [0.0] * 800
    tone = [0.2 * math.sin(2 * math.pi * 440 * i / rate) for i in range(800)]
    segments = vad_pcm16_mono(b"".join(int(x * 32767).to_bytes(2, "little", signed=True) for x in silence + tone), rate, threshold=0.02)
    assert segments
    assert segments[-1].end_s >= 0.1


def test_audio_record_never_invents_transcript():
    data = make_wav([0.0] * 100)
    record = audio_record(data, source="lab")
    assert record["transcript"] is None
    assert record["transcript_status"] == "not_configured"
    assert record["raw_sha256"] == inspect_wav(data).sha256
