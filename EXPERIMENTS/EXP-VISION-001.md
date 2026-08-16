# EXP-VISION-001 — Vision intake, structure and graph

## Purpose

Build the first vision organ that can accept JPEG/PNG images and video, preserve source identity, sample video frames, and represent detected objects as nodes and relations without pretending that an untested model understood the image.

## Principle

`source → observation → object → attributes → relations → memory`

The source remains the root of the evidence graph. Every semantic claim must retain its confidence and provenance.

## Required layers

1. **Input** — phone camera/image upload/video.
2. **Integrity** — SHA-256 for files; frame hashes for sampled video frames.
3. **Geometry** — width, height, channels, frame index, timestamp.
4. **Detection** — object class + confidence.
5. **Segmentation** — optional object mask.
6. **Pose/parts** — optional keypoints for people/animals/objects.
7. **Relations** — contains, near, behind, on, holding, etc.; only when supported by evidence.
8. **Identity/memory** — later layer; never infer a person's identity from appearance alone.
9. **Trust** — confidence, provenance, model/version, and whether the claim was verified.

## Initial ontology

### Person

`person → head, torso, arm, hand, leg, foot`

Optional visual attributes are observations, not identity claims: hair, clothing, approximate pose, visible accessories, etc.

### Cat

`cat → head, body, legs, paws, tail, ears, whiskers`

### Dog

`dog → head, body, legs, paws, tail, ears, muzzle`

The ontology is deliberately structural. It is not a claim that every instance has every visible part in every frame.

## External baseline checked

Ultralytics YOLO is a useful technical baseline because its current framework covers detection, segmentation, pose/keypoints, depth, classification, oriented boxes and tracking. However, its current open-source licensing is AGPL-3.0; commercial use without those AGPL requirements requires its commercial/Enterprise licensing. Therefore we use it as a **benchmark/reference candidate**, not as an automatic dependency of our own product. 

## Benchmark plan

### Image

- JPEG / PNG
- one object
- multiple objects
- partially occluded object
- poor lighting
- blur
- clutter

### Video

- fixed camera
- moving camera
- object enters/leaves frame
- same object across frames
- multiple objects

### Required metrics

- detection precision/recall/mAP where ground truth exists;
- segmentation IoU where masks exist;
- tracking identity consistency;
- frame processing latency;
- RAM/VRAM;
- graph node/edge preservation;
- confidence calibration;
- false-positive rate.

## Status

🟡 Architecture implemented.
🟡 Structural intake implemented.
🟡 Video sampling implemented.
⚪ Real detector/segmenter benchmark pending.
⚪ Phone camera integration pending.
⚪ Learned semantic associations pending.

Do not mark the organ green until real image/video fixtures have passed the benchmark.
