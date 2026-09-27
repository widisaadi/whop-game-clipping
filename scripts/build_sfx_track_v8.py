import subprocess
import os

def build_sfx_track(duration=34.39):
    os.makedirs("temp", exist_ok=True)
    out_sfx = "temp/sfx_track_v8.wav"
    
    # List of (file, delay_ms, volume)
    # Total duration = 34.39s
    events = [
        ("shared/sfx/metal_gear_alert.mp3", 0, 0.90),    # t=0.00s: Metal Gear Alert on INTRO.mp4 hook
        ("shared/sfx/whoosh.mp3", 4200, 0.50),           # t=4.20s: Transition to dock clip
        ("shared/sfx/pop.mp3", 4400, 0.65),              # t=4.40s: Spring Intro Badge pop-in
        ("shared/sfx/whoosh.mp3", 6800, 0.45),           # t=6.80s: Reeling floppy shrimp
        ("shared/sfx/vine_boom.mp3", 9800, 0.85),        # t=9.80s: Water boils & Spider Crab emerges
        ("shared/sfx/whoosh.mp3", 16200, 0.45),          # t=16.20s: Transition to upgrading gear
        ("shared/sfx/pop.mp3", 19100, 0.65),             # t=19.10s: Heavy shotgun inventory reveals
        ("shared/sfx/punch.mp3", 22000, 0.85),           # t=22.00s: Melee strike on beast
        ("shared/sfx/hitmarker.mp3", 22050, 0.70),       # t=22.05s: Hitmarker impact
        ("shared/sfx/gunshot.mp3", 24000, 0.85),         # t=24.00s: Gunshot volley vs colossal boss
        ("shared/sfx/vine_boom.mp3", 28800, 0.90),       # t=28.80s: 3D Endcard slam
        ("shared/sfx/ding.mp3", 32800, 0.75),            # t=32.80s: CTA ding
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
    
    print(f"Generating sfx_track_v8.wav (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("Error creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track()
