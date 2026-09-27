import subprocess
import os

def build_sfx_track(duration=28.98):
    os.makedirs("temp", exist_ok=True)
    out_sfx = "temp/sfx_track_v12.wav"
    
    events = [
        ("shared/sfx/metal_gear_alert.mp3", 0, 0.90),     # t=0.00s: Metal Gear Alert on INTRO.mp4 hook
        ("shared/sfx/whoosh.mp3", 3400, 0.50),            # t=3.40s: Transition to dock
        ("shared/sfx/pop.mp3", 3600, 0.65),               # t=3.60s: Spring badge pop
        ("shared/sfx/whoosh.mp3", 7500, 0.50),            # t=7.50s: Speedboat voyage
        ("shared/sfx/pop.mp3", 11300, 0.65),              # t=11.30s: Granny shop & shotgun equip
        ("shared/sfx/punch.mp3", 14500, 0.85),            # t=14.50s: Monster hit
        ("shared/sfx/hitmarker.mp3", 14550, 0.75),        # t=14.55s: Hitmarker
        ("shared/sfx/whoosh.mp3", 18800, 0.50),           # t=18.80s: Stormy voyage
        ("shared/sfx/gunshot.mp3", 21800, 0.90),          # t=21.80s: Colossal titan shootout
        ("shared/sfx/vine_boom.mp3", 24600, 0.90),        # t=24.60s: 3D Endcard slam
        ("shared/sfx/ding.mp3", 27200, 0.75),             # t=27.20s: CTA ding
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
    
    print(f"Generating sfx_track_v12.wav (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("ERROR creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track()
