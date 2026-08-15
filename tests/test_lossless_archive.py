from TOOLS.lossless_archive import compress, decompress, inspect


def test_roundtrip_representative_payloads():
    payloads = [
        b"",
        b"0" * 10000,
        bytes(range(256)) * 40,
        bytes(((i * 73 + 19) % 256) for i in range(10000)),
    ]
    for payload in payloads:
        archive = compress(payload)
        assert decompress(archive) == payload
        info = inspect(archive)
        assert info.original_size == len(payload)
        assert info.payload_size == len(archive) - 54
        assert len(info.sha256) == 64


def test_archive_detects_corruption():
    payload = b"history must survive exactly" * 100
    archive = bytearray(compress(payload))
    archive[-1] ^= 1
    try:
        decompress(bytes(archive))
    except ValueError as exc:
        assert "corrupt" in str(exc) or "integrity" in str(exc)
    else:
        raise AssertionError("corruption was not detected")
