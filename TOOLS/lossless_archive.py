"""Adaptive lossless archive container.

Stores exact original bytes. Selects the smallest payload among deterministic
stdlib codecs and records codec, original length, and SHA-256 for integrity.
No semantic or historical information is discarded.
"""

from __future__ import annotations

import bz2
import gzip
import hashlib
import lzma
import struct
from dataclasses import dataclass

MAGIC = b"BLAR1"
_HEADER = struct.Struct(">5sBQQ32s")
_CODECS = {0: "gzip", 1: "bz2", 2: "xz"}


@dataclass(frozen=True)
class ArchiveInfo:
    codec: str
    original_size: int
    payload_size: int
    sha256: str


def _encode(codec: int, data: bytes) -> bytes:
    if codec == 0:
        return gzip.compress(data, compresslevel=9, mtime=0)
    if codec == 1:
        return bz2.compress(data, compresslevel=9)
    if codec == 2:
        return lzma.compress(data, preset=9, check=lzma.CHECK_SHA256)
    raise ValueError("unknown codec")


def _decode(codec: int, payload: bytes) -> bytes:
    if codec == 0:
        return gzip.decompress(payload)
    if codec == 1:
        return bz2.decompress(payload)
    if codec == 2:
        return lzma.decompress(payload)
    raise ValueError("unknown codec")


def compress(data: bytes) -> bytes:
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    candidates = {codec: _encode(codec, data) for codec in _CODECS}
    codec, payload = min(candidates.items(), key=lambda item: (len(item[1]), item[0]))
    digest = hashlib.sha256(data).digest()
    return _HEADER.pack(MAGIC, codec, len(data), len(payload), digest) + payload


def decompress(archive: bytes) -> bytes:
    if not isinstance(archive, bytes) or len(archive) < _HEADER.size:
        raise ValueError("invalid archive")
    magic, codec, original_size, payload_size, digest = _HEADER.unpack_from(archive)
    if magic != MAGIC or codec not in _CODECS:
        raise ValueError("invalid archive header")
    payload = archive[_HEADER.size:]
    if len(payload) != payload_size:
        raise ValueError("payload length mismatch")
    try:
        data = _decode(codec, payload)
    except Exception as exc:
        raise ValueError("archive payload is corrupt") from exc
    if len(data) != original_size or hashlib.sha256(data).digest() != digest:
        raise ValueError("archive integrity check failed")
    return data


def inspect(archive: bytes) -> ArchiveInfo:
    if len(archive) < _HEADER.size:
        raise ValueError("invalid archive")
    magic, codec, original_size, payload_size, digest = _HEADER.unpack_from(archive)
    if magic != MAGIC or codec not in _CODECS:
        raise ValueError("invalid archive header")
    return ArchiveInfo(_CODECS[codec], original_size, payload_size, digest.hex())
