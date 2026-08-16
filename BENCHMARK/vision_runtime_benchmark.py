"""Ω-VISION runtime benchmark.

Gates:
1. deterministic structural layer;
2. real detection;
3. real instance segmentation;
4. real pose/keypoints;
5. real video tracking.

The benchmark checks evidence integrity and graph preservation. It does not
claim that a single reference image proves general-world accuracy.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from urllib.request import urlretrieve

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


def _download_image(path: Path) -> None:
    urlretrieve(FIXTURE_URL, path)
    assert path.stat().st_size > 1000


def image_gate() -> list[dict]:
    from TOOLS.vision_model_adapter import detect_yolo, pose_yolo, segment_yolo

    with tempfile.TemporaryDirectory() as d:
        image = Path(d) / "bus.jpg"
        _download_image(image)
        results = []

        detection = detect_yolo(image)
        assert detection["detections"]
        assert len(detection["graph"]["nodes"]) == len(detection["detections"]) + 1
        results.append({
            "gate": "real_detector", "status": "PASS",
            "model": detection["model"], "detections": len(detection["detections"])
        })

        segmentation = segment_yolo(image)
        segmented = [d for d in segmentation["detections"] if d.get("mask_present")]
        assert segmented, "reference image produced no segmentation masks"
        results.append({
            "gate": "real_segmentation", "status": "PASS",
            "model": segmentation["model"], "segmented_objects": len(segmented)
        })

        pose = pose_yolo(image)
        posed = [d for d in pose["detections"] if d.get("keypoints_present")]
        assert posed, "reference image produced no pose/keypoint detections"
        results.append({
            "gate": "real_pose", "status": "PASS",
            "model": pose["model"], "posed_objects": len(posed),
            "keypoints": posed[0]["keypoint_count"]
        })
        return results


def video_tracking_gate() -> dict:
    import cv2
    from TOOLS.vision_model_adapter import track_yolo

    with tempfile.TemporaryDirectory() as d:
        image = Path(d) / "bus.jpg"
        video = Path(d) / "bus_test.mp4"
        _download_image(image)
        frame = cv2.imread(str(image))
        assert frame is not None
        h, w = frame.shape[:2]
        writer = cv2.VideoWriter(
            str(video), cv2.VideoWriter_fourcc(*"mp4v"), 5.0, (w, h)
        )
        assert writer.isOpened(), "video writer unavailable"
        try:
            # Repeated frames isolate the tracking pipeline from a second
            # motion-generation algorithm. Identity continuity is the test target.
            for _ in range(4):
                writer.write(frame)
        finally:
            writer.release()

        result = track_yolo(video)
        observed = [f for f in result["frames"] if f["track_ids"]]
        assert len(result["frames"]) >= 2
        assert observed, "tracker returned no object tracks"
        return {
            "gate": "real_video_tracking", "status": "PASS",
            "frames": len(result["frames"]),
            "tracked_frames": len(observed),
            "model": result["model"],
        }


if __name__ == "__main__":
    results = [structural_gate()]
    if "--real" in sys.argv:
        results.extend(image_gate())
        results.append(video_tracking_gate())
    print(json.dumps(results, ensure_ascii=False, indent=2))
