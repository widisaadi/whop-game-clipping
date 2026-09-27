import subprocess
import os

def build_sfx_track(duration=25.56):
    os.makedirs("temp/tongue_escape", exist_ok=True)
    out_sfx = "temp/tongue_escape/sfx_track_fast.wav"
    
    events = [
        ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),     # t=0.00s: Metal Gear Alert hook
        ("assets/sfx/whoosh.mp3", 1500, 0.60),            # t=1.50s: Tongue bridge shoot
        ("assets/sfx/ding.mp3", 2900, 0.70),              # t=2.90s: +1 Tongue Escape title badge
        ("assets/sfx/pop.mp3", 6000, 0.60),               # t=6.00s: Gym treadmills
        ("assets/sfx/ding.mp3", 8500, 0.75),              # t=8.50s: Level up & studs increase
        ("assets/sfx/bass_drop.mp3", 10000, 0.80),        # t=10.00s: Hacker x99 treadmill
        ("assets/sfx/whoosh.mp3", 12300, 0.65),           # t=12.30s: Sky vertical jump
        ("assets/sfx/punch.mp3", 15000, 0.85),            # t=15.00s: Stage 7 landing
        ("assets/sfx/hitmarker.mp3", 15050, 0.75),        # t=15.05s: +100 Wins chime
        ("assets/sfx/pop.mp3", 18000, 0.65),              # t=18.00s: Elemental trails shop
        ("assets/sfx/whoosh.mp3", 21000, 0.70),           # t=21.00s: Stage 8 jump
        ("assets/sfx/vine_boom.mp3", 22000, 0.85),        # t=22.00s: Endcard slam
        ("assets/sfx/ding.mp3", 23800, 0.75),             # t=23.80s: Link in bio chime
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
    
    print(f"Generating sfx_track_fast.wav (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("ERROR creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track(duration=25.56)
