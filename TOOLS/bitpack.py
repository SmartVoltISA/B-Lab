"""Bit-packed serialization for binary structural memory."""


def pack_memory(initial: int, targets: list[int]) -> bytes:
    if initial not in (0, 1) or any(v not in (0, 1) for v in targets):
        raise ValueError("binary values required")
    values = [initial, *targets]
    out = bytearray()
    current = 0
    count = 0
    for bit in values:
        current = (current << 1) | bit
        count += 1
        if count == 8:
            out.append(current)
            current = 0
            count = 0
    if count:
        out.append(current << (8 - count))
    return bytes(out)


def unpack_memory(payload: bytes, length: int) -> tuple[int, list[int]]:
    if length < 1 or length > len(payload) * 8:
        raise ValueError("invalid logical length")
    bits = []
    for byte in payload:
        for shift in range(7, -1, -1):
            bits.append((byte >> shift) & 1)
    bits = bits[:length]
    return bits[0], bits[1:]
