import subprocess
import os

EVENTS = [
    ("shared/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Hook opener
    ("shared/sfx/whoosh.mp3", 2060, 0.50),              # t=2.06s: Roblox game pop-in
    ("shared/sfx/pop.mp3", 3400, 0.60),                 # t=3.40s: Escape the island cut
    ("shared/sfx/punch.mp3", 5460, 0.70),               # t=5.46s: Own tongue grapple
    ("shared/sfx/ding.mp3", 7680, 0.75),                # t=7.68s: Gym treadmill training
    ("shared/sfx/whoosh.mp3", 10000, 0.50),             # t=10.00s: Lava gap swing
    ("shared/sfx/ding.mp3", 11820, 0.75),               # t=11.82s: Unlock weirder tongues
    ("shared/sfx/vine_boom.mp3", 14600, 0.85),          # t=14.60s: Tongue that lets you FLY
    ("shared/sfx/whoosh.mp3", 17280, 0.60),             # t=17.28s: Official game card reveal
    ("shared/sfx/pop.mp3", 19940, 0.65),                # t=19.94s: Codes menu modal
    ("shared/sfx/hitmarker.mp3", 21560, 0.70),          # t=21.56s: Type BONUS500
    ("shared/sfx/ding.mp3", 22720, 0.85),               # t=22.72s: Claim +10,000 free tongue!
]

def build_sfx():
    os.makedirs("temp/tongue_escape", exist_ok=True)
    out_sfx = "temp/tongue_escape/sfx_track_v17.wav"
    duration = 23.58
    
    inputs = []
    filter_parts = []
    
    for idx, (path, delay_ms, vol) in enumerate(EVENTS):
        inputs.extend(["-i", path])
        filter_parts.append(f"[{idx}:a]adelay={delay_ms}|{delay_ms},volume={vol:.2f},aresample=48000[a{idx}];")
    
    mix_inputs = "".join(f"[a{idx}]" for idx in range(len(EVENTS)))
    filter_parts.append(f"{mix_inputs}amix=inputs={len(EVENTS)}:duration=longest:normalize=0[aout]")
    
    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", "".join(filter_parts),
        "-map", "[aout]",
        "-t", f"{duration:.2f}",
        "-ar", "48000",
        "-ac", "2",
        out_sfx
    ]
    
    print(f"Generating {out_sfx} (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("Error creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"--> Generated {out_sfx} ({os.path.getsize(out_sfx)} bytes)")
    return True

if __name__ == "__main__":
    build_sfx()
