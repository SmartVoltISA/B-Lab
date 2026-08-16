"""Deterministic benchmark for the structural part of Ω-VISION-001."""
from pathlib import Path
import tempfile

from TOOLS.vision_engine import VisionObservation, make_graph


def run() -> dict:
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "fixture.jpg"
        p.write_bytes(b"vision-fixture")
        from TOOLS.vision_engine import file_sha256
        digest = file_sha256(p)
        obs = VisionObservation(str(p), "image", digest, 640, 480, 3)
        graph = make_graph(obs, [("cat", 0.98), ("person", 0.91)])
        assert graph["observation"]["sha256"] == digest
        assert len(graph["nodes"]) == 3
        assert len(graph["edges"]) == 2
        assert all(0.0 <= e["confidence"] <= 1.0 for e in graph["edges"])
        return {"status": "PASS", "nodes": len(graph["nodes"]), "edges": len(graph["edges"])}


if __name__ == "__main__":
    print(run())
