# scene_description/speak.py

import pyttsx3

def _pick_voice(engine):
    """
    Prefer an English male-ish voice on macOS.
    Tries en-IN Rishi first, then any English voice.
    """
    voices = engine.getProperty("voices")

    # 1) Prefer Rishi (Indian English)
    for v in voices:
        if "en-IN" in v.id or "Rishi" in v.name:
            return v.id

    # 2) Otherwise pick any English voice
    for v in voices:
        if "en_" in v.id or "English" in v.name:
            return v.id

    # 3) Fallback: default voice
    return None


def speak(text: str):
    """Speak given text using a fresh engine each time."""
    if not text:
        return

    try:
        engine = pyttsx3.init()

        voice_id = _pick_voice(engine)
        if voice_id:
            engine.setProperty("voice", voice_id)

        # Reasonable speaking speed
        engine.setProperty("rate", 185)

        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print(f"🔈 TTS error: {e}")
        
# for listing of voices present
# import pyttsx3
# engine = pyttsx3.init()
# for v in engine.getProperty('voices'):
#     print(f"{v.id} → {v.name}")
