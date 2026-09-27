import subprocess
import os

def build_sfx_track(duration=44.24):
    os.makedirs("temp/tongue_escape", exist_ok=True)
    out_sfx = "temp/tongue_escape/sfx_track.wav"
    
    events = [
        ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),     # t=0.00s: Metal Gear Alert hook
        ("assets/sfx/whoosh.mp3", 2500, 0.60),            # t=2.50s: Giant tongue shoot
        ("assets/sfx/ding.mp3", 6500, 0.70),              # t=6.50s: Title badge
        ("assets/sfx/whoosh.mp3", 8500, 0.50),            # t=8.50s: Tongue bridge slide
        ("assets/sfx/pop.mp3", 13500, 0.60),              # t=13.50s: Treadmill gym enter
        ("assets/sfx/ding.mp3", 16700, 0.75),             # t=16.70s: Level up & studs increase
        ("assets/sfx/bass_drop.mp3", 21000, 0.80),        # t=21.00s: Hacker x99 treadmill
        ("assets/sfx/whoosh.mp3", 23500, 0.65),           # t=23.50s: Sky vertical jump
        ("assets/sfx/punch.mp3", 29500, 0.85),            # t=29.50s: Stage 7 landing
        ("assets/sfx/hitmarker.mp3", 29550, 0.75),        # t=29.55s: +100 Wins chime
        ("assets/sfx/pop.mp3", 33800, 0.65),              # t=33.80s: Elemental trails
        ("assets/sfx/vine_boom.mp3", 39500, 0.85),        # t=39.50s: Endcard slam
        ("assets/sfx/ding.mp3", 42000, 0.75),             # t=42.00s: Play CTA chime
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
    
    print(f"Generating sfx_track.wav (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("ERROR creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track()
