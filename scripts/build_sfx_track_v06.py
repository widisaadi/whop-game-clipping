import subprocess
import os

def build_sfx_track(duration=19.90):
    os.makedirs("temp/tongue_escape", exist_ok=True)
    out_sfx = "temp/tongue_escape/sfx_track_v06.wav"
    
    # Total duration = 19.90s
    events = [
        ("shared/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Hook alert
        ("shared/sfx/whoosh.mp3", 1300, 0.45),              # t=1.30s: Cut from avatar to gameplay
        ("shared/sfx/pop.mp3", 2800, 0.60),                 # t=2.80s: Spit giant tongue pop
        ("shared/sfx/whoosh.mp3", 5600, 0.40),              # t=5.60s: Bridge crossing whoosh
        ("shared/sfx/ding.mp3", 8000, 0.75),                # t=8.00s: 40,000 studs / Level 56 ding
        ("shared/sfx/bass_drop.mp3", 10500, 0.70),          # t=10.50s: Lava obstacles bass drop
        ("shared/sfx/hitmarker.mp3", 12300, 0.65),          # t=12.30s: Stage 7 splash hitmarker
        ("shared/sfx/punch.mp3", 14300, 0.80),              # t=14.30s: Leaderboards flex punch
        ("shared/sfx/vine_boom.mp3", 16000, 0.85),          # t=16.00s: Endcard slam!
        ("shared/sfx/ding.mp3", 18000, 0.70),               # t=18.00s: Link in bio chime
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
    
    print(f"Generating sfx_track_v06.wav (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("Error creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track()
