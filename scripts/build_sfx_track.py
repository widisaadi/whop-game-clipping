import subprocess
import os

def build_sfx_track():
    os.makedirs("temp", exist_ok=True)
    out_sfx = "temp/sfx_track.wav"
    
    # List of (file, delay_ms, volume)
    events = [
        ("assets/sfx/whoosh.mp3", 0, 0.35),
        ("assets/sfx/whoosh.mp3", 4400, 0.45),
        ("assets/sfx/pop.mp3", 4550, 0.70),
        ("assets/sfx/whoosh.mp3", 5800, 0.40),
        ("assets/sfx/pop.mp3", 13000, 0.50),
        ("assets/sfx/pop.mp3", 18200, 0.55),
        ("assets/sfx/punch.mp3", 20650, 0.75),
        ("assets/sfx/hitmarker.mp3", 20650, 0.80),
        ("assets/sfx/hitmarker.mp3", 22350, 0.80),
        ("assets/sfx/gunshot.mp3", 26050, 0.75),
        ("assets/sfx/vine_boom.mp3", 28500, 0.90),
        ("assets/sfx/ding.mp3", 32320, 0.60),
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
        "-t", "33.76",
        "-ar", "48000",
        "-ac", "2",
        out_sfx
    ]
    
    print("Generating sfx_track.wav...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("Error creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track()
