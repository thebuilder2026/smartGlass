import os
from collections import Counter
import cv2
from dotenv import load_dotenv
from ultralytics import YOLO

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "yolov8n.pt")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.45"))
CLOSE_AREA = float(os.getenv("CLOSE_OBJECT_AREA_RATIO", "0.16"))
VERY_CLOSE_AREA = float(os.getenv("VERY_CLOSE_OBJECT_AREA_RATIO", "0.30"))

ROAD_HAZARDS = {"car", "truck", "bus", "motorcycle", "bicycle", "train"}
INDOOR_HAZARDS = {"chair", "couch", "bed", "dining table", "bench", "potted plant"}
GENERAL_HAZARDS = ROAD_HAZARDS | INDOOR_HAZARDS | {"person", "dog", "cat", "horse"}

_model = None

def get_model():
    global _model
    if _model is None:
        _model = YOLO(MODEL_NAME)
    return _model

def closeness_label(area_ratio):
    if area_ratio >= VERY_CLOSE_AREA:
        return "VERY CLOSE"
    if area_ratio >= CLOSE_AREA:
        return "CLOSE"
    return "NORMAL"

def position_label(cx, frame_width):
    p = cx / max(frame_width, 1)
    if p < 0.33:
        return "left"
    if p > 0.67:
        return "right"
    return "ahead"

def analyze_frame(frame, mode="General Mobility"):
    model = get_model()
    result = model.predict(source=frame, conf=CONFIDENCE_THRESHOLD, verbose=False)[0]
    h, w = frame.shape[:2]
    frame_area = max(h*w, 1)
    annotated = frame.copy()
    detections, alerts = [], []

    if result.boxes is None:
        return annotated, detections, alerts, "No objects detected."

    names = model.names
    for box in result.boxes:
        cls_id = int(box.cls[0].item())
        conf = float(box.conf[0].item())
        x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
        label = names[cls_id]

        ratio = max((x2-x1)*(y2-y1), 0) / frame_area
        close = closeness_label(ratio)
        pos = position_label((x1+x2)/2, w)

        if mode == "Road Safety":
            is_hazard = label in ROAD_HAZARDS or label == "person"
        elif mode == "Indoor Navigation":
            is_hazard = label in INDOOR_HAZARDS or label in {"person","dog","cat"}
        else:
            is_hazard = label in GENERAL_HAZARDS

        hazard_now = bool(is_hazard and close != "NORMAL")
        detections.append({
            "object": label,
            "confidence": round(conf, 3),
            "position": pos,
            "closeness": close,
            "area_ratio": round(ratio, 4),
            "hazard": hazard_now
        })

        color = (0,0,255) if hazard_now else (0,180,0)
        cv2.rectangle(annotated, (x1,y1), (x2,y2), color, 2)
        cv2.putText(
            annotated,
            f"{label} {conf:.2f} | {pos} | {close}",
            (x1, max(20,y1-8)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2
        )

        if hazard_now:
            prefix = "Warning" if close == "VERY CLOSE" else "Caution"
            alerts.append(f"{prefix}: {label} {close.lower()} {pos}.")

    return annotated, detections, alerts, build_scene_summary(detections)

def build_scene_summary(detections):
    if not detections:
        return "No objects detected."
    counts = Counter(d["object"] for d in detections)
    parts = [f"{count} {name}" for name, count in counts.most_common(6)]
    nearby = [f"{d['object']} {d['position']}" for d in detections if d["closeness"] != "NORMAL"]
    text = "Detected " + ", ".join(parts) + "."
    if nearby:
        text += " Nearby: " + ", ".join(nearby[:5]) + "."
    return text
