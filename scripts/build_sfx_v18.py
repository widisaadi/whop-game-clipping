import subprocess
import os

EVENTS = [
    ("shared/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Hook opener
    ("shared/sfx/whoosh.mp3", 1680, 0.50),              # t=1.68s: Cut to gameplay
    ("shared/sfx/pop.mp3", 3040, 0.60),                 # t=3.04s: Trapped on island
    ("shared/sfx/bass_drop.mp3", 5380, 0.65),           # t=5.38s: Jumping completely banned!
    ("shared/sfx/punch.mp3", 6440, 0.70),               # t=6.44s: Spitting tongue grapple
    ("shared/sfx/ding.mp3", 8740, 0.75),                # t=8.74s: Speed gym treadmills
    ("shared/sfx/whoosh.mp3", 10140, 0.50),             # t=10.14s: Massive multipliers
    ("shared/sfx/pop.mp3", 13160, 0.60),                # t=13.16s: Bridge giant gaps
    ("shared/sfx/hitmarker.mp3", 15660, 0.70),          # t=15.66s: Laser walls & lava
    ("shared/sfx/vine_boom.mp3", 18380, 0.85),          # t=18.38s: Literally FLY across map
    ("shared/sfx/whoosh.mp3", 20520, 0.60),             # t=20.52s: Living Endcard slam
    ("shared/sfx/ding.mp3", 22600, 0.80),               # t=22.60s: Link is in my bio chime
]

def build_sfx():
    os.makedirs("temp/tongue_escape", exist_ok=True)
    out_sfx = "temp/tongue_escape/sfx_track_v18.wav"
    duration = 23.73
    
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
