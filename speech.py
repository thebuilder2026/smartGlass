import os
import time
from dotenv import load_dotenv

load_dotenv()
SPEECH_COOLDOWN = float(os.getenv("SPEECH_COOLDOWN_SECONDS", "4"))
_last_spoken = {}
_engine = None

def _get_engine():
    global _engine
    if _engine is None:
        import pyttsx3
        _engine = pyttsx3.init()
        _engine.setProperty("rate", 175)
    return _engine

def speak(text, force=False):
    if not text:
        return False
    now = time.time()
    if not force and now - _last_spoken.get(text, 0) < SPEECH_COOLDOWN:
        return False
    try:
        engine = _get_engine()
        engine.say(text)
        engine.runAndWait()
        _last_spoken[text] = now
        return True
    except Exception:
        return False
