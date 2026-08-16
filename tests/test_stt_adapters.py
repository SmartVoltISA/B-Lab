from TOOLS.stt_adapters import word_error_rate


def test_wer_exact_match():
    assert word_error_rate("привет мир", "привет мир") == 0.0


def test_wer_detects_one_word_error():
    assert word_error_rate("привет мир сегодня", "привет мир завтра") == 1 / 3


def test_wer_empty_reference_is_defined():
    assert word_error_rate("", "что-то") == 1.0
    assert word_error_rate("", "") == 0.0
