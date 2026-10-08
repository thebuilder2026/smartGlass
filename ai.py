import os
import requests
from dotenv import load_dotenv

load_dotenv()

SYSTEM = """You are a concise smart-glasses scene assistant.
Use only the detected-object context given to you.
Give short mobility-oriented guidance. Do not invent objects or claim certainty."""

def fallback(summary, alerts):
    return " ".join(alerts[:3]) if alerts else summary

def scene_guidance(summary, alerts):
    key = os.getenv("GROQ_API_KEY","").strip()
    model = os.getenv("GROQ_MODEL","llama-3.1-8b-instant").strip()
    if not key:
        return fallback(summary, alerts), "Local guidance"
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"},
            json={
                "model":model,
                "messages":[
                    {"role":"system","content":SYSTEM},
                    {"role":"user","content":f"Scene: {summary}\nAlerts: {alerts}"}
                ],
                "temperature":0.1,
                "max_tokens":120
            },
            timeout=20
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"], f"AI mode: {model}"
    except Exception:
        return fallback(summary, alerts), "Fallback local guidance"
