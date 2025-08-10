from ultralytics import YOLO
import cv2

class YOLODetector:
    def __init__(self, model_path="models/yolo/yolov8s.pt"):
        self.model = YOLO(model_path)

    def detect(self, image_path):
        results = self.model(image_path)[0]  # Get first result
        objects = []
        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = self.model.names[cls_id]
            confidence = float(box.conf[0])
            objects.append((label, confidence))
        return objects
