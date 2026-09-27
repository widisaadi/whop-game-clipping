import subprocess
import os

def build_sfx_track(duration=40.73):
    os.makedirs("temp", exist_ok=True)
    out_sfx = "temp/sfx_track_v9.wav"
    
    # List of (file, delay_ms, volume)
    # Total duration = 40.73s
    events = [
        ("shared/sfx/metal_gear_alert.mp3", 0, 0.90),    # t=0.00s: Metal Gear Alert on INTRO.mp4 hook
        ("shared/sfx/whoosh.mp3", 5000, 0.50),           # t=5.00s: Transition to dock clip
        ("shared/sfx/pop.mp3", 5200, 0.65),              # t=5.20s: Spring Intro Badge pop-in
        ("shared/sfx/whoosh.mp3", 8400, 0.45),           # t=8.40s: Reeling on peaceful pier
        ("shared/sfx/vine_boom.mp3", 12800, 0.85),       # t=12.80s: Mutant sea beast surfaces
        ("shared/sfx/punch.mp3", 18000, 0.80),           # t=18.00s: Switching to weapons & melee combat
        ("shared/sfx/hitmarker.mp3", 18050, 0.70),       # t=18.05s: Hitmarker impact
        ("shared/sfx/whoosh.mp3", 22400, 0.45),          # t=22.40s: Weapon rack upgrade shop
        ("shared/sfx/pop.mp3", 22600, 0.60),             # t=22.60s: Weapon unlock pop
        ("shared/sfx/whoosh.mp3", 26800, 0.50),          # t=26.80s: Speedboat ocean cruising
        ("shared/sfx/gunshot.mp3", 31000, 0.85),         # t=31.00s: Full FPS shootout vs colossal boss
        ("shared/sfx/vine_boom.mp3", 36000, 0.90),       # t=36.00s: 3D Endcard slam
        ("shared/sfx/ding.mp3", 39400, 0.75),            # t=39.40s: CTA ding
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
    
    print(f"Generating sfx_track_v9.wav (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("ERROR creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track()
