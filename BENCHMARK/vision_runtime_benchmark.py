"""Ω-VISION runtime benchmark.

Two gates are deliberate:
1. deterministic structural gate (always runnable);
2. real detector gate (requires the experimental vision dependencies and model weights).

A detector result is never accepted merely because the process completed: the
benchmark checks that the returned evidence contains labels, confidence values,
geometry, source hash, and graph nodes/edges.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from urllib.request import urlretrieve

# The repository is intentionally lightweight and does not require packaging.
# Add its root so the benchmark works when invoked directly by GitHub Actions.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from TOOLS.vision_engine import VisionObservation, file_sha256, make_graph

FIXTURE_URL = "https://github.com/ultralytics/assets/releases/download/v0.0.0/bus.jpg"


def structural_gate() -> dict:
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "fixture.jpg"
        p.write_bytes(b"vision-fixture")
        digest = file_sha256(p)
        obs = VisionObservation(str(p), "image", digest, 640, 480, 3)
        graph = make_graph(obs, [("cat", 0.98), ("person", 0.91)])
        assert graph["observation"]["sha256"] == digest
        assert len(graph["nodes"]) == 3
        assert len(graph["edges"]) == 2
        assert all(0.0 <= e["confidence"] <= 1.0 for e in graph["edges"])
        return {"gate": "structural", "status": "PASS", "nodes": 3, "edges": 2}


def real_detector_gate() -> dict:
    from TOOLS.vision_model_adapter import detect_yolo

    with tempfile.TemporaryDirectory() as d:
        image = Path(d) / "bus.jpg"
        urlretrieve(FIXTURE_URL, image)
        result = detect_yolo(image)
        detections = result["detections"]
        graph = result["graph"]
        assert graph["observation"]["sha256"] == file_sha256(image)
        assert detections, "reference image produced no detections"
        assert len(graph["nodes"]) == len(detections) + 1
        assert len(graph["edges"]) == len(detections)
        for det in detections:
            assert det["label"]
            assert 0.0 <= det["confidence"] <= 1.0
            assert len(det["bbox_xyxy"]) == 4
        return {
            "gate": "real_detector",
            "status": "PASS",
            "backend": result["backend"],
            "model": result["model"],
            "detections": len(detections),
        }


if __name__ == "__main__":
    results = [structural_gate()]
    if "--real" in sys.argv:
        results.append(real_detector_gate())
    print(json.dumps(results, ensure_ascii=False, indent=2))
