import cv2
import datetime
import os

def capture_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # Warm up camera (read and discard a few frames)
    for _ in range(5):
        ret, frame = cap.read()

    cap.release()

    if not ret:
        raise ValueError("Failed to capture image from webcam")

    os.makedirs("captured_images", exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"captured_images/captured_{timestamp}.jpg"
    
    saved = cv2.imwrite(image_path, frame)
    print(f"✅ Image saved at: {image_path} | Saved: {saved}")

    return image_path

