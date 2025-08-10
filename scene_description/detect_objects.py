from ultralytics import YOLO
import cv2

# Load model once globally
MODEL_PATH = "yolov8s.pt"
model = YOLO(MODEL_PATH)

def detect_objects(image_path: str) -> list:
    try:
        results = model(image_path)
        names = model.names

        detected = set()
        for result in results:
            for cls in result.boxes.cls:
                label = names[int(cls)]
                detected.add(label)

        return list(detected)

    except Exception as e:
        print(f"❌ Error in detect_objects(): {e}")
        return []
