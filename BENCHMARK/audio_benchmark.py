"""EXP-AUDIO-001: deterministic audio evidence and VAD benchmark."""
import io
import math
import wave

from TOOLS.audio_engine import audio_record, inspect_wav, vad_pcm16_mono


def wav_pcm16(samples, rate=8000):
    out = io.BytesIO()
    with wave.open(out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes(b"".join(int(max(-1, min(1, x))*32767).to_bytes(2, "little", signed=True) for x in samples))
    return out.getvalue()


def run():
    rate = 8000
    silence = [0.0] * 800
    tone = [0.2 * math.sin(2 * math.pi * 440 * i / rate) for i in range(800)]
    data = wav_pcm16(silence + tone, rate)
    evidence = inspect_wav(data)
    segments = vad_pcm16_mono(b"".join(int(x*32767).to_bytes(2, "little", signed=True) for x in silence + tone), rate)
    record = audio_record(data, "synthetic-lab")
    assert evidence.sha256 == record["raw_sha256"]
    assert segments
    assert record["transcript"] is None
    assert record["transcript_status"] == "not_configured"
    print("AUDIO BENCHMARK: PASS")
    print(f"sample_rate={evidence.sample_rate}")
    print(f"duration_s={evidence.duration_s}")
    print(f"vad_segments={len(segments)}")
    print("raw_sha256_stable=true")
    print("transcript_invention=false")


if __name__ == "__main__":
    run()
