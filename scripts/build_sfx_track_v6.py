import subprocess
import os

def build_sfx_track(duration=29.61):
    os.makedirs("temp", exist_ok=True)
    out_sfx = "temp/sfx_track_v6.wav"
    
    # List of (file, delay_ms, volume)
    # Total duration = 29.61s
    events = [
        ("assets/sfx/metal_gear_alert.mp3", 0, 0.90),  # Right at the very start with INTRO.mp4!
        ("assets/sfx/whoosh.mp3", 4400, 0.45),         # Transition to Island 1
        ("assets/sfx/pop.mp3", 4600, 0.70),            # Spring Intro Badge pop-in
        ("assets/sfx/pop.mp3", 12800, 0.60),           # Heavy shotguns reveal
        ("assets/sfx/pop.mp3", 14700, 0.60),           # Living bait reveal
        ("assets/sfx/punch.mp3", 17800, 0.80),         # Mutant beast brass knuckles punch
        ("assets/sfx/hitmarker.mp3", 17800, 0.85),
        ("assets/sfx/hitmarker.mp3", 20200, 0.85),     # Crowbar strike on mutant crab
        ("assets/sfx/gunshot.mp3", 22600, 0.85),       # Ocean boss shootout gunshot
        ("assets/sfx/vine_boom.mp3", 24800, 0.90),     # 3D Endcard dramatic slam
        ("assets/sfx/ding.mp3", 28400, 0.70),          # "Play right now" CTA ding
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
    
    print(f"Generating sfx_track_v6.wav (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("Error creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track()
