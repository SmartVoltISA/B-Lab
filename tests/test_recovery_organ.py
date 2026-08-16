from TOOLS.disk_image import chunk_ranges, fingerprint_bytes
from TOOLS.filesystem_analyzer import analyze_extents
from TOOLS.format_validators import validate_signature
from TOOLS.recovery_organ import build_evidence_graph, recovery_report, scan_signatures, trust_score


def test_read_only_image_fingerprint_and_chunks():
    data = b"A" * 10000
    info = fingerprint_bytes(data)
    assert info.read_only is True
    assert info.size == len(data)
    assert sum(b - a for a, b in chunk_ranges(len(data), 4096)) == len(data)


def test_filesystem_metadata_is_conservative():
    result = analyze_extents([
        {"path": "/a", "start": 0, "length": 10, "allocated": True},
        {"path": "/b", "start": 20, "length": 5, "allocated": False},
        {"path": "", "start": -1, "length": 2, "allocated": True},
    ])
    assert result["files"] == 2
    assert result["allocated"] == 1
    assert result["unallocated"] == 1


def test_signature_to_graph_to_report():
    data = b"X" * 32 + b"%PDF-1.7" + b"Y" * 32
    evidence = scan_signatures(data, {"pdf": b"%PDF-"})
    graph = build_evidence_graph(evidence)
    assert len(graph.nodes) == 1
    report = recovery_report(data, graph)
    assert report["full_recovery"] is False


def test_trust_is_evidence_strength_not_probability():
    e = scan_signatures(b"\xff\xd8\xffabc", {"jpeg": b"\xff\xd8\xff"})[0]
    assert trust_score(e, checksum_ok=True, parser_ok=True, redundant_copy=True) == 0.95


def test_known_format_header():
    assert validate_signature("png", b"\x89PNG\r\n\x1a\nrest")["signature_match"] is True
    assert validate_signature("png", b"not png")["signature_match"] is False
