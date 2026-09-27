import subprocess
import os

def build_sfx_track(total_dur=23.88):
    os.makedirs("temp/how_to_fisch", exist_ok=True)
    out_wav = "temp/how_to_fisch/sfx_track_htf_v12.wav"

    sfx_events = [
        ("assets/sfx/metal_gear_alert.mp3", 0.05, 0.85),
        ("assets/sfx/whoosh.mp3", 2.55, 0.65),
        ("assets/sfx/pop.mp3", 2.65, 0.70),
        ("assets/sfx/bass_drop.mp3", 5.50, 0.90),
        ("assets/sfx/whoosh.mp3", 8.55, 0.60),
        ("assets/sfx/ding.mp3", 8.70, 0.80),
        ("assets/sfx/gunshot.mp3", 11.75, 0.80),
        ("assets/sfx/hitmarker.mp3", 12.05, 0.70),
        ("assets/sfx/whoosh.mp3", 14.00, 0.65),
        ("assets/sfx/vine_boom.mp3", 16.10, 0.85),
        ("assets/sfx/whoosh.mp3", 18.25, 0.65),
        ("assets/sfx/ding.mp3", 18.35, 0.85),
    ]

    # Build ffmpeg amix complex filter
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

    print(f"Building synchronous SFX track for How to Fisch v12 ({total_dur:.2f}s)...")
    subprocess.run(cmd, check=True)
    print(f"SFX track saved to {out_wav}")

if __name__ == "__main__":
    build_sfx_track()
