import subprocess
import os

def build_sfx_track(total_dur=19.60):
    os.makedirs("temp/how_to_fisch", exist_ok=True)
    out_wav = "temp/how_to_fisch/sfx_track_htf_v13.wav"

    sfx_events = [
        # Beat 1: Hook (0.00s - 2.85s)
        ("assets/sfx/metal_gear_alert.mp3", 0.05, 0.85),
        ("assets/sfx/pop.mp3", 1.25, 0.70),

        # Beat 2: Core Constraint / Rod Cast (2.85s - 5.45s)
        ("assets/sfx/whoosh.mp3", 2.80, 0.65),
        ("assets/sfx/ding.mp3", 2.95, 0.75),

        # Beat 3: Monster Attack (5.45s - 8.55s)
        ("assets/sfx/bass_drop.mp3", 5.40, 0.90),
        ("assets/sfx/vine_boom.mp3", 5.50, 0.85),
        ("assets/sfx/hitmarker.mp3", 7.05, 0.80),

        # Beat 4A: Upgrading Gear at Granny (8.55s - 11.35s)
        ("assets/sfx/whoosh.mp3", 8.50, 0.65),
        ("assets/sfx/pop.mp3", 8.65, 0.70),

        # Beat 4B: Iron Sights Boss Shootout (11.35s - 13.85s)
        ("assets/sfx/whoosh.mp3", 11.30, 0.65),
        ("assets/sfx/gunshot.mp3", 11.45, 0.85),
        ("assets/sfx/hitmarker.mp3", 11.90, 0.75),

        # Beat 5: Motorboat Ocean Titan (13.85s - 15.70s)
        ("assets/sfx/whoosh.mp3", 13.80, 0.65),
        ("assets/sfx/bass_drop.mp3", 13.95, 0.80),

        # Beat 6: Living Endcard CTA (15.70s - 19.60s)
        ("assets/sfx/whoosh.mp3", 15.65, 0.65),
        ("assets/sfx/ding.mp3", 15.75, 0.85),
    ]

    inputs = ["-f", "lavfi", "-t", f"{total_dur:.2f}", "-i", "anullsrc=r=48000:cl=stereo"]
    filter_parts = []
    mix_labels = ["[0:a]"]

    for idx, (path, start_t, vol) in enumerate(sfx_events, start=1):
        inputs.extend(["-i", path])
        delay_ms = int(start_t * 1000)
        filter_parts.append(f"[{idx}:a]adelay={delay_ms}|{delay_ms},volume={vol:.2f}[sfx_{idx}];")
        mix_labels.append(f"[sfx_{idx}]")

    filter_complex = "".join(filter_parts) + "".join(mix_labels) + f"amix=inputs={len(sfx_events)+1}:duration=first:dropout_transition=2[aout]"

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[aout]",
        "-t", f"{total_dur:.2f}",
        out_wav
    ]

    print(f"Building clean SFX track for How to Fisch Video 13 ({total_dur:.2f}s)...")
    subprocess.run(cmd, check=True)
    print(f"SFX track saved to {out_wav}")

if __name__ == "__main__":
    build_sfx_track()
