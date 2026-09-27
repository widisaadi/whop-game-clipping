import os
import urllib.request
import json
import base64

API_KEY = os.environ.get("GEMINI_API_KEY", "")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

with open("temp/how_to_fisch/voiceover_htf_v13_fast.wav", "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode("utf-8")

payload = {
    "contents": [{
        "parts": [
            {
                "text": (
                    "Here is an audio recording of a gaming voiceover: "
                    "'In Roblox, fishing will literally get you attacked! "
                    "In How to Fisch, you cast your rod for a calm catch, "
                    "until a mutant Piranha Boss leaps out to eat you alive! "
                    "Sprint to Granny to buy shotguns and lethal bait, "
                    "then lock your iron sights to wipe out its health bar! "
                    "Hop into your motorboat to raid colossal ocean titans! "
                    "Search How to Fisch on Roblox!'\n\n"
                    "Provide exact word-by-word timestamps in seconds in JSON format: "
                    "[{\"word\": \"In\", \"start\": 0.0, \"end\": 0.2}, ...]. "
                    "Output ONLY raw JSON array, no markdown markdown formatting."
                )
            },
            {
                "inline_data": {
                    "mime_type": "audio/wav",
                    "data": audio_b64
                }
            }
        ]
    }]
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        txt = res["candidates"][0]["content"]["parts"][0]["text"].strip()
        if txt.startswith("```json"):
            txt = txt[7:]
        if txt.startswith("```"):
            txt = txt[3:]
        if txt.endswith("```"):
            txt = txt[:-3]
        txt = txt.strip()
        with open("temp/how_to_fisch/aligned_words_v13.json", "w", encoding="utf-8") as out_f:
            out_f.write(txt)
        print("Alignment saved successfully to temp/how_to_fisch/aligned_words_v13.json!")
except Exception as e:
    print("Error:", e)
