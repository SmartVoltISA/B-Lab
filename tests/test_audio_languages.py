from TOOLS.audio_languages import language_options, validate_language


def test_core_languages_available():
    options = language_options()
    for code in ("ru", "kk", "en", "de", "fr", "es", "zh", "ja", "ko", "ar", "tr", "uk"):
        assert code in options


def test_explicit_language_is_stable():
    assert validate_language("RU") == "ru"
    assert validate_language(" kk ") == "kk"
    assert validate_language("auto") == "auto"


def test_unknown_language_rejected():
    try:
        validate_language("xx")
    except ValueError:
        pass
    else:
        raise AssertionError("unknown language must be rejected")
