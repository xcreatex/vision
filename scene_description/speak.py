

import pyttsx3

def speak(text):
    engine = pyttsx3.init()

    # Set voice to English male
    # voices = engine.getProperty('voices')
    # for voice in voices:
    #     if "english" in voice.name.lower() and "male" in voice.name.lower():
    #         engine.setProperty('voice', voice.id)
    #         break
    #     elif "english" in voice.name.lower():
    #         engine.setProperty('voice', voice.id)
#
    # engine.setProperty('voice', 'com.apple.speech.synthesis.voice.daniel')  # or alex, fred, etc.        
    engine.setProperty('voice', 'com.apple.voice.compact.en-IN.Rishi → Rishi')  # or alex, fred, etc.        
    engine.setProperty('rate', 180)  # Speed
    engine.setProperty('volume', 1.0)  # Volume

    engine.say(text)
    engine.runAndWait()

# for listing of voices present
import pyttsx3
engine = pyttsx3.init()
for v in engine.getProperty('voices'):
    print(f"{v.id} → {v.name}")
