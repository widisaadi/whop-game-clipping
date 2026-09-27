import subprocess
import os

def build_sfx_track(duration=29.10):
    os.makedirs("temp", exist_ok=True)
    out_sfx = "temp/sfx_track_v7.wav"
    
    # List of (file, delay_ms, volume)
    # Total duration = 29.10s
    events = [
        ("shared/sfx/metal_gear_alert.mp3", 0, 0.90),   # Right at t=0s on INTRO.mp4!
        ("shared/sfx/whoosh.mp3", 3000, 0.45),          # Cut from INTRO to Island 1
        ("shared/sfx/pop.mp3", 3200, 0.70),             # Spring Intro Badge pop-in
        ("shared/sfx/whoosh.mp3", 8400, 0.45),          # Motorboat acceleration
        ("shared/sfx/pop.mp3", 13300, 0.60),            # Gold Rod & Burrito Bait pop
        ("shared/sfx/punch.mp3", 16400, 0.80),          # Mutant beast strike
        ("shared/sfx/hitmarker.mp3", 16400, 0.85),
        ("shared/sfx/gunshot.mp3", 22000, 0.85),        # Pike Boss gunshot blast
        ("shared/sfx/vine_boom.mp3", 24800, 0.90),      # 3D Endcard slam
        ("shared/sfx/ding.mp3", 27500, 0.70),           # CTA "Play right now" ding
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
    
    print(f"Generating sfx_track_v7.wav (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("Error creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track()
