"""B-Lab canonical memory engine.

Own, dependency-free lossless storage primitives for the three memory tiers:
ACTIVE, TEMPORARY and LONG_TERM.

Design rule:
    canonical bytes are stored once; decoded text/relations/views are materialized
    only when requested. The engine never claims compression when the encoded form
    is not smaller than the source.

The binary core packs 0/1 states eight per byte. For general byte/text data a
small deterministic RLE codec is used only when it actually reduces size.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class MemoryTier(str, Enum):
    ACTIVE = "active"
    TEMPORARY = "temporary"
    LONG_TERM = "long_term"


MAGIC = b"BLM1"
MODE_RAW = 0
MODE_RLE = 1
MODE_BITS = 2


@dataclass(frozen=True)
class MemoryRecord:
    tier: MemoryTier
    payload: bytes
    original_size: int
    mode: int

    @property
    def stored_size(self) -> int:
        return len(MAGIC) + 1 + 1 + 4 + len(self.payload)

    @property
    def ratio(self) -> float:
        if self.original_size == 0:
            return 1.0
        return self.original_size / self.stored_size


def pack_bits(states: Iterable[int]) -> bytes:
    """Pack binary states into bytes, least significant bit first."""
    values = list(states)
    if any(v not in (0, 1) for v in values):
        raise ValueError("states must contain only 0 or 1")
    out = bytearray((len(values) + 7) // 8)
    for i, value in enumerate(values):
        if value:
            out[i // 8] |= 1 << (i % 8)
    return bytes(out)


def unpack_bits(data: bytes, count: int) -> list[int]:
    if count < 0:
        raise ValueError("count must be non-negative")
    if len(data) < (count + 7) // 8:
        raise ValueError("bit payload is shorter than declared state count")
    return [(data[i // 8] >> (i % 8)) & 1 for i in range(count)]


def rle_encode(data: bytes) -> bytes:
    """Simple deterministic byte RLE: [run_length, byte] pairs, max run 255."""
    if not data:
        return b""
    out = bytearray()
    start = 0
    while start < len(data):
        value = data[start]
        end = start + 1
        while end < len(data) and data[end] == value and end - start < 255:
            end += 1
        out.extend((end - start, value))
        start = end
    return bytes(out)


def rle_decode(data: bytes) -> bytes:
    if len(data) % 2:
        raise ValueError("invalid RLE payload")
    out = bytearray()
    for i in range(0, len(data), 2):
        count, value = data[i], data[i + 1]
        if count == 0:
            raise ValueError("invalid zero-length RLE run")
        out.extend(bytes((value,)) * count)
    return bytes(out)


def encode(data: bytes, binary_count: int | None = None) -> tuple[int, bytes]:
    """Choose the smallest lossless representation among raw/RLE/bit-packed."""
    candidates: list[tuple[int, bytes]] = [(MODE_RAW, data)]
    rle = rle_encode(data)
    if len(rle) < len(data):
        candidates.append((MODE_RLE, rle))
    if binary_count is not None and binary_count >= 0 and len(data) == binary_count:
        try:
            packed = pack_bits(data)
            if len(packed) < len(data):
                candidates.append((MODE_BITS, packed))
        except ValueError:
            pass
    return min(candidates, key=lambda item: len(item[1]))


def decode(mode: int, payload: bytes, binary_count: int | None = None) -> bytes:
    if mode == MODE_RAW:
        return payload
    if mode == MODE_RLE:
        return rle_decode(payload)
    if mode == MODE_BITS:
        if binary_count is None:
            raise ValueError("binary_count is required for bit-packed data")
        return bytes(unpack_bits(payload, binary_count))
    raise ValueError(f"unknown mode: {mode}")


def serialize(record: MemoryRecord) -> bytes:
    if record.original_size < 0:
        raise ValueError("original_size must be non-negative")
    return MAGIC + bytes((list(MemoryTier).index(record.tier), record.mode)) + record.original_size.to_bytes(4, "big") + record.payload


def deserialize(blob: bytes) -> MemoryRecord:
    if len(blob) < 10 or blob[:4] != MAGIC:
        raise ValueError("invalid B-Lab memory record")
    tier_id, mode = blob[4], blob[5]
    try:
        tier = list(MemoryTier)[tier_id]
    except IndexError as exc:
        raise ValueError("invalid memory tier") from exc
    size = int.from_bytes(blob[6:10], "big")
    return MemoryRecord(tier=tier, payload=blob[10:], original_size=size, mode=mode)


def store(data: bytes, tier: MemoryTier, binary_count: int | None = None) -> bytes:
    mode, payload = encode(data, binary_count=binary_count)
    return serialize(MemoryRecord(tier=tier, payload=payload, original_size=len(data), mode=mode))


def load(blob: bytes, binary_count: int | None = None) -> tuple[MemoryTier, bytes]:
    record = deserialize(blob)
    data = decode(record.mode, record.payload, binary_count=binary_count)
    if len(data) != record.original_size:
        raise ValueError("decoded data does not match original size")
    return record.tier, data


def compress_text(text: str, tier: MemoryTier = MemoryTier.LONG_TERM) -> bytes:
    return store(text.encode("utf-8"), tier)


def decompress_text(blob: bytes) -> str:
    _, data = load(blob)
    return data.decode("utf-8")
