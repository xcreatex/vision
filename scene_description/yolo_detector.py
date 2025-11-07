# scene_description/yolo_detector.py
from ultralytics import YOLO
import cv2

class YOLODetector:
    def __init__(self, model_path="models/yolo/yolov8s.pt"):
        self.model = YOLO(model_path)

    def detect_detailed(self, image_path, conf=0.45, imgsz=640):
        """
        Returns a detailed list of detections:
        [{label, conf, region, bbox(x1,y1,x2,y2)}]
        """
        results = self.model.predict(image_path, conf=conf, imgsz=imgsz, verbose=False)
        frame = cv2.imread(image_path)
        h, w = frame.shape[:2]
        one_third = w // 3

        detailed = []
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            label = self.model.names[cls_id]
            conf_score = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            # Determine region (left, center, right)
            center_x = (x1 + x2) / 2
            if center_x < one_third:
                region = "left"
            elif center_x < 2 * one_third:
                region = "center"
            else:
                region = "right"

            detailed.append({
                "label": label,
                "conf": conf_score,
                "region": region,
                "bbox": (x1, y1, x2, y2)
            })

        return detailed
