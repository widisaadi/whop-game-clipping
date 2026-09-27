import subprocess
import os

def build_sfx_track(duration=23.30):
    os.makedirs("temp/tongue_escape", exist_ok=True)
    out_sfx = "temp/tongue_escape/sfx_track_v11.wav"
    
    events = [
        ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Avatar intro opener
        ("assets/sfx/punch.mp3", 1400, 0.80),               # t=1.40s: Stage 8 lava pit slam
        ("assets/sfx/whoosh.mp3", 3800, 0.70),              # t=3.80s: Lava near miss
        ("assets/sfx/pop.mp3", 5200, 0.65),                 # t=5.20s: Gym transition
        ("assets/sfx/ding.mp3", 7200, 0.75),                # t=7.20s: Treadmill stud jump
        ("assets/sfx/bass_drop.mp3", 8800, 0.80),           # t=8.80s: 40,000 studs peak
        ("assets/sfx/whoosh.mp3", 9800, 0.75),              # t=9.80s: Massive tongue shoot
        ("assets/sfx/hitmarker.mp3", 12500, 0.75),          # t=12.50s: Rocket slide past arrows
        ("assets/sfx/ding.mp3", 14200, 0.80),               # t=14.20s: Landing on finish platform
        ("assets/sfx/pop.mp3", 15300, 0.70),                # t=15.30s: Roblox breakdowns flex
        ("assets/sfx/ding.mp3", 17200, 0.85),               # t=17.20s: Smash that like chime!
        ("assets/sfx/vine_boom.mp3", 19000, 0.85),          # t=19.00s: Living Endcard slam
        ("assets/sfx/ding.mp3", 21200, 0.75),               # t=21.20s: Link in bio chime
    ]
    
    inputs = []
    filter_parts = []
    
    for idx, (path, delay_ms, vol) in enumerate(events):
        inputs.extend(["-i", path])
        filter_parts.append(f"[{idx}:a]adelay={delay_ms}|{delay_ms},volume={vol:.2f},aresample=48000[a{idx}];")
    
    mix_inputs = "".join(f"[a{idx}]" for idx in range(len(events)))
    filter_parts.append(f"{mix_inputs}amix=inputs={len(events)}:duration=longest:normalize=0[aout]")
    
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
    
    print(f"Generating sfx_track_v11.wav (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("ERROR creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track(duration=23.30)
