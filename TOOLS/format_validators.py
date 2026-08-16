"""Small evidence validators for common file families.

These validators deliberately check magic/container signatures only. They do
not claim semantic correctness of a complete image/video/document.
"""
from __future__ import annotations

SIGNATURES = {
    "jpeg": (b"\xff\xd8\xff",),
    "png": (b"\x89PNG\r\n\x1a\n",),
    "pdf": (b"%PDF-",),
    "zip": (b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08"),
    "riff": (b"RIFF",),
}


def validate_signature(kind: str, data: bytes) -> dict:
    variants = SIGNATURES.get(kind.lower(), ())
    matched = any(data.startswith(sig) for sig in variants)
    return {
        "kind": kind,
        "signature_match": matched,
        "evidence": "header_match" if matched else "no_supported_header",
        "full_semantic_validation": False,
    }
