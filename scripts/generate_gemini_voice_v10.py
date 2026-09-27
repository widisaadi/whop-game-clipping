import urllib.request
import json
import base64
import wave
import os

API_KEY = os.environ.get("GEMINI_API_KEY", "")

SCRIPT = (
    "I found one of the weirdest Roblox games you will ever play! "
    "It is called How to Fisch, and nothing makes sense here! "
    "Instead of regular worms, you literally fish using living burritos as bait! "
    "You meet an old granny on a lighthouse who sells you heavy shotguns and military crowbars! "
    "And when you reel in a catch, it is not a bass, it is a mutant beast trying to punch you! "
    "Earn crazy cash selling your weird catches to buy overpowered weapons! "
    "Then squad up with friends to hunt down giant ocean monsters! "
    "Are you ready for the weirdest catch? Search How to Fisch on Roblox and play right now!"
)

def generate_voice():
    os.makedirs("temp", exist_ok=True)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Read the following gaming voiceover with a humorous, bewildered, high-energy storytelling tone:\n\n{SCRIPT}"
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
        print("ERROR: No audio data returned from Gemini TTS!")
        return False

    out_raw = "temp/voiceover_v10.wav"
    with wave.open(out_raw, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(24000)
        wav_file.writeframes(audio_bytes)

    print(f"Generated raw voiceover: {out_raw} (Size: {len(audio_bytes)} bytes)")
    return True

if __name__ == "__main__":
    generate_voice()
