"""Ω-VISION model adapter.

External models are replaceable components. The adapter converts their raw
predictions into the B-Lab evidence graph instead of letting a model define
our ontology or memory format.

Current reference backend: Ultralytics YOLO26n family.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from TOOLS.vision_engine import VisionObservation, make_graph


def detect_yolo(path: str | Path, model_name: str = "yolo26n.pt", conf: float = 0.25) -> dict[str, Any]:
    """Object detection -> B-Lab graph."""
    return _image_task(path, model_name, conf, task="detect")


def segment_yolo(path: str | Path, model_name: str = "yolo26n-seg.pt", conf: float = 0.25) -> dict[str, Any]:
    """Instance segmentation -> boxes + masks metadata + B-Lab graph."""
    return _image_task(path, model_name, conf, task="segment")


def pose_yolo(path: str | Path, model_name: str = "yolo26n-pose.pt", conf: float = 0.25) -> dict[str, Any]:
    """Human/animal pose -> boxes + keypoints metadata + B-Lab graph."""
    return _image_task(path, model_name, conf, task="pose")


def _image_task(path: str | Path, model_name: str, conf: float, task: str) -> dict[str, Any]:
    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise RuntimeError(
            "Ultralytics is not installed. Install the experimental vision dependencies."
        ) from exc

    model = YOLO(model_name)
    results = model.predict(source=str(path), conf=conf, verbose=False)
    if not results:
        raise RuntimeError("vision model returned no result")
    result = results[0]
    names = result.names
    objects: list[dict[str, Any]] = []
    labels: list[tuple[str, float]] = []

    if result.boxes is not None:
        for i, box in enumerate(result.boxes):
            cls_id = int(box.cls[0].item())
            score = float(box.conf[0].item())
            label = str(names[cls_id])
            item: dict[str, Any] = {
                "object_id": f"object:{i}",
                "label": label,
                "confidence": score,
                "bbox_xyxy": [float(v) for v in box.xyxy[0].tolist()],
            }
            if task == "segment" and result.masks is not None:
                item["mask_present"] = True
                item["mask_points"] = int(len(result.masks.xy[i])) if i < len(result.masks.xy) else 0
            if task == "pose" and result.keypoints is not None:
                item["keypoints_present"] = True
                item["keypoint_count"] = int(result.keypoints.data.shape[1]) if result.keypoints.data.ndim == 3 else 0
            labels.append((label, score))
            objects.append(item)

    observation = _image_observation(path)
    graph = make_graph(observation, labels)
    for node, item in zip(graph["nodes"][1:], objects):
        node["attributes"] = {k: v for k, v in item.items() if k not in {"object_id", "label", "confidence"}}

    return {
        "backend": "ultralytics-yolo26",
        "task": task,
        "model": model_name,
        "confidence_threshold": conf,
        "graph": graph,
        "detections": objects,
    }


def track_yolo(video: str | Path, model_name: str = "yolo26n.pt", conf: float = 0.25) -> dict[str, Any]:
    """Track objects through a video and preserve model track IDs."""
    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise RuntimeError("Ultralytics is not installed") from exc

    model = YOLO(model_name)
    results = model.track(source=str(video), conf=conf, persist=False, verbose=False)
    frames: list[dict[str, Any]] = []
    for frame_index, result in enumerate(results):
        ids = []
        if result.boxes is not None and result.boxes.id is not None:
            ids = [int(v) for v in result.boxes.id.tolist()]
        frames.append({"frame_index": frame_index, "track_ids": ids, "object_count": len(ids)})
    return {"backend": "ultralytics-yolo26", "model": model_name, "frames": frames}


def _image_observation(path: str | Path) -> VisionObservation:
    from TOOLS.vision_engine import inspect_image
    return inspect_image(path)


if __name__ == "__main__":
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument("image")
    parser.add_argument("--model", default="yolo26n.pt")
    parser.add_argument("--task", choices=["detect", "segment", "pose"], default="detect")
    parser.add_argument("--conf", type=float, default=0.25)
    args = parser.parse_args()
    fn = {"detect": detect_yolo, "segment": segment_yolo, "pose": pose_yolo}[args.task]
    print(json.dumps(fn(args.image, args.model, args.conf), ensure_ascii=False, indent=2))
