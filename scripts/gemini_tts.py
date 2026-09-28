import urllib.request
import json
import base64
import wave
import os
import subprocess
import time

API_KEYS = [k.strip() for k in os.environ.get("GEMINI_API_KEYS", os.environ.get("GEMINI_API_KEY", "")).split(",") if k.strip()]
DEFAULT_VOICE = os.environ.get("GEMINI_VOICE", "Kore")

def request_tts_with_rotation(text, voice_name=None, output_raw_wav="temp/raw_tts.wav"):
    if voice_name is None:
        voice_name = DEFAULT_VOICE
    os.makedirs(os.path.dirname(output_raw_wav), exist_ok=True)
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": text}
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": voice_name
                    }
                }
            }
        }
    }
    
    models = [
        "gemini-2.5-flash-preview-tts",
        "gemini-3.1-flash-tts-preview"
    ]
    
    for key_idx, key in enumerate(API_KEYS):
        print(f"\n[TTS] Trying API Key {key_idx + 1}/{len(API_KEYS)} ({key[:8]}...)...")
        for model in models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
            try:
                print(f"  Attempting model: {model}...")
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    res_data = json.loads(resp.read().decode("utf-8"))
                    
                part = res_data["candidates"][0]["content"]["parts"][0]
                audio_b64 = part["inlineData"]["data"]
                audio_bytes = base64.b64decode(audio_b64)
                
                with wave.open(output_raw_wav, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(24000)
                    wf.writeframes(audio_bytes)
                    
                dur = (len(audio_bytes) / 2) / 24000
                print(f"  [SUCCESS] Audio generated via {model} using Key {key_idx + 1}! Duration: {dur:.2f}s")
                return output_raw_wav
            except Exception as e:
                print(f"  Model {model} failed on Key {key_idx + 1}: {e}")
                time.sleep(1)
                
    raise RuntimeError("All Gemini API keys and models exhausted for TTS generation!")

if __name__ == "__main__":
    test_wav = "temp/test_tts_rotation.wav"
    request_tts_with_rotation("This is a test of the auto-rotating Gemini Puck TTS system.", output_raw_wav=test_wav)
