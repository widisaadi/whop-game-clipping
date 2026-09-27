import subprocess
import os

EVENTS = [
    ("shared/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Hook alert
    ("shared/sfx/whoosh.mp3", 1300, 0.45),              # t=1.30s: Cut from avatar to gameplay
    ("shared/sfx/vine_boom.mp3", 4100, 0.60),           # t=4.10s: Banned!
    ("shared/sfx/bass_drop.mp3", 7300, 0.70),           # t=7.30s: Fall into void
    ("shared/sfx/pop.mp3", 10000, 0.65),                # t=10.00s: Spit tongue pop
    ("shared/sfx/whoosh.mp3", 12000, 0.40),             # t=12.00s: Massive bridge stretch
    ("shared/sfx/ding.mp3", 14500, 0.75),               # t=14.50s: Speed gym multipliers
    ("shared/sfx/hitmarker.mp3", 17200, 0.65),          # t=17.20s: Dodge crushers
    ("shared/sfx/punch.mp3", 20800, 0.80),              # t=20.80s: Stage 8 flex
    ("shared/sfx/vine_boom.mp3", 22200, 0.85),          # t=22.20s: Living Endcard slam
    ("shared/sfx/ding.mp3", 24800, 0.70),               # t=24.80s: Link in bio chime
]

def build_sfx():
    os.makedirs("temp/tongue_escape", exist_ok=True)
    out_sfx = "temp/tongue_escape/sfx_track_v15_remake.wav"
    duration = 26.80
    
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
