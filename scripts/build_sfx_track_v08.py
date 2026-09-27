import subprocess
import os

def build_sfx_track(duration=18.00):
    os.makedirs("temp/tongue_escape", exist_ok=True)
    out_sfx = "temp/tongue_escape/sfx_track_v08.wav"
    
    events = [
        ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Metal Gear Alert hook
        ("assets/sfx/whoosh.mp3", 1250, 0.60),              # t=1.25s: Tongue spit launch
        ("assets/sfx/ding.mp3", 3750, 0.70),                # t=3.75s: Gym treadmill level-up chime
        ("assets/sfx/whoosh.mp3", 6250, 0.60),              # t=6.25s: Canyon bridge glide
        ("assets/sfx/pop.mp3", 8250, 0.65),                 # t=8.25s: Window obstacle pass
        ("assets/sfx/whoosh.mp3", 10750, 0.60),             # t=10.75s: Narrow canyon slide
        ("assets/sfx/hitmarker.mp3", 12250, 0.75),          # t=12.25s: Stage 7 +100 Wins
        ("assets/sfx/vine_boom.mp3", 14100, 0.85),          # t=14.10s: Living Endcard slam
        ("assets/sfx/ding.mp3", 16000, 0.75),               # t=16.00s: Link in bio chime
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
    
    print(f"Generating sfx_track_v08.wav (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("ERROR creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track(duration=18.00)
