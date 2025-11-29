# webcam_capture.py
import cv2
import datetime
import os
import glob

def capture_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # Warm camera
    for _ in range(5):
        ret, frame = cap.read()
    cap.release()

    if not ret:
        raise ValueError("Failed to capture image")

    os.makedirs("captured_images", exist_ok=True)

    # Save current image
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    new_image = f"captured_images/captured_{timestamp}.jpg"
    cv2.imwrite(new_image, frame)

    print(f"📁 Saved image: {new_image}")

    # REMOVE ALL PREVIOUS IMAGES EXCEPT THIS ONE
    for old_image in glob.glob("captured_images/*.jpg"):
        if old_image != new_image:  # keep the latest file only
            try:
                os.remove(old_image)
                # print(f"🗑 Deleted old image: {old_image}")
            except:
                pass

    return new_image