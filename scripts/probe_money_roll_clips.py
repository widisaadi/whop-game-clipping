import subprocess
import os
import json

clips_dir = "campaigns/money_roll/assets/clips"
clips = sorted(os.listdir(clips_dir))

catalog = []
print(f"Probing {len(clips)} downloaded clips...")

for c in clips:
    path = os.path.join(clips_dir, c)
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,duration,r_frame_rate",
        "-of", "json",
        path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        info = json.loads(res.stdout)
        stream = info.get("streams", [{}])[0]
        w = stream.get("width")
        h = stream.get("height")
        dur = float(stream.get("duration", 0))
        catalog.append({"file": c, "width": w, "height": h, "duration": dur})
        print(f"- {c}: {w}x{h}, {dur:.2f}s")
    else:
        print(f"- {c}: probe error")

out_catalog = "campaigns/money_roll/guide/footage_catalog.json"
with open(out_catalog, "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2)

print(f"\nSaved footage catalog with {len(catalog)} clips to {out_catalog}")
