import subprocess
import os

EVENTS = [
    ("shared/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Hook alert
    ("shared/sfx/whoosh.mp3", 1300, 0.45),              # t=1.30s: Cut from avatar to gameplay
    ("shared/sfx/pop.mp3", 2800, 0.60),                 # t=2.80s: Tongue pop
    ("shared/sfx/whoosh.mp3", 5400, 0.40),              # t=5.40s: Bridge stretch whoosh
    ("shared/sfx/ding.mp3", 7900, 0.75),                # t=7.90s: Speed gym reach ding
    ("shared/sfx/bass_drop.mp3", 10400, 0.70),          # t=10.40s: Crushing laser walls bass drop
    ("shared/sfx/hitmarker.mp3", 12200, 0.65),          # t=12.20s: Final stage clear hitmarker
    ("shared/sfx/punch.mp3", 14200, 0.80),              # t=14.20s: Flex punch
    ("shared/sfx/vine_boom.mp3", 15600, 0.85),          # t=15.60s: Endcard slam!
    ("shared/sfx/ding.mp3", 17500, 0.70),               # t=17.50s: Link in bio chime
]

def build_sfx():
    os.makedirs("temp/tongue_escape", exist_ok=True)
    out_sfx = "temp/tongue_escape/sfx_track_v15.wav"
    duration = 19.50
    
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
