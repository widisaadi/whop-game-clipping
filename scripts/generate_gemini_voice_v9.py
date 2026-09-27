import urllib.request
import json
import base64
import wave
import os

API_KEY = os.environ.get("GEMINI_API_KEY", "")

SCRIPT = (
    "This is literally the first ever FPS and fishing game in Roblox! "
    "It is called How to Fisch, and it gets crazy fast! "
    "You start out on a peaceful pier, reeling in floppy fish and weird little crabs. "
    "Until aggressive mutated sea creatures crawl straight out of the water to attack you! "
    "That is right, drop your fishing rod, pull out pistols and shotguns, and fight for your life! "
    "Sell your rare catches to upgrade your weapons and unlock serious military firepower! "
    "Hop in a high speed motorboat, explore deep uncharted waters with your crew, "
    "and blast colossal ocean bosses in full FPS combat for legendary loot! "
    "Think you can survive? Search How to Fisch on Roblox and play right now!"
)

def generate_voice():
    os.makedirs("temp", exist_ok=True)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Read the following gaming voiceover with an intense, punchy, exciting, and cinematic storytelling tone:\n\n{SCRIPT}"
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
        print(json.dumps(res_data, indent=2))
        return False

    out_raw = "temp/voiceover_v9.wav"
    # Write PCM as WAV (Gemini audio is 24kHz, 1-channel 16-bit PCM)
    with wave.open(out_raw, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(24000)
        wav_file.writeframes(audio_bytes)

    print(f"Generated raw voiceover: {out_raw} (Size: {len(audio_bytes)} bytes)")
    return True

if __name__ == "__main__":
    generate_voice()
