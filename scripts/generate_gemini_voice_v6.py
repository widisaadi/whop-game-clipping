import urllib.request
import json
import base64
import wave
import os

API_KEY = os.environ.get("GEMINI_API_KEY", "")

SCRIPT = (
    "Wait, why does this Roblox fishing game give you actual weapons?! "
    "In How to Fisch, Island 1 starts off like a normal chill fishing game. "
    "But once you visit the secret island trader, you can buy heavy shotguns and living bait! "
    "Because when the alarm sounds, mutant sea beasts will raid the shore to take your catch! "
    "Grab your firepower and team up to take down colossal ocean bosses! "
    "Think you can survive the raid? Search How to Fisch on Roblox and play right now!"
)

def generate_voice():
    os.makedirs("temp", exist_ok=True)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Read the following gaming voiceover with an energetic, punchy, engaging, and exciting storytelling tone:\n\n{SCRIPT}"
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": "Achird"
                    }
                }
            }
        }
    }

    print("Requesting voiceover from gemini-3.1-flash-tts-preview (Voice: Achird)...")
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode("utf-8"))

    audio_bytes = None
    for candidate in res_data.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            inline_data = part.get("inlineData") or part.get("inline_data")
            if inline_data and "data" in inline_data:
                audio_bytes = base64.b64decode(inline_data["data"])
                break

    if not audio_bytes:
        raise RuntimeError(f"No audio data found in response: {res_data}")

    print(f"Received {len(audio_bytes)} raw audio bytes.")

    out_wav = "temp/voiceover_v6.wav"
    with wave.open(out_wav, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2) # 16-bit
        wav_file.setframerate(24000)
        wav_file.writeframes(audio_bytes)

    duration = (len(audio_bytes) / 2) / 24000
    print(f"Saved complete Gemini WAV voiceover to: {out_wav} (Duration: {duration:.2f}s)")
    return out_wav, duration

if __name__ == "__main__":
    generate_voice()
