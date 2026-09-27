import urllib.request
import json
import base64
import wave
import os

API_KEY = os.environ.get("GEMINI_API_KEY", "")

SCRIPTS = {
    "v12": {
        "id": "12_tongue_escape_most_illegal_obby",
        "text": (
            "I think I just found the most illegal obby on Roblox, and how is this even allowed?! "
            "In +1 Tongue Escape, you literally grow your tongue into a massive highway to bypass impossible death traps! "
            "Hop on the x99 treadmill to grind out crazy studs, jump across raging lava chasms, and conquer Stage 8 to flex on the leaderboards! "
            "Play +1 Tongue Escape on Roblox, link is in my bio!"
        )
    },
    "v13": {
        "id": "13_tongue_escape_nobody_told_me",
        "text": (
            "Nobody told me this Roblox obby gets this completely insane! "
            "In +1 Tongue Escape, normal jumping is impossible—you have to spit out a giant tongue to bridge crazy gaps! "
            "Train on high-speed treadmills to level up your reach, survive brutal moving lava obstacles, and flex Stage 8 on the global leaderboards! "
            "Play +1 Tongue Escape on Roblox, link is in my bio!"
        )
    },
    "v14": {
        "id": "14_tongue_escape_broke_physics",
        "text": (
            "This new Roblox game completely broke obby physics! "
            "Instead of regular parkour, +1 Tongue Escape lets you stretch your tongue thousands of studs across the map! "
            "Speed train in the gym for insane multipliers, cross deadly lava chasms without touching the floor, and race your friends to the top of the leaderboards! "
            "Play +1 Tongue Escape on Roblox, link is in my bio!"
        )
    }
}

def generate_voice(vid_key, script_info):
    os.makedirs("temp/tongue_escape", exist_ok=True)
    out_wav = f"temp/tongue_escape/voiceover_{vid_key}.wav"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={API_KEY}"
    
    prompt = (
        "Read the following Roblox gaming promotional voiceover with an ultra FAST-PACED, high-energy, rapid-fire, punchy, and highly enthusiastic gaming delivery. "
        "Pronounce '+1 Tongue Escape' clearly as 'Plus One Tongue Escape'. "
        "No dead pauses, high momentum from the first word to the last:\n\n"
        f"{script_info['text']}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
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

    print(f"\nRequesting fast-paced voiceover for {vid_key} ({script_info['id']}) from Gemini Aoede...")
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=60) as response:
        res_data = json.loads(response.read().decode("utf-8"))

    audio_bytes = None
    for candidate in res_data.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            inline_data = part.get("inlineData") or part.get("inline_data")
            if inline_data and "data" in inline_data:
                audio_bytes = base64.b64decode(inline_data["data"])
                break

    if not audio_bytes:
        raise RuntimeError(f"No audio data found in response for {vid_key}: {res_data}")

    with wave.open(out_wav, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(24000)
        wav_file.writeframes(audio_bytes)

    duration = (len(audio_bytes) / 2) / 24000
    print(f"--> Saved {out_wav} (Duration: {duration:.2f}s)")
    return out_wav, duration

def main():
    results = {}
    for key, info in SCRIPTS.items():
        out_wav, dur = generate_voice(key, info)
        results[key] = dur
    print("\nAll voiceovers generated successfully:")
    for k, d in results.items():
        print(f"- {k}: {d:.2f} seconds")

if __name__ == "__main__":
    main()
