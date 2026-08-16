"""Ω-VISION model adapter.

External models are replaceable components. The adapter converts their raw
predictions into the B-Lab evidence graph instead of letting a model define
our ontology or memory format.

Current reference backend: Ultralytics YOLO26n.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from TOOLS.vision_engine import VisionObservation, make_graph


def detect_yolo(path: str | Path, model_name: str = "yolo26n.pt", conf: float = 0.25) -> dict[str, Any]:
    """Run an optional YOLO detector and return B-Lab graph-compatible output."""
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
    labels: list[tuple[str, float]] = []
    boxes: list[dict[str, Any]] = []

    if result.boxes is not None:
        for i, box in enumerate(result.boxes):
            cls_id = int(box.cls[0].item())
            score = float(box.conf[0].item())
            xyxy = [float(v) for v in box.xyxy[0].tolist()]
            label = str(names[cls_id])
            labels.append((label, score))
            boxes.append({
                "object_id": f"object:{i}",
                "label": label,
                "confidence": score,
                "bbox_xyxy": xyxy,
            })

    observation = _image_observation(path)
    graph = make_graph(observation, labels)
    for node, box in zip(graph["nodes"][1:], boxes):
        node["attributes"] = {"bbox_xyxy": box["bbox_xyxy"]}

    return {
        "backend": "ultralytics-yolo26",
        "model": model_name,
        "confidence_threshold": conf,
        "graph": graph,
        "detections": boxes,
    }


def _image_observation(path: str | Path) -> VisionObservation:
    from TOOLS.vision_engine import inspect_image
    return inspect_image(path)


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("image")
    parser.add_argument("--model", default="yolo26n.pt")
    parser.add_argument("--conf", type=float, default=0.25)
    args = parser.parse_args()
    print(json.dumps(detect_yolo(args.image, args.model, args.conf), ensure_ascii=False, indent=2))
