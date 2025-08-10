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

# adding a trigger command word
# import os
# import queue
# import sounddevice as sd
# import vosk
# import json

# # Vosk model path
# MODEL_PATH = "/Users/amankashyap/smart-assistant-scene/vosk-model-small-en-in-0.4"
# model = vosk.Model(MODEL_PATH)

# SAMPLERATE = 16000
# DEVICE = None  # Default microphone

# ACTIVATION_WORD = "robot"

# # Shared listener function
# def listen_once(timeout=7):
#     q = queue.Queue()

#     def callback(indata, frames, time_info, status):
#         if status:
#             print("⚠️", status)
#         q.put(bytes(indata))

#     with sd.RawInputStream(samplerate=SAMPLERATE, blocksize=8000, device=DEVICE,
#                            dtype='int16', channels=1, callback=callback):
#         rec = vosk.KaldiRecognizer(model, SAMPLERATE)
#         result_text = ""

#         import time
#         start_time = time.time()

#         while True:
#             if time.time() - start_time > timeout:
#                 break
#             data = q.get()
#             if rec.AcceptWaveform(data):
#                 result = json.loads(rec.Result())
#                 result_text = result.get("text", "").strip().lower()
#                 if result_text:
#                     return result_text
#     return ""


# def wait_for_activation():
#     print(f"🎙️ Waiting for command ending with '{ACTIVATION_WORD}'...")
#     while True:
#         text = listen_once(timeout=10)
#         if not text:
#             continue
#         print("🗣️ Heard:", text)
#         if text.endswith(ACTIVATION_WORD):
#             print("✅ Activated!")
#             return


# # def listen_for_main_command():
# #     print("🎧 Now listening for your main command...")
# #     text = listen_once(timeout=6)
# #     if text:
# #         print("📥 Command received:", text)
# #         # Here, call your scene description / camera capture logic
# #         # describe_scene()
# #     else:
# #         print("🕓 No command heard.")

# def listen_for_command(timeout=5):
#     q = queue.Queue()

#     def callback(indata, frames, time_info, status):
#         if status:
#             print("⚠️", status)
#         q.put(bytes(indata))

#     with sd.RawInputStream(samplerate=SAMPLERATE, blocksize=8000, device=DEVICE,
#                            dtype='int16', channels=1, callback=callback):
#         print("🎙️ Listening...")
#         rec = vosk.KaldiRecognizer(model, SAMPLERATE)
#         result_text = ""

#         try:
#             import time
#             start_time = time.time()

#             while True:
#                 if time.time() - start_time > timeout:
#                     break
#                 data = q.get()
#                 if rec.AcceptWaveform(data):
#                     result = json.loads(rec.Result())
#                     result_text = result.get("text", "")
#                     print(result_text)
#                     break
#         except Exception as e:
#             print("❌ Vosk error:", e)

#     return result_text.strip()

# # Full assistant loop
# if __name__ == "__main__":
#     while True:
#         wait_for_activation()
#         listen_for_main_command()
#         print("🔁 Waiting for next activation...\n")
