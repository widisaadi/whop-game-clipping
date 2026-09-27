import subprocess
import os

def build_sfx_track(duration=31.74):
    os.makedirs("temp", exist_ok=True)
    out_sfx = "temp/sfx_track_v5.wav"
    
    # List of (file, delay_ms, volume)
    # Precisely timed to the tightened voiceover (31.74s total)
    events = [
        ("assets/sfx/whoosh.mp3", 0, 0.35),       # Initial hook whoosh
        ("assets/sfx/whoosh.mp3", 3900, 0.45),    # Intro badge entrance
        ("assets/sfx/pop.mp3", 4140, 0.70),       # Intro badge bounce pop
        ("assets/sfx/whoosh.mp3", 5500, 0.40),    # Transition to cast rod
        ("assets/sfx/pop.mp3", 12500, 0.50),      # Island 2 reveal pop
        ("assets/sfx/pop.mp3", 16880, 0.55),      # Burrito bait pop
        ("assets/sfx/punch.mp3", 19700, 0.80),    # Mutant lobster brass knuckle punch
        ("assets/sfx/hitmarker.mp3", 19700, 0.85),
        ("assets/sfx/hitmarker.mp3", 21300, 0.85), # Mutant crab crowbar strike
        ("assets/sfx/gunshot.mp3", 24900, 0.80),   # Pike fish boss gunshot blast
        ("assets/sfx/vine_boom.mp3", 27000, 0.90), # Living blurred endcard slam
        ("assets/sfx/ding.mp3", 30600, 0.65),     # "Play right now" CTA ding
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
    
    print("Generating sfx_track_v5.wav...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("Error creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track()
