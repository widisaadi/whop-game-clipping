import os
import urllib.request
import json
import base64
import wave

API_KEY = os.environ.get("GEMINI_API_KEY", "")

SCRIPT = (
    "Think this is just another chill fishing game on Roblox? Think again! "
    "This is How to Fisch, where every catch has a mind of its own! "
    "Start by casting your rod, but instead of normal fish, you reel in floppy shrimp and goofy clams. "
    "Sell your loot to the lighthouse keeper to upgrade your gear and bait. "
    "Because out here, you have to survive against massive bosses like the Spider Crab! "
    "Sail to new islands, unlock weapons, and hunt down legendary sea monsters. "
    "Search How to Fisch on Roblox and play right now!"
)

def generate_voice():
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Read the following gaming voiceover with an energetic, engaging, and exciting storytelling tone:\n\n{SCRIPT}"
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

    out_wav = "temp/gemini_voiceover_achird.wav"
    with wave.open(out_wav, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2) # 16-bit
        wav_file.setframerate(24000)
        wav_file.writeframes(audio_bytes)

    duration = (len(audio_bytes) / 2) / 24000
    print(f"Saved complete Gemini WAV voiceover to: {out_wav} (Duration: {duration:.2f}s)")

if __name__ == "__main__":
    generate_voice()
