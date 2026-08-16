"""EXP-0018 — Recovery Organ integration benchmark."""
from TOOLS.disk_image import fingerprint_bytes
from TOOLS.filesystem_analyzer import analyze_extents
from TOOLS.format_validators import validate_signature
from TOOLS.recovery_organ import build_evidence_graph, recovery_report, scan_signatures, trust_score


def run() -> None:
    source = b"A" * 4096 + b"%PDF-1.7\n" + b"B" * 4096
    image = fingerprint_bytes(source, "fixture-image")
    evidence = scan_signatures(source, {"pdf": b"%PDF-"})
    graph = build_evidence_graph(evidence)
    report = recovery_report(source, graph)
    fs = analyze_extents([{"path": "/fixture.pdf", "start": 4096, "length": 9, "allocated": True}])
    validator = validate_signature("pdf", source[4096:])
    score = trust_score(evidence[0], parser_ok=validator["signature_match"])

    assert image.read_only
    assert len(evidence) == 1
    assert len(graph.nodes) == 1
    assert fs["files"] == 1
    assert validator["signature_match"]
    assert 0.0 < score <= 0.95
    assert report["full_recovery"] is False

    print("RECOVERY ORGAN BENCHMARK: PASS")
    print(f"source_bytes={image.size}")
    print(f"source_sha256={image.sha256}")
    print(f"evidence_nodes={len(graph.nodes)}")
    print(f"evidence_edges={len(graph.edges)}")
    print(f"format_validated={validator['signature_match']}")
    print(f"trust_score={score:.2f}")
    print("read_only=true")
    print("full_recovery_claim=false")


if __name__ == "__main__":
    run()
