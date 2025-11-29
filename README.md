# 👁️🗣️ Offline Smart Scene Assistant (Webcam + YOLO + BLIP + Vosk)

This project is an **offline**, voice-triggered **visual assistant** that:

- Captures images from your **webcam**
- Describes the scene using a **BLIP image captioning** model
- Detects objects and their **spatial position** (left / center / right) using **YOLOv8**
- Answers **questions** about the scene (e.g., *“how many bottles do you see?”*, *“where is the person?”*, *“what color is the bottle?”*)
- Works with **voice commands** via **Vosk** (or text input during testing)
- Speaks responses using **offline TTS (pyttsx3)**

> 🔁 **New behavior:** For **every** command or question, the assistant captures a **fresh image** from the webcam and processes that frame. No stale frames are reused.

---

## ✨ Features

### 1. Scene Description
Triggered by commands such as:

- `describe robot`
- `what do you see robot`
- `capture robot`
- `tell me what you see robot`

Behavior:

- Captures a **new image** from webcam
- Runs BLIP to generate a **natural language caption**
- Runs YOLOv8 to detect objects and divides them into **left / center / right** regions
- Generates **navigation-style guidance**, e.g.:
  - *“The bottle is on the left, move the camera slightly right.”*
- Speaks a combined response like:
  > “A woman standing in a messy room with a bottle of water.  
  > In the center: person, bottle. Main objects are centered. Good framing.”

---

### 2. Object Position + Navigation (Left / Center / Right)

Using `detect_objects.py` + YOLO:

- Each detected object is assigned to one of:
  - **Left** – object’s center x < 1/3 of image width  
  - **Center** – between 1/3 and 2/3  
  - **Right** – > 2/3
- The assistant summarizes object layout:
  - *“Left → chair, table | Center → person | Right → bottle”*
- It then gives **guidance** like:
  - *“The bottle is on the left, please move right to center it.”*

This is the basis for **navigation help** (especially useful for visually impaired users).

---

### 3. Question Answering about the Scene

After any command (description or otherwise), you can ask **questions**, e.g.:

- **Presence**
  - `is there a person`
  - `do you see any bottle`
- **Count**
  - `how many bottles do you see`
  - `count chairs`
- **Location**
  - `where is the person`
  - `location of the bottle`
- **Center**
  - `what is in the center`
  - `what’s in the middle`
- **Listing**
  - `what do you see`
  - `what objects do you see`
- **Color**
  - `what color is the bottle`
  - `what colour is the chair`

The logic lives in `scene_description/question_answer.py` and uses:

- **Regex-based intent parsing** (presence, count, where, color, etc.)
- A small **synonym map** so things like `"person"` match YOLO labels `"man"` / `"woman"`, `"bottle"` matches `"water bottle"`, etc.
- A simple **dominant color** estimator inside the bounding box (HSV → basic colors like red, green, blue, etc.)

💡 For every question, the assistant **captures a fresh image** and runs YOLO on it before answering.

---

### 4. Voice Commands (Offline – Vosk)

The project uses **Vosk** for offline speech recognition (via `listen_vosk.py`):

- Listens to microphone input
- Transcribes to text offline using the model:
  - `vosk-model-small-en-in-0.4` (recommended for Indian English)
- Supports activation words, like:
  - `robot`, `assistant`, `ai`, etc.

For development/testing, `main.py` also supports **manual text input** instead of real voice so you can test without speaking.

---

### 5. Offline Text-to-Speech

Using `pyttsx3` in `speak.py`, all responses are spoken offline:

- No network required
- Uses a selected **system voice** (configurable)
- Reads:
  - Scene descriptions
  - Object summaries
  - Question answers

---

## 🧱 Project Structure

```bash
smart-assistant-scene/
├── main.py                        # Main voice/text-driven loop (fresh image per command)
├── requirements.txt               # Python dependencies
├── models/
│   ├── blip-image-captioning-base/ # Local BLIP model (from Hugging Face)
│   └── yolo/
│       └── yolov8s.pt             # YOLOv8s weights
├── vosk-model-small-en-in-0.4/    # Vosk speech model (unzipped)
├── captured_images/               # Auto-created; stores captured frames
└── scene_description/
    ├── __init__.py
    ├── webcam_capture.py          # Captures a frame from the webcam
    ├── describe_scene.py          # BLIP captioning
    ├── speak.py                   # pyttsx3 TTS
    ├── listen_vosk.py             # Vosk streaming recognition
    ├── detect_objects.py          # YOLO + left/center/right + guidance
    ├── yolo_detector.py           # YOLO wrapper for detailed detections
    └── question_answer.py         # Scene-based Q&A engine (presence, count, where, color, etc.)
```

---

## ⚙️ Installation

### 1. Clone the Repo

```bash
git clone https://github.com/amankashyap00/vision.git -b region-divison
cd vision
```

### 2. Create & Activate Virtual Environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
# On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should include (at minimum):

```text
torch
torchvision
torchaudio
transformers
ultralytics
opencv-python
Pillow
numpy
sounddevice
scipy
vosk
pyttsx3
rapidfuzz
```

---

## 📥 Model Setup (Offline)

### 1. BLIP Model (Image Captioning)

Download from Hugging Face:

* Model: `Salesforce/blip-image-captioning-base`

Either:

* Use `from_pretrained("Salesforce/blip-image-captioning-base")` once online and cache it, or
* Manually download and place it under:

```bash
models/blip-image-captioning-base/
```

`scene_description/describe_scene.py` expects:

```python
MODEL_DIR = "./models/blip-image-captioning-base"
processor = BlipProcessor.from_pretrained(MODEL_DIR)
model = BlipForConditionalGeneration.from_pretrained(MODEL_DIR)
```

---

### 2. YOLOv8 Model

Download YOLOv8s weights using ultralytics once (online):

```bash
from ultralytics import YOLO
YOLO("yolov8s.pt")
```

Then put `yolov8s.pt` under:

```bash
models/yolo/yolov8s.pt
```

`yolo_detector.py` uses:

```python
class YOLODetector:
    def __init__(self, model_path="models/yolo/yolov8s.pt"):
        self.model = YOLO(model_path)
```

---

### 3. Vosk Model

Download a small English-India model (for example):

* `vosk-model-small-en-in-0.4`

Unzip it into the project root:

```bash
vosk-model-small-en-in-0.4/
```

`listen_vosk.py` points to this path, e.g.:

```python
MODEL_PATH = "/Users/<you>/smart-assistant-scene/vosk-model-small-en-in-0.4"
```

Update the path to match your system.

---

## ▶️ Running the Assistant

From the project root (with `venv` activated):

```bash
python main.py
```

You’ll see something like:

```text
🎬 Voice-triggered scene assistant started (offline mode with Vosk).
🎤 Say 'describe robot' or ask things like 'where is the bottle', 'how many chairs', 'what color is the bottle'...
📝 Enter a simulated voice command:
```

### Testing with Text Commands (Recommended First)

You can type:

* `describe robot`
* `what do you see`
* `how many bottles do you see`
* `where is the person`
* `what color is the bottle`

For each command:

1. A **new frame** is captured from webcam.
2. Depending on command:

   * Description → BLIP + YOLO + guidance
   * Q&A → YOLO detailed detection + question_answer logic
3. Response is printed and spoken aloud.

### Switching to Real Voice

In `main.py`, swap:

```python
# command = listen_for_command()
command = input("📝 Enter a simulated voice command: ").strip()
```

to:

```python
command = listen_for_command()
# command = input("📝 Enter a simulated voice command: ").strip()
```

Make sure your mic works and Vosk is correctly configured.

---

## 🧪 Example Interactions

```text
📝 Enter a simulated voice command: describe robot
→ captures new image
→ "a woman standing in a messy room with a bottle of water.
   In the center: person, bottle. Main objects are centered. Good framing."

📝 Enter a simulated voice command: how many bottles do you see
→ captures new image
→ "I see 2 bottles."

📝 Enter a simulated voice command: where is the person
→ captures new image
→ "The person is in the center."

📝 Enter a simulated voice command: what color is the bottle
→ captures new image
→ "The bottle looks green."
```

---

## 🛠️ Current Status / TODO

* ✅ Works fully **offline** after models are downloaded
* ✅ Fresh frame processing per command/question
* ✅ Basic Q&A (presence, count, where, color, list, center)
* ✅ Left / center / right navigation hints

**Planned / Possible Extensions:**

* [ ] Short-term conversational memory (understand follow-ups like *“what color is it?”* where “it” is the last-referenced object)
* [ ] Continuous **live video mode** (frame-by-frame analysis + navigation)
* [ ] Better object synonym coverage and more robust NLU
* [ ] Support for multiple languages (Vosk + multilingual TTS)

---

## 💡 Notes

* Tested on **macOS** with a **webcam**, Python 3.10+.
* On first use, BLIP & YOLO may be slow as they load into memory.
* For smoother performance, avoid very large camera resolutions.

---

Happy hacking! 🤖📷🗣️
If you use or extend this project, consider starring the repo and sharing your use case.
