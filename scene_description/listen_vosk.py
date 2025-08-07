import os
import queue
import sounddevice as sd
import vosk
import json

# Path to the Vosk model folder (unzip first!)
# MODEL_PATH = "/Users/amankashyap/smart-assistant-scene/vosk-model-small-en-in-0.4"
MODEL_PATH = "/Users/amankashyap/smart-assistant-scene/vosk-model-small-en-in-0.4"

# Load model once
model = vosk.Model(MODEL_PATH)

# Audio recording parameters
SAMPLERATE = 16000
DEVICE = None  # Use default microphone

def listen_for_command(timeout=5):
    q = queue.Queue()

    def callback(indata, frames, time_info, status):
        if status:
            print("⚠️", status)
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=SAMPLERATE, blocksize=8000, device=DEVICE,
                           dtype='int16', channels=1, callback=callback):
        print("🎙️ Listening...")
        rec = vosk.KaldiRecognizer(model, SAMPLERATE)
        result_text = ""

        try:
            import time
            start_time = time.time()

            while True:
                if time.time() - start_time > timeout:
                    break
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    result_text = result.get("text", "")
                    print(result_text)
                    break
        except Exception as e:
            print("❌ Vosk error:", e)

    return result_text.strip()
