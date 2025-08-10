# # # # # import speech_recognition as sr

# # # # # def listen_for_trigger(trigger_phrases=None, timeout=5):
# # # # #     if trigger_phrases is None:
# # # # #         trigger_phrases = ["describe", "describe the scene", "what do you see", "scene", "dekho"]

# # # # #     recognizer = sr.Recognizer()
# # # # #     mic = sr.Microphone()

# # # # #     print("🎤 Listening for voice command...")

# # # # #     with mic as source:
# # # # #         recognizer.adjust_for_ambient_noise(source)
# # # # #         try:
# # # # #             audio = recognizer.listen(source, timeout=timeout)
# # # # #             command = recognizer.recognize_google(audio).lower()
# # # # #             print(f"🔊 Heard: {command}")
# # # # #             for trigger in trigger_phrases:
# # # # #                 if trigger in command:
# # # # #                     return True
# # # # #         except sr.WaitTimeoutError:
# # # # #             print("⌛ Listening timed out.")
# # # # #         except sr.UnknownValueError:
# # # # #             print("❌ Could not understand the audio.")
# # # # #         except sr.RequestError as e:
# # # # #             print(f"❌ Speech Recognition error: {e}")
    
# # # # #     return False

# # # # # This replaces your existing listen.py file using offline speech recognition:
# # # # # scene_description/listen_vosk.py
# # # # import queue
# # # # import sounddevice as sd
# # # # import sys
# # # # import json
# # # # from vosk import Model, KaldiRecognizer
# # # # import os
# # # # base_dir = os.path.dirname(os.path.abspath(__file__))
# # # # MODEL_PATH = os.path.join(base_dir, "..", "vosk-model-small-en-in-0.4")

# # # # # Load model
# # # # # MODEL_PATH = "vosk_models/vosk-model-small-en-us-0.15"
# # # # # MODEL_PATH = "vosk-model-small-en-in-0.4"

# # # # model = Model(MODEL_PATH)
# # # # print("📁 Loading Vosk model from:", MODEL_PATH)

# # # # # Create a streaming recognizer
# # # # recognizer = KaldiRecognizer(model, 16000)
# # # # audio_queue = queue.Queue()

# # # # def audio_callback(indata, frames, time, status):
# # # #     if status:
# # # #         print(f"⚠️ Audio status: {status}", file=sys.stderr)
# # # #     audio_queue.put(bytes(indata))

# # # # def listen_for_command():
# # # #     print("🎤 Listening for command (Vosk)...")
# # # #     with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
# # # #                            channels=1, callback=audio_callback):
# # # #         while True:
# # # #             data = audio_queue.get()
# # # #             if recognizer.AcceptWaveform(data):
# # # #                 result = recognizer.Result()
# # # #                 text = json.loads(result).get("text", "")
# # # #                 if text:
# # # #                     print(f"✅ Heard: {text}")
# # # #                     return text

# # # import json
# # # from vosk import Model, KaldiRecognizer
# # # import pyaudio
# # # from difflib import get_close_matches

# # # # --------------------------
# # # # Configurable expected keywords
# # # # --------------------------
# # # EXPECTED_WORDS = [
# # #     "aman", "priya", "rahul", "mumbai", "describe", "what do you see", "abhishek"
# # #     "capture", "again", "scene", "bag", "person", "object", "bottle"
# # # ]

# # # # --------------------------
# # # # Initialize Vosk
# # # # --------------------------
# # # MODEL_PATH = "vosk-model-small-en-in-0.4"

# # # try:
# # #     model = Model(MODEL_PATH)
# # # except Exception as e:
# # #     print(f"❌ Could not load Vosk model from {MODEL_PATH}: {e}")
# # #     exit(1)

# # # rec = KaldiRecognizer(model, 16000)

# # # # --------------------------
# # # # Setup Microphone Input
# # # # --------------------------
# # # p = pyaudio.PyAudio()
# # # stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
# # #                 input=True, frames_per_buffer=8192)
# # # stream.start_stream()

# # # print("🎤 Speak into the mic. Press Ctrl+C to stop.\n")

# # # try:
# # #     while True:
# # #         data = stream.read(4096, exception_on_overflow=False)

# # #         if rec.AcceptWaveform(data):
# # #             result = json.loads(rec.Result())
# # #             text = result.get("text", "").strip().lower()

# # #             if not text:
# # #                 continue

# # #             print(f"📝 Raw recognized: {text}")

# # #             # Try matching with expected words
# # #             match = get_close_matches(text, EXPECTED_WORDS, n=1, cutoff=0.6)
# # #             if match:
# # #                 print(f"✅ Matched as: {match[0]}\n")
# # #             else:
# # #                 print(f"⚠️ No close match found.\n")

# # # except KeyboardInterrupt:
# # #     print("\n🛑 Stopped listening.")
# # #     stream.stop_stream()
# # #     stream.close()
# # #     p.terminate()


# # import json
# # import pyaudio
# # from vosk import Model, KaldiRecognizer
# # from difflib import get_close_matches

# # # --- CONFIGURATION ---

# # MODEL_PATH = "/Users/amankashyap/smart-assistant-scene/vosk-model-small-en-in-0.4"

# # # Add your custom keywords here (all lowercase!)
# # EXPECTED_WORDS = [
# #     "aman", "kashyap", "describe", "what", "see", "capture","rahul", "abhishek","roshni","mantu",
# #     "environment", "hello", "hi", "open", "again"
# # ]

# # # Fuzzy matching threshold (0.6 to 1.0). Lower = more lenient
# # FUZZY_MATCH_THRESHOLD = 0.6

# # # ----------------------


# # def match_fuzzy(word, expected_words):
# #     matches = get_close_matches(word, expected_words, n=1, cutoff=FUZZY_MATCH_THRESHOLD)
# #     return matches[0] if matches else word


# # def main():
# #     # Load model
# #     print("⏳ Loading Vosk model...")
# #     model = Model(MODEL_PATH)

# #     # Initialize recognizer with limited vocabulary (grammar mode)
# #     rec = KaldiRecognizer(model, 16000, json.dumps(EXPECTED_WORDS))

# #     # Setup microphone
# #     p = pyaudio.PyAudio()
# #     stream = p.open(format=pyaudio.paInt16,
# #                     channels=1,
# #                     rate=16000,
# #                     input=True,
# #                     frames_per_buffer=8192)
# #     stream.start_stream()

# #     print("🎤 Listening... (Ctrl+C to stop)\n")

# #     try:
# #         while True:
# #             data = stream.read(4096, exception_on_overflow=False)

# #             if rec.AcceptWaveform(data):
# #                 result = json.loads(rec.Result())
# #                 spoken_text = result.get("text", "").strip()

# #                 if spoken_text:
# #                     print(f"✅ Heard: {spoken_text}")

# #                     # Fuzzy match each word
# #                     corrected = [
# #                         match_fuzzy(word, EXPECTED_WORDS)
# #                         for word in spoken_text.split()
# #                     ]
# #                     print(f"🔍 Matched: {' '.join(corrected)}\n")
# #                 else:
# #                     print("⛔ Silence or unclear speech\n")

# #             else:
# #                 partial = json.loads(rec.PartialResult()).get("partial", "").strip()
# #                 if partial:
# #                     print(f"⏳ Partial: {partial}", end="\r")

# #     except KeyboardInterrupt:
# #         print("\n🛑 Stopped by user.")
# #     finally:
# #         stream.stop_stream()
# #         stream.close()
# #         p.terminate()


# # if __name__ == "__main__":
# #     main()

# import os
# import queue
# import sounddevice as sd
# import vosk
# import json

# # Path to your model
# MODEL_PATH = "/Users/amankashyap/smart-assistant-scene/vosk-model-small-en-in-0.4"
# model = vosk.Model(MODEL_PATH)

# SAMPLERATE = 16000
# DEVICE = None  # Use default microphone

# # 🔐 List of activation phrases
# ACTIVATION_PHRASES = {
#     "describe now AI",
#     "what do you see vision",
#     "capture again vision",
#     "start scene vision"
# }

# def listen_for_activation():
#     q = queue.Queue()

#     def callback(indata, frames, time_info, status):
#         if status:
#             print("⚠️", status)
#         q.put(bytes(indata))

#     with sd.RawInputStream(samplerate=SAMPLERATE, blocksize=8000, device=DEVICE,
#                            dtype='int16', channels=1, callback=callback):
#         print("🕓 Listening for activation phrase...")

#         rec = vosk.KaldiRecognizer(model, SAMPLERATE)

#         while True:
#             data = q.get()
#             if rec.AcceptWaveform(data):
#                 result = json.loads(rec.Result())
#                 text = result.get("text", "").lower().strip()

#                 if text:
#                     print("🗣️ Heard:", text)

#                     for phrase in ACTIVATION_PHRASES:
#                         if phrase in text:
#                             print(f"✅ Matched activation: '{phrase}'")
#                             return phrase  # or return text if needed

# # Example usage
# if __name__ == "__main__":
#     command = listen_for_activation()
#     print("🎯 Final Activation Triggered:", command)

import os
import queue
import sounddevice as sd
import vosk
import json

# Load Vosk model
MODEL_PATH = "/Users/amankashyap/smart-assistant-scene/vosk-model-small-en-in-0.4"
model = vosk.Model(MODEL_PATH)

SAMPLERATE = 16000
DEVICE = None  # Default mic

# Word that must come at the end to activate
ACTIVATION_WORD = "robot"

def listen_for_activation():
    q = queue.Queue()

    def callback(indata, frames, time_info, status):
        if status:
            print("⚠️", status)
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=SAMPLERATE, blocksize=8000, device=DEVICE,
                           dtype='int16', channels=1, callback=callback):
        print("🎙️ Waiting for sentence ending with:", ACTIVATION_WORD)

        rec = vosk.KaldiRecognizer(model, SAMPLERATE)

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").lower().strip()

                if text:
                    print("🗣️ Heard:", text)
                    if text.endswith(ACTIVATION_WORD):
                        print("✅ Activation matched!")
                        return text

# Test
if __name__ == "__main__":
    command = listen_for_activation()
    print("🎯 Activated with:", command)
