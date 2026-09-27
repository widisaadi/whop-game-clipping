import subprocess
import os

EVENTS = [
    ("shared/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Hook alert
    ("shared/sfx/whoosh.mp3", 1500, 0.45),              # t=1.50s: Cut to gameplay
    ("shared/sfx/vine_boom.mp3", 2800, 0.60),           # t=2.80s: Fail this jump!
    ("shared/sfx/bass_drop.mp3", 6200, 0.70),           # t=6.20s: Straight into the lava!
    ("shared/sfx/ding.mp3", 8500, 0.75),                # t=8.50s: Speed gym treadmills
    ("shared/sfx/whoosh.mp3", 10500, 0.40),             # t=10.50s: Multipliers stack
    ("shared/sfx/pop.mp3", 12000, 0.65),                # t=12.00s: Spitting tongue pop
    ("shared/sfx/hitmarker.mp3", 14800, 0.65),          # t=14.80s: Crushing laser walls
    ("shared/sfx/punch.mp3", 16200, 0.80),              # t=16.20s: Conquer Stage 8
    ("shared/sfx/vine_boom.mp3", 18000, 0.85),          # t=18.00s: Living Endcard slam
    ("shared/sfx/ding.mp3", 20300, 0.70),               # t=20.30s: Link in bio chime
]

def build_sfx():
    os.makedirs("temp/tongue_escape", exist_ok=True)
    out_sfx = "temp/tongue_escape/sfx_track_v16.wav"
    duration = 22.00
    
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
