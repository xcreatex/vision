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

# ------------------ Utility ------------------

def clear_old_images(folder="captured_images"):
    if not os.path.exists(folder):
        os.makedirs(folder)
        return
    for f in os.listdir(folder):
        if f.endswith(".jpg"):
            try: os.remove(os.path.join(folder,f))
            except: pass


# Activation + triggers (fuzzy)
ACTIVATION_WORDS = ["robot","robit","robort","rabot","rowbot","rawbot","assistant","ai","ei"]

TRIGGER_PHRASES = [
    "describe","what do you see","capture","environment",
    "tell me what you see","can you see","scene","picture","show me"
]

ACTIVATION_THRESHOLD = 85
TRIGGER_THRESHOLD = 80

def command_matches(text:str):
    text = text.lower().strip()
    # Check activation first
    act = any(fuzz.ratio(w,a)>=ACTIVATION_THRESHOLD 
              for w in text.split() for a in ACTIVATION_WORDS)
    if not act: return False
    # Check trigger phrase
    trg = any(fuzz.partial_ratio(t,text)>=TRIGGER_THRESHOLD for t in TRIGGER_PHRASES)
    return trg

def looks_like_question(text:str):
    t=text.lower().strip()
    return ("?" in t) or t.startswith(("what","where","how many","is there","do you see","which"))


# ---------------- MAIN Pipeline ----------------

def main():
    clear_old_images()
    print("\n🎬 SMART SCENE ASSISTANT INITIALIZED")
    print("📸 A new image will be captured for EVERY command/question.\n")

    detector = YOLODetector()

    while True:
        try:
            # Real speech input
            # command = listen_for_command()

            # Manual text for testing
            command=input("\n📝 Enter a command/question: ").strip()

            # ----------- DESCRIPTION MODE ------------
            if command_matches(command) and not looks_like_question(command):
                print("\n📸 Capturing fresh image...")
                img = capture_image()

                print("\n🧠 Describing scene...")
                desc = describe_image(img)
                print("🖼️ Caption:", desc)

                print("\n🔍 Detecting objects + left/center/right mapping...")
                det = detect_objects(img)

                left,center,right = det["left"],det["center"],det["right"]
                guidance = det["guidance"]

                summary=[]
                if left: summary.append(f"Left → {', '.join(left)}")
                if center: summary.append(f"Center → {', '.join(center)}")
                if right: summary.append(f"Right → {', '.join(right)}")

                final = (". ".join(summary) if summary else "No objects detected.")
                nav = " ".join(guidance)

                response=f"{desc}. {final}. {nav}"
                print("\n🗣 Speaking →",response)
                speak(response)

            # ----------- QUESTION ANSWERING -----------
            elif looks_like_question(command):
                print("\n📸 Capturing fresh image for question...")
                img=capture_image()

                print("🔍 YOLO analysis for question...")
                scene=detector.detect_detailed(img,conf=0.45,imgsz=832)
                frame=cv2.imread(img)

                clean=command.lower()
                for a in ACTIVATION_WORDS:
                    if clean.endswith(a):
                        clean=clean[:-len(a)].strip()

                ans=answer_question(clean,scene,image_bgr=frame)
                print("🧠 Answer →",ans)
                speak(ans)

            else:
                print("⚠ Unrecognized input. Say 'describe robot' or ask 'where is bottle'.")
                continue

            print("\n🕓 READY for next voice command.\n")
            time.sleep(1)

        except KeyboardInterrupt:
            print("\n🛑 Session ended.")
            break

if __name__=="__main__":
    main()
