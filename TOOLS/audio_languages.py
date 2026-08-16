"""Ω-AUDIO language registry.

Whisper multilingual models support a broad set of languages. The registry
keeps language selection explicit so the engine can use a user-selected
language or controlled auto-detection without silently changing languages.
"""
from __future__ import annotations

SUPPORTED_LANGUAGES = {
    "ru": "Русский", "kk": "Қазақша", "en": "English", "de": "Deutsch",
    "fr": "Français", "es": "Español", "it": "Italiano", "pt": "Português",
    "nl": "Nederlands", "pl": "Polski", "uk": "Українська", "be": "Беларуская",
    "cs": "Čeština", "sk": "Slovenčina", "bg": "Български", "sr": "Српски",
    "hr": "Hrvatski", "sl": "Slovenščina", "ro": "Română", "hu": "Magyar",
    "tr": "Türkçe", "ar": "العربية", "fa": "فارسی", "he": "עברית",
    "hi": "हिन्दी", "bn": "বাংলা", "ur": "اردو", "zh": "中文",
    "ja": "日本語", "ko": "한국어", "vi": "Tiếng Việt", "th": "ไทย",
    "id": "Bahasa Indonesia", "ms": "Bahasa Melayu", "ta": "தமிழ்",
    "te": "తెలుగు", "mr": "मराठी", "gu": "ગુજરાતી", "pa": "ਪੰਜਾਬੀ",
    "fa": "فارسی", "uz": "Oʻzbekcha", "mn": "Монгол",
}


def validate_language(code: str) -> str:
    code = code.lower().strip()
    if code == "auto":
        return code
    if code not in SUPPORTED_LANGUAGES:
        raise ValueError(f"unsupported language: {code}")
    return code


def language_options() -> dict[str, str]:
    return dict(SUPPORTED_LANGUAGES)
