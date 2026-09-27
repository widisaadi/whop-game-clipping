import subprocess
import os

def build_sfx_track(duration=23.50):
    os.makedirs("temp/tongue_escape", exist_ok=True)
    out_sfx = "temp/tongue_escape/sfx_track_v05.wav"
    
    # List of (file, delay_ms, volume)
    # Total duration = 23.50s
    events = [
        ("shared/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Hook alert
        ("shared/sfx/whoosh.mp3", 1300, 0.45),              # t=1.30s: Cut from avatar to gameplay
        ("shared/sfx/vine_boom.mp3", 1800, 0.65),           # t=1.80s: "Completely wrong!" emphasis
        ("shared/sfx/whoosh.mp3", 2800, 0.40),              # t=2.80s: Electric treadmill cut
        ("shared/sfx/pop.mp3", 4200, 0.55),                 # t=4.20s: Training tongue studs
        ("shared/sfx/bass_drop.mp3", 5800, 0.70),          # t=5.80s: Rainbow treadmill surge
        ("shared/sfx/ding.mp3", 7500, 0.75),                # t=7.50s: Shop open / Wins stack
        ("shared/sfx/ding.mp3", 9400, 0.80),                # t=9.40s: Fire trail unlock
        ("shared/sfx/ding.mp3", 11600, 0.80),               # t=11.60s: Lightning / Ruby trail
        ("shared/sfx/whoosh.mp3", 13800, 0.60),             # t=13.80s: Canyon launch whoosh
        ("shared/sfx/punch.mp3", 16800, 0.80),              # t=16.80s: Stage 7 slam impact
        ("shared/sfx/hitmarker.mp3", 17200, 0.65),          # t=17.20s: 100 Wins collected
        ("shared/sfx/vine_boom.mp3", 19600, 0.85),          # t=19.60s: Endcard slam!
        ("shared/sfx/ding.mp3", 21300, 0.70),               # t=21.30s: Link in bio chime
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
    
    print(f"Generating sfx_track_v05.wav (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("Error creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track()
