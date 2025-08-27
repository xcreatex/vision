# import os
# import time
# from scene_description.webcam_capture import capture_image
# from scene_description.describe_scene import describe_image
# from scene_description.speak import speak
# from scene_description.listen_vosk import listen_for_command
# from scene_description.detect_objects import detect_objects
# from rapidfuzz import fuzz

# # Clean up old images
# def clear_old_images(folder="captured_images"):
#     if not os.path.exists(folder):
#         os.makedirs(folder)
#         return
#     for file_name in os.listdir(folder):
#         if file_name.endswith(".jpg"):
#             try:
#                 os.remove(os.path.join(folder, file_name))
#             except Exception as e:
#                 print(f"⚠️ Could not delete {file_name}: {e}")

# # List of acceptable activation words (common variants/mishearings)
# ACTIVATION_WORDS = ["robot", "robit", "robort", "rabot", "rawbot", "rowbot", "assistant", "asistantat","AI","ai","ei"]

# # Phrases that indicate the user wants a command to be run
# TRIGGER_PHRASES = [
#     "describe", "what do you see", "capture", "environment",
#     "tell me what you see", "can you see", "scene", "picture", "show me"
# ]

# # Fuzzy matching thresholds
# ACTIVATION_THRESHOLD = 85
# TRIGGER_THRESHOLD = 80

# def command_matches(text):
#     text = text.lower().strip()

#     # Check for fuzzy match of activation word
#     found_activation = False
#     for word in text.split():
#         for activation in ACTIVATION_WORDS:
#             score = fuzz.ratio(word, activation)
#             if score >= ACTIVATION_THRESHOLD:
#                 found_activation = True
#                 break
#         if found_activation:
#             break

#     if not found_activation:
#         print("❌ No activation word found.")
#         return False

#     # Check for fuzzy match with trigger phrases
#     for trigger in TRIGGER_PHRASES:
#         score = fuzz.partial_ratio(trigger, text)
#         if score >= TRIGGER_THRESHOLD:
#             print(f"✅ Trigger matched: '{trigger}' with score {score}")
#             return True

#     print("❌ No matching trigger phrase found.")
#     return False

# def main():
#     clear_old_images()
#     print("🎬 Voice-triggered scene assistant started (offline mode with Vosk).")
#     print("🎤 Say something like 'describe', 'what do you see', or 'capture again'...\n")

#     while True:
#         try:
#             print("🎧 Listening for command...")
#             command = listen_for_command()
#             # Simulate a text input instead of voice
#             # command = input("📝 Enter a simulated voice command: ")

#             if command_matches(command):
#                 print("📸 Capturing image...")
#                 image_path = capture_image()
#                 print(f"✅ Image captured: {image_path}")

#                 print("🧠 Describing image...")
#                 description = describe_image(image_path)
#                 print(f"🖼️ Scene Description: {description}")

#                 print("🔍 Detecting objects...")
#                 detected_objects = detect_objects(image_path)
#                 if detected_objects:
#                     objects_text = ", ".join(detected_objects)
#                     print(f"📦 Detected objects: {objects_text}")
#                     full_response = f"{description}. I can also see: {objects_text}."
#                 else:
#                     print("📦 No objects detected.")
#                     full_response = description

#                 print("🗣️ Speaking full response...")
#                 speak(full_response)

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



# main.py with Vosk integration + command matching
import os
import time
# Import the new function from describe_scene
from scene_description.webcam_capture import capture_image
from scene_description.describe_scene import describe_all_parts
from scene_description.speak import speak
from scene_description.listen_vosk import listen_for_command

def clear_old_images(folder="captured_images"):
    if not os.path.exists(folder):
        os.makedirs(folder)
        return
    for file_name in os.listdir(folder):
        if file_name.endswith(".jpg"):
            try:
                os.remove(os.path.join(folder, file_name))
            except Exception as e:
                print(f"⚠️ Could not delete {file_name}: {e}")

def command_matches(text):
    # Simple, extendable way to match multiple possible commands
    TRIGGERS = [
        "describe", "what do you see", "capture", "environment",
        "tell me what you see", "can you see", "scene", "picture", "show me"
    ]
    text = text.lower()
    return any(trigger in text for trigger in TRIGGERS)

def main():
    clear_old_images()
    print("🎬 Voice-triggered scene assistant started (offline mode with Vosk).")
    print("🎤 Say something like 'describe', 'what do you see', or 'capture again'...\n")

    while True:
        try:
            print("🎧 Listening for command...")
            command = listen_for_command()

            if command_matches(command):
                print("📸 Capturing image...")
                image_path = capture_image()
                print(f"✅ Image captured: {image_path}")

                print("🧠 Describing image...")
                # Call the new function to describe the three parts
                description = describe_all_parts(image_path)
                print(f"🖼️ Scene Description: {description}")

                print("🗣️ Speaking description...")
                speak(description)
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