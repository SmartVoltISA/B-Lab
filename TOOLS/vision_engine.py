"""Ω-VISION-001: deterministic vision intake and structural representation.

This module does not claim semantic understanding by itself. It extracts stable
observations from JPEG/PNG images and video frames, then represents them as a
graph suitable for later vision models and memory integration.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
from pathlib import Path
from typing import Any

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None

try:
    import cv2
except ImportError:  # pragma: no cover
    cv2 = None


@dataclass(frozen=True)
class VisionObservation:
    source: str
    source_type: str
    sha256: str
    width: int | None
    height: int | None
    channels: int | None
    frame_index: int | None = None
    timestamp_ms: float | None = None


@dataclass(frozen=True)
class VisionNode:
    node_id: str
    kind: str
    label: str
    confidence: float | None = None
    attributes: dict[str, Any] | None = None


@dataclass(frozen=True)
class VisionEdge:
    source: str
    relation: str
    target: str
    confidence: float | None = None


def file_sha256(path: str | Path) -> str:
    h = sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def inspect_image(path: str | Path) -> VisionObservation:
    path = Path(path)
    digest = file_sha256(path)
    if Image is None:
        return VisionObservation(str(path), "image", digest, None, None, None)
    with Image.open(path) as im:
        channels = len(im.getbands())
        return VisionObservation(
            str(path), "image", digest, im.width, im.height, channels
        )


def sample_video(path: str | Path, every_n_frames: int = 30, max_frames: int = 32) -> list[VisionObservation]:
    if cv2 is None:
        raise RuntimeError("opencv-python is required for video sampling")
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise ValueError(f"cannot open video: {path}")
    out: list[VisionObservation] = []
    i = 0
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    try:
        while len(out) < max_frames:
            ok, frame = cap.read()
            if not ok:
                break
            if i % every_n_frames == 0:
                h, w = frame.shape[:2]
                # Frame hash makes the observation reproducible without storing pixels.
                digest = sha256(frame.tobytes()).hexdigest()
                out.append(VisionObservation(
                    str(path), "video_frame", digest, w, h,
                    int(frame.shape[2]) if len(frame.shape) == 3 else 1,
                    i, (i / fps * 1000.0) if fps else None,
                ))
            i += 1
    finally:
        cap.release()
    return out


def make_graph(observation: VisionObservation, labels: list[tuple[str, float]] | None = None) -> dict[str, Any]:
    """Create the structural layer; semantic labels are supplied by a vision model."""
    root = "source:0"
    nodes = [VisionNode(root, "source", observation.source)]
    edges: list[VisionEdge] = []
    for idx, (label, confidence) in enumerate(labels or []):
        node_id = f"object:{idx}"
        nodes.append(VisionNode(node_id, "object", label, confidence))
        edges.append(VisionEdge(root, "contains", node_id, confidence))
    return {
        "observation": asdict(observation),
        "nodes": [asdict(n) for n in nodes],
        "edges": [asdict(e) for e in edges],
    }
