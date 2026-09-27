import subprocess
import os

EVENTS = [
    ("shared/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Hook alert
    ("shared/sfx/whoosh.mp3", 1200, 0.45),              # t=1.20s: Fastest way
    ("shared/sfx/vine_boom.mp3", 2800, 0.60),           # t=2.80s: Starting ball
    ("shared/sfx/pop.mp3", 5300, 0.65),                 # t=5.30s: Secret trick
    ("shared/sfx/ding.mp3", 8700, 0.75),                # t=8.70s: Hatch rare eggs
    ("shared/sfx/whoosh.mp3", 10500, 0.40),             # t=10.50s: Cash multipliers
    ("shared/sfx/ding.mp3", 12000, 0.75),               # t=12.00s: Speed gym treadmills
    ("shared/sfx/bass_drop.mp3", 15000, 0.70),          # t=15.00s: Rebirth machine
    ("shared/sfx/whoosh.mp3", 17500, 0.40),             # t=17.50s: Massive boulder
    ("shared/sfx/hitmarker.mp3", 19500, 0.65),          # t=19.50s: Finish line
    ("shared/sfx/vine_boom.mp3", 20800, 0.85),          # t=20.80s: Living Endcard slam
    ("shared/sfx/ding.mp3", 23200, 0.70),               # t=23.20s: Map code on screen chime
]

def build_sfx():
    os.makedirs("temp/money_roll", exist_ok=True)
    out_sfx = "temp/money_roll/sfx_track_v02.wav"
    duration = 24.80
    
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
