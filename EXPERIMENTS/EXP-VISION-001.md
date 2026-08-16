# EXP-VISION-001 — Vision intake, structure and graph

## Purpose

Build the first vision organ that can accept JPEG/PNG images and video, preserve source identity, sample video frames, and represent detected objects and relations without pretending that an untested model understood the image.

## Principle

`source → observation → object → attributes → relations → memory`

The source remains the root of the evidence graph. Every semantic claim must retain confidence and provenance.

## Required layers

1. **Input** — phone camera/image upload/video.
2. **Integrity** — SHA-256 for files; frame hashes for sampled video frames.
3. **Geometry** — width, height, channels, frame index, timestamp.
4. **Detection** — object class + confidence.
5. **Segmentation** — optional object mask.
6. **Pose/parts** — optional keypoints for people/animals/objects.
7. **Tracking** — persistent object track IDs across video frames.
8. **Relations** — contains, near, behind, on, holding, etc.; only when supported by evidence.
9. **Identity/memory** — later layer; never infer a person's identity from appearance alone.
10. **Trust** — confidence, provenance, model/version, and whether the claim was verified.

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

Current Ultralytics YOLO26 provides detection, instance/semantic segmentation, depth, classification, pose, oriented detection and tracking. It is used only as an external benchmark/reference backend; B-Lab does not adopt its ontology or memory model.

## Implemented B-Lab adapter

`TOOLS/vision_model_adapter.py` converts model output into our own evidence format:

- detection → object node + confidence + bounding box;
- segmentation → object node + mask presence/geometry metadata;
- pose → object node + keypoint count;
- tracking → frame sequence + persistent track IDs.

The external model therefore supplies observations; B-Lab retains control of the ontology, graph, provenance and later memory layers.

## Real runtime smoke benchmark

Reference fixture: public Ultralytics `bus.jpg`.

CI run `31936344248` passed both structural and real runtime gates.

Results:

- **Detection:** PASS — 5 detections.
- **Instance segmentation:** PASS — 5 segmented objects.
- **Pose:** PASS — 4 posed objects, 17 keypoints.
- **Video tracking:** PASS — 4 frames, tracks observed on all 4.
- **Graph preservation:** PASS.
- **Source hashing:** PASS.

These are **smoke tests**, not accuracy claims. General accuracy still requires a controlled fixture set with ground truth, including occlusion, blur, lighting, clutter and multiple object classes.

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

🟢 Architecture + real runtime smoke path verified.
🟢 Detection verified.
🟢 Segmentation verified.
🟢 Pose/keypoints verified.
🟢 Video tracking verified.
🟡 Controlled accuracy benchmark pending.
🟡 Phone camera integration pending.
🟡 Learned semantic associations pending.
🟡 Memory/association loop pending.

Do not mark the organ fully complete until controlled fixtures and phone-camera input have passed.
