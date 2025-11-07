# import os
# import time
# import cv2
# from scene_description.webcam_capture import capture_image
# from scene_description.describe_scene import describe_image
# from scene_description.speak import speak
# from scene_description.listen_vosk import listen_for_command
# from scene_description.detect_objects import detect_objects
# from scene_description.yolo_detector import YOLODetector
# from scene_description.question_answer import answer_question
# from rapidfuzz import fuzz

# # ------------------ Utility Functions ------------------

# def clear_old_images(folder="captured_images"):
#     """Deletes previously captured images to avoid clutter."""
#     if not os.path.exists(folder):
#         os.makedirs(folder)
#         return
#     for file_name in os.listdir(folder):
#         if file_name.endswith(".jpg"):
#             try:
#                 os.remove(os.path.join(folder, file_name))
#             except Exception as e:
#                 print(f"⚠️ Could not delete {file_name}: {e}")


# # Activation words and triggers (fuzzy)
# ACTIVATION_WORDS = [
#     "robot", "robit", "robort", "rabot", "rawbot", "rowbot",
#     "assistant", "ai", "ei"
# ]

# TRIGGER_PHRASES = [
#     "describe", "what do you see", "capture", "environment",
#     "tell me what you see", "can you see", "scene", "picture", "show me"
# ]

# ACTIVATION_THRESHOLD = 85
# TRIGGER_THRESHOLD = 80


# def command_matches(text):
#     """Checks if the spoken text contains an activation + trigger phrase."""
#     text = text.lower().strip()
#     found_activation = False

#     for word in text.split():
#         for activation in ACTIVATION_WORDS:
#             if fuzz.ratio(word, activation) >= ACTIVATION_THRESHOLD:
#                 found_activation = True
#                 break
#         if found_activation:
#             break

#     if not found_activation:
#         print("❌ No activation word found.")
#         return False

#     for trigger in TRIGGER_PHRASES:
#         if fuzz.partial_ratio(trigger, text) >= TRIGGER_THRESHOLD:
#             print(f"✅ Trigger matched: '{trigger}'")
#             return True

#     print("❌ No matching trigger phrase found.")
#     return False


# def looks_like_question(text: str) -> bool:
#     """Rudimentary detection for question-type queries."""
#     t = text.lower().strip()
#     return ("?" in t) or t.startswith(
#         ("what", "where", "how many", "is there", "do you see")
#     )


# # ------------------ Main Loop ------------------

# def main():
#     clear_old_images()
#     print("🎬 Voice-triggered scene assistant started (offline mode with Vosk).")
#     print("🎤 Say something like 'describe robot', or ask a question like 'where is the board?'...\n")

#     detector_detail = YOLODetector()  # YOLO for detailed detections
#     last_image_path = None  # Cache last image for Q&A reuse

#     while True:
#         try:
#             # Option A (real voice)
#             # command = listen_for_command()

#             # Option B (manual text input for testing)
#             command = input("📝 Enter a simulated voice command: ")

#             # --- Describe scene branch ---
#             if command_matches(command) and not looks_like_question(command):
#                 print("📸 Capturing image...")
#                 image_path = capture_image()
#                 last_image_path = image_path
#                 print(f"✅ Image captured: {image_path}")

#                 print("🧠 Describing image...")
#                 description = describe_image(image_path)
#                 print(f"🖼️ Scene Description: {description}")

#                 print("🔍 Detecting objects (regions)...")
#                 detections = detect_objects(image_path)

#                 left = detections["left"]
#                 center = detections["center"]
#                 right = detections["right"]
#                 guidance = detections["guidance"]

#                 objects_text = []
#                 if left:
#                     objects_text.append(f"On the left: {', '.join(left)}")
#                 if center:
#                     objects_text.append(f"In the center: {', '.join(center)}")
#                 if right:
#                     objects_text.append(f"On the right: {', '.join(right)}")

#                 final_detection_text = (
#                     " | ".join(objects_text) if objects_text else "No objects detected."
#                 )

#                 if guidance:
#                     print("🧭 Guidance:")
#                     for g in guidance:
#                         print("   -", g)
#                 else:
#                     print("🧭 No special guidance needed.")

#                 full_response = f"{description}. {final_detection_text}. " + " ".join(
#                     guidance
#                 )

#                 print("🗣️ Speaking full response...")
#                 speak(full_response)

#             # --- Q&A branch ---
#             elif looks_like_question(command):
#                 if last_image_path is None:
#                     print("📸 No recent image. Capturing one now for Q&A...")
#                     last_image_path = capture_image()

#                 print("🔎 Analyzing scene for Q&A...")
#                 scene_state = detector_detail.detect_detailed(
#                     last_image_path, conf=0.45, imgsz=832
#                 )
#                 image_bgr = cv2.imread(last_image_path)

#                 ans = answer_question(command, scene_state, image_bgr=image_bgr)
#                 print(f"🧠 Answer: {ans}")
#                 speak(ans)

#             # --- No match ---
#             else:
#                 print("🔇 No valid command detected. Heard:", command)

#         except KeyboardInterrupt:
#             print("\n🛑 Assistant stopped by user.")
#             break
#         except Exception as e:
#             print(f"❌ Error: {e}")
#             time.sleep(3)


# if __name__ == "__main__":
#     main()

import os
import time
import cv2
from scene_description.webcam_capture import capture_image
from scene_description.describe_scene import describe_image
from scene_description.speak import speak
from scene_description.listen_vosk import listen_for_command
from scene_description.detect_objects import detect_objects
from scene_description.yolo_detector import YOLODetector
from scene_description.question_answer import answer_question
from rapidfuzz import fuzz

# ------------------ Utility Functions ------------------

def clear_old_images(folder="captured_images"):
    """Deletes previously captured images to avoid clutter."""
    if not os.path.exists(folder):
        os.makedirs(folder)
        return
    for file_name in os.listdir(folder):
        if file_name.endswith(".jpg"):
            try:
                os.remove(os.path.join(folder, file_name))
            except Exception as e:
                print(f"⚠️ Could not delete {file_name}: {e}")


# Activation words and triggers (fuzzy)
ACTIVATION_WORDS = [
    "robot", "robit", "robort", "rabot", "rawbot", "rowbot",
    "assistant", "ai", "ei"
]

TRIGGER_PHRASES = [
    "describe", "what do you see", "capture", "environment",
    "tell me what you see", "can you see", "scene", "picture", "show me"
]

ACTIVATION_THRESHOLD = 85
TRIGGER_THRESHOLD = 80


def command_matches(text):
    """Checks if the spoken text contains an activation + trigger phrase."""
    text = text.lower().strip()
    found_activation = False

    for word in text.split():
        for activation in ACTIVATION_WORDS:
            if fuzz.ratio(word, activation) >= ACTIVATION_THRESHOLD:
                found_activation = True
                break
        if found_activation:
            break

    if not found_activation:
        print("❌ No activation word found.")
        return False

    for trigger in TRIGGER_PHRASES:
        if fuzz.partial_ratio(trigger, text) >= TRIGGER_THRESHOLD:
            print(f"✅ Trigger matched: '{trigger}'")
            return True

    print("❌ No matching trigger phrase found.")
    return False


def looks_like_question(text: str) -> bool:
    """Rudimentary detection for question-type queries."""
    t = text.lower().strip()
    return ("?" in t) or t.startswith(
        ("what", "where", "how many", "is there", "do you see")
    )


# ------------------ Main Loop ------------------

def main():
    clear_old_images()
    print("🎬 Voice-triggered scene assistant started (offline mode with Vosk).")
    print("🎤 Say something like 'describe robot', or ask questions like 'where is the bottle?' or 'what color is it?'...\n")

    detector_detail = YOLODetector()  # YOLO for detailed detections
    last_image_path = None  # Cache last image for Q&A reuse

    while True:
        try:
            # Option A (real voice)
            # command = listen_for_command()

            # Option B (manual text input for testing)
            command = input("📝 Enter a simulated voice command: ")

            # --- Describe scene branch ---
            if command_matches(command) and not looks_like_question(command):
                print("📸 Capturing image...")
                image_path = capture_image()
                last_image_path = image_path
                print(f"✅ Image captured: {image_path}")

                print("🧠 Describing image...")
                description = describe_image(image_path)
                print(f"🖼️ Scene Description: {description}")

                print("🔍 Detecting objects (regions)...")
                detections = detect_objects(image_path)

                left = detections["left"]
                center = detections["center"]
                right = detections["right"]
                guidance = detections["guidance"]

                objects_text = []
                if left:
                    objects_text.append(f"On the left: {', '.join(left)}")
                if center:
                    objects_text.append(f"In the center: {', '.join(center)}")
                if right:
                    objects_text.append(f"On the right: {', '.join(right)}")

                final_detection_text = (
                    " | ".join(objects_text) if objects_text else "No objects detected."
                )

                if guidance:
                    print("🧭 Guidance:")
                    for g in guidance:
                        print("   -", g)
                else:
                    print("🧭 No special guidance needed.")

                full_response = f"{description}. {final_detection_text}. " + " ".join(
                    guidance
                )

                print("🗣️ Speaking full response...")
                speak(full_response)

            # --- Q&A branch ---
            elif looks_like_question(command):
                if last_image_path is None:
                    print("📸 No recent image. Capturing one now for Q&A...")
                    last_image_path = capture_image()

                print("🔎 Analyzing scene for Q&A...")
                scene_state = detector_detail.detect_detailed(
                    last_image_path, conf=0.45, imgsz=832
                )
                image_bgr = cv2.imread(last_image_path)

                # Remove activation word from end of question (for better Q&A)
                clean_command = command.lower().strip()
                for word in ACTIVATION_WORDS:
                    if clean_command.endswith(word):
                        clean_command = clean_command[: -len(word)].strip()
                        break

                ans = answer_question(clean_command, scene_state, image_bgr=image_bgr)
                print(f"🧠 Answer: {ans}")
                speak(ans)

            # --- No match ---
            else:
                print("🔇 No valid command detected. Heard:", command)

        except KeyboardInterrupt:
            print("\n🛑 Assistant stopped by user.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(3)


if __name__ == "__main__":
    main()
