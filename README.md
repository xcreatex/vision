
---

# 🎥 Voice-Triggered Scene Assistant (Offline AI)

This project is an **offline AI-powered assistant** that combines **speech recognition, object detection, image captioning, and live navigation guidance**.
It can describe your environment, detect objects, and guide you through navigation using only your voice.

---

## ✨ Features

* 🎤 **Offline voice commands** with [Vosk](https://alphacephei.com/vosk/)
* 🖼 **Scene description** with [BLIP](https://huggingface.co/Salesforce/blip-image-captioning-base)
* 📦 **Object detection** with [YOLOv8](https://github.com/ultralytics/ultralytics)
* 👁 **Object localization** (Left / Center / Right)
* 🧭 **Navigation mode** with real-time video feed and guidance
* 🗣 **Text-to-speech feedback** using `pyttsx3` (offline, no API required)
* ⚡ Works **fully offline**, no internet required after model download

---

## 📂 Project Structure

```
scene-assistant/
│── main.py                      # Entry point (voice commands + control flow)
│── requirements.txt              # Dependencies
│
├── scene_description/            # Core modules
│   ├── webcam_capture.py         # Captures images from webcam
│   ├── describe_scene.py         # BLIP-based scene captioning
│   ├── detect_objects.py         # YOLOv8 object detection + Left/Center/Right division
│   ├── yolo_detector.py          # Wrapper class for YOLO
│   ├── live_navigation.py        # Real-time navigation mode
│   ├── speak.py                  # Offline text-to-speech
│   ├── listen_vosk.py            # Offline speech recognition
│
├── models/                       # Downloaded models
│   ├── yolo/yolov8s.pt           # YOLOv8 pretrained weights
│   ├── blip-image-captioning-base/  # BLIP model (Hugging Face local copy)
│
├── captured_images/              # Saved snapshots
└── README.md
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/xcreatex/vision
cd scene-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Download models

* **YOLOv8**: Already included via Ultralytics (you can also download `yolov8s.pt` into `models/yolo/`)
* **BLIP**: Download [Salesforce/blip-image-captioning-base](https://huggingface.co/Salesforce/blip-image-captioning-base) and place inside `models/blip-image-captioning-base/`
* **Vosk**: Download a model (e.g., [vosk-model-small-en-us](https://alphacephei.com/vosk/models)) and update `listen_vosk.py` to use it

---

## 🎮 Usage

### Run the assistant

```bash
python main.py
```

### Available commands (voice or text simulation)

* **Scene description**

  * "Robot describe"
  * "Assistant, what do you see?"
  * "AI capture scene"

* **Start navigation**

  * "Robot guide me"
  * "AI start navigation"
  * "Assistant help me walk"

* **Stop navigation**

  * "Stop navigation"
  * "Exit navigation"

---

## 🧭 Navigation Mode

When navigation is active:

* Objects are categorized into **Left / Center / Right** regions
* Assistant gives **guidance** if important objects are off-center
* Live video feed shows guidelines
* Press **`q`** to exit manually

---

## 🛠 Requirements

* Python 3.8+
* Webcam & microphone
* Dependencies:

```
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
```

---

## 📌 Future Improvements

* 🔊 Integrate more natural speech synthesis (e.g., Coqui TTS, ElevenLabs)
* 🌍 Multilingual support (Vosk + BLIP multilingual models)
* 🤝 Object-following mode with real-time instructions
* 🧩 Integration with wearable hardware (Raspberry Pi, smart glasses)

---

