import subprocess
import os

def build_sfx_track(duration=18.40):
    os.makedirs("temp/tongue_escape", exist_ok=True)
    out_sfx = "temp/tongue_escape/sfx_track_v07.wav"
    
    events = [
        ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Metal Gear Alert hook
        ("assets/sfx/whoosh.mp3", 1250, 0.60),              # t=1.25s: Vertical sky tongue launch
        ("assets/sfx/ding.mp3", 3250, 0.70),                # t=3.25s: +1 Tongue Escape intro
        ("assets/sfx/bass_drop.mp3", 5500, 0.75),           # t=5.50s: Hacker x99 treadmill sparks
        ("assets/sfx/whoosh.mp3", 7500, 0.60),              # t=7.50s: Impossible gap slide
        ("assets/sfx/pop.mp3", 9500, 0.65),                 # t=9.50s: Elemental trails showcase
        ("assets/sfx/hitmarker.mp3", 11500, 0.70),          # t=11.50s: Ruby/Fire trails
        ("assets/sfx/punch.mp3", 12800, 0.80),              # t=12.80s: Stage 8 challenge
        ("assets/sfx/vine_boom.mp3", 14500, 0.85),          # t=14.50s: Living Endcard slam
        ("assets/sfx/ding.mp3", 16500, 0.75),               # t=16.50s: Link in bio CTA chime
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
    
    print(f"Generating sfx_track_v07.wav (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("ERROR creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track(duration=18.40)
