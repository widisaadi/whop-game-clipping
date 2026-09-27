import subprocess
import os

def build_sfx_track(duration=25.00):
    os.makedirs("temp/tongue_escape", exist_ok=True)
    out_sfx = "temp/tongue_escape/sfx_track_v09_remake.wav"
    
    events = [
        ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Metal Gear Alert hook
        ("assets/sfx/punch.mp3", 1250, 0.70),               # t=1.25s: Fail thud / revive
        ("assets/sfx/whoosh.mp3", 3250, 0.65),              # t=3.25s: Lava chasm glide
        ("assets/sfx/pop.mp3", 5450, 0.60),                 # t=5.45s: Gym treadmills enter
        ("assets/sfx/ding.mp3", 8500, 0.75),                # t=8.50s: Level up chime
        ("assets/sfx/bass_drop.mp3", 9500, 0.75),           # t=9.50s: 40,000 studs escalation
        ("assets/sfx/whoosh.mp3", 11500, 0.65),             # t=11.50s: Massive tongue shoot
        ("assets/sfx/pop.mp3", 14600, 0.65),                # t=14.60s: Honeycomb dodge
        ("assets/sfx/hitmarker.mp3", 16600, 0.75),          # t=16.60s: Stage 7 crush
        ("assets/sfx/whoosh.mp3", 18900, 0.70),             # t=18.90s: Stage 8 lava lake
        ("assets/sfx/vine_boom.mp3", 20800, 0.85),          # t=20.80s: Living Endcard slam
        ("assets/sfx/ding.mp3", 22700, 0.75),               # t=22.70s: Link in bio chime
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
    
    print(f"Generating sfx_track_v09_remake.wav (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("ERROR creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track(duration=25.00)
