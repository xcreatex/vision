# from ultralytics import YOLO

# class YOLODetector:
#     def __init__(self, model_path="models/yolo/yolov8s.pt"):
#         self.model = YOLO(model_path)

#     def detect(self, image_path):
#         """
#         Detect objects and split them into left/center/right lists.
#         Returns a dict: {"left": [...], "center": [...], "right": [...]}
#         """
#         results = self.model(image_path)[0]
#         width = results.orig_shape[1]  # image width
#         region_size = width // 3

#         regions = {"left": [], "center": [], "right": []}

#         for box in results.boxes:
#             cls_id = int(box.cls[0])
#             label = self.model.names[cls_id]
#             confidence = float(box.conf[0])
#             x1, y1, x2, y2 = box.xyxy[0].tolist()
#             center_x = (x1 + x2) / 2

#             if center_x < region_size:
#                 regions["left"].append((label, confidence))
#             elif center_x < 2 * region_size:
#                 regions["center"].append((label, confidence))
#             else:
#                 regions["right"].append((label, confidence))

#         return regions


from ultralytics import YOLO
import cv2

# Initialize YOLO once globally
MODEL_PATH = "models/yolo/yolov8s.pt"
model = YOLO(MODEL_PATH)

# Configurable list of objects of interest
OBJECTS_OF_INTEREST = ["person", "board", "bottle"]

def detect_objects(image_path: str):
    try:
        results = model(image_path)[0]  # First result
        width = results.orig_shape[1]   # Image width
        region_size = width // 3        # Divide into 3 parts

        # Store detections in buckets
        left, center, right = [], [], []
        guidance = []

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            confidence = float(box.conf[0])

            # Center X coordinate of the bounding box
            x_center = float((box.xyxy[0][0] + box.xyxy[0][2]) / 2)

            # Decide region
            if x_center < region_size:
                left.append(label)
                region = "left"
            elif x_center < 2 * region_size:
                center.append(label)
                region = "center"
            else:
                right.append(label)
                region = "right"

            # Add guidance only if it's an object of interest
            if label in OBJECTS_OF_INTEREST:
                if region == "left":
                    guidance.append(f"{label} is on the left, move camera right to center it.")
                elif region == "right":
                    guidance.append(f"{label} is on the right, move camera left to center it.")
                else:
                    guidance.append(f"{label} is already centered.")

        return {
            "left": left,
            "center": center,
            "right": right,
            "guidance": guidance
        }

    except Exception as e:
        print(f"❌ Error in detect_objects(): {e}")
        return {"left": [], "center": [], "right": [], "guidance": []}
