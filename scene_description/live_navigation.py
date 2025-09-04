import cv2
from scene_description.detect_objects import detect_objects
from scene_description.speak import speak

def start_navigation():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise IOError("❌ Cannot open webcam")

    print("🎥 Live navigation started. Say 'stop navigation' or press 'q' to quit.")

    navigation_active = True
    while navigation_active:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to grab frame")
            break

        # Save frame temporarily for processing
        image_path = "temp_frame.jpg"
        cv2.imwrite(image_path, frame)

        # Detect objects and guidance
        detections = detect_objects(image_path)

        left = detections["left"]
        center = detections["center"]
        right = detections["right"]
        guidance = detections["guidance"]

        # Build response text
        objects_text = []
        if left: objects_text.append(f"Left: {', '.join(left)}")
        if center: objects_text.append(f"Center: {', '.join(center)}")
        if right: objects_text.append(f"Right: {', '.join(right)}")

        detection_summary = " | ".join(objects_text) if objects_text else "No objects detected."
        guidance_text = " ".join(guidance) if guidance else "No guidance needed."

        response = f"{detection_summary}. {guidance_text}"

        print("📢", response)
        speak(response)

        # Show video feed with guidelines
        h, w, _ = frame.shape
        cv2.line(frame, (w//3, 0), (w//3, h), (0, 255, 0), 2)
        cv2.line(frame, (2*w//3, 0), (2*w//3, h), (0, 255, 0), 2)
        cv2.imshow("Live Navigation", frame)

        # Press q to quit (manual stop)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("🛑 Live navigation stopped.")
