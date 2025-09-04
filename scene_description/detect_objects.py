from ultralytics import YOLO

class YOLODetector:
    def __init__(self, model_path="models/yolo/yolov8s.pt"):
        self.model = YOLO(model_path)

    def detect(self, image_path):
        """
        Detect objects and split them into left/center/right lists.
        Returns a dict: {"left": [...], "center": [...], "right": [...]}
        """
        results = self.model(image_path)[0]
        width = results.orig_shape[1]  # image width
        region_size = width // 3

        regions = {"left": [], "center": [], "right": []}

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = self.model.names[cls_id]
            confidence = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            center_x = (x1 + x2) / 2

            if center_x < region_size:
                regions["left"].append((label, confidence))
            elif center_x < 2 * region_size:
                regions["center"].append((label, confidence))
            else:
                regions["right"].append((label, confidence))

        return regions
