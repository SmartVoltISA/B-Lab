"""EXP-AUDIO-002: deterministic STT scoring benchmark.

No model is downloaded in CI. This benchmark validates the metric and the
provider contract; real speech accuracy is measured later on a fixed audio set.
"""
from TOOLS.stt_adapters import word_error_rate


def run():
    cases = [
        ("привет мир", "привет мир", 0.0),
        ("это лаборатория", "это лаборатория", 0.0),
        ("мы проверяем голосовой ввод", "мы проверяем голосовой вывод", 0.25),
    ]
    for reference, hypothesis, expected in cases:
        got = word_error_rate(reference, hypothesis)
        assert abs(got - expected) < 1e-12
    print("STT SCORING BENCHMARK: PASS")
    print("wer_metric=true")
    print("model_download=false")
    print("real_stt_accuracy_not_claimed=true")


if __name__ == "__main__":
    run()
