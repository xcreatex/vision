from ultralytics import YOLO
import cv2
import os

# Load YOLOv8 model (make sure yolov8s.pt is in ./models/yolo/)
MODEL_PATH = "models/yolo/yolov8s.pt"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ YOLO model not found at {MODEL_PATH}")

model = YOLO(MODEL_PATH)


def detect_objects(image_path: str, conf_threshold: float = 0.45):
    """
    Detects objects in the image and divides them into left, center, and right regions.
    Returns dict with region lists + guidance text.
    """

    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Failed to load image from path")

        height, width, _ = image.shape
        left_boundary = width // 3
        right_boundary = 2 * width // 3

        # Run detection
        results = model.predict(image, conf=conf_threshold, verbose=False)[0]

        left_objs, center_objs, right_objs = [], [], []
        guidance = []

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            conf = float(box.conf[0])

            # Box coordinates
            x1, y1, x2, y2 = box.xyxy[0]
            x_center = (x1 + x2) / 2

            # Region classification
            if x_center < left_boundary:
                left_objs.append(label)
            elif x_center < right_boundary:
                center_objs.append(label)
            else:
                right_objs.append(label)

        # --- Guidance logic ---
        if not center_objs:
            if left_objs and not right_objs:
                guidance.append("Move camera slightly to the right.")
            elif right_objs and not left_objs:
                guidance.append("Move camera slightly to the left.")
            elif left_objs and right_objs:
                guidance.append("Objects detected on both sides. Center your view.")
            else:
                guidance.append("No objects detected. Try refocusing.")
        else:
            guidance.append("Main objects are centered. Good framing.")

        return {
            "left": list(set(left_objs)),
            "center": list(set(center_objs)),
            "right": list(set(right_objs)),
            "guidance": guidance,
        }

    except Exception as e:
        print(f"❌ Error in detect_objects(): {e}")
        return {"left": [], "center": [], "right": [], "guidance": ["Detection failed."]}
