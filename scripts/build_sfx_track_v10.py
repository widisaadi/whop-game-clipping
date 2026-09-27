import subprocess
import os

def build_sfx_track(duration=24.50):
    os.makedirs("temp/tongue_escape", exist_ok=True)
    out_sfx = "temp/tongue_escape/sfx_track_v10.wav"
    
    events = [
        ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Metal Gear Alert hook
        ("assets/sfx/punch.mp3", 1200, 0.80),               # t=1.20s: Crushing walls slam
        ("assets/sfx/whoosh.mp3", 2800, 0.70),              # t=2.80s: Near-miss lava dive
        ("assets/sfx/pop.mp3", 4200, 0.65),                 # t=4.20s: Gym transition
        ("assets/sfx/ding.mp3", 6200, 0.80),                # t=6.20s: Rainbow x30 tongue unlock
        ("assets/sfx/whoosh.mp3", 8000, 0.75),              # t=8.00s: Lightning bridge shoot
        ("assets/sfx/hitmarker.mp3", 9800, 0.75),           # t=9.80s: Through the closing walls
        ("assets/sfx/whoosh.mp3", 11200, 0.70),             # t=11.20s: POV supersonic slide
        ("assets/sfx/bass_drop.mp3", 13000, 0.80),          # t=13.00s: Giant arrow canyon
        ("assets/sfx/ding.mp3", 15000, 0.80),               # t=15.00s: Stage 7 landing +100 wins
        ("assets/sfx/pop.mp3", 17000, 0.70),                # t=17.00s: Bonus wins pop
        ("assets/sfx/ding.mp3", 18200, 0.75),               # t=18.20s: Golden halo dance flex
        ("assets/sfx/vine_boom.mp3", 20300, 0.85),          # t=20.30s: Living Endcard slam
        ("assets/sfx/ding.mp3", 22400, 0.75),               # t=22.40s: Link in bio chime
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
    
    print(f"Generating sfx_track_v10.wav (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("ERROR creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track(duration=24.50)
