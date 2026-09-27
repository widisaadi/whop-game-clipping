import urllib.request
import json
import base64
import wave
import os
import subprocess

API_KEY = os.environ.get("GEMINI_API_KEY", "")

SCRIPT = (
    "He swore he hated her... but enemies do not look at each other like this. "
    "The moment he pinned her against the wall, everything changed. "
    "She fell first... but he fell so much harder. "
    "You have to watch Lessons in Love and Hate on Shorts right now!"
)

TEMP_DIR = r"d:\create something\local\tiktokclipping\temp\lessons_in_love_and_hate"
os.makedirs(TEMP_DIR, exist_ok=True)

def generate_voice():
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "Read the following romance drama voiceover with an emotional, compelling, breathless storytelling tone. "
                            "Captivate the listener with intense romantic suspense and clear pronunciation:\n\n"
                            f"{SCRIPT}"
                        )
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": "Aoede"
                    }
                }
            }
        }
    }

    print("Requesting voiceover from Gemini TTS...")
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

    out_raw = os.path.join(TEMP_DIR, "vo_raw.wav")
    with wave.open(out_raw, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2) # 16-bit
        wav_file.setframerate(24000)
        wav_file.writeframes(audio_bytes)

    duration = (len(audio_bytes) / 2) / 24000
    print(f"Saved raw voiceover to {out_raw} (Duration: {duration:.2f}s)")

    # Resample to 48kHz stereo and adjust tempo slightly (1.08x) for crisp pacing
    out_final = os.path.join(TEMP_DIR, "vo_48k.wav")
    cmd = [
        "ffmpeg", "-y", "-i", out_raw,
        "-filter:a", "atempo=1.06,aresample=48000",
        "-ac", "2", out_final
    ]
    subprocess.run(cmd, check=True)
    
    # Get final duration
    p_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", out_final]
    final_dur = float(subprocess.check_output(p_cmd).decode("utf-8").strip())
    print(f"Final 48kHz VO ready at {out_final} (Duration: {final_dur:.2f}s)")
    return out_final, final_dur

if __name__ == "__main__":
    generate_voice()
