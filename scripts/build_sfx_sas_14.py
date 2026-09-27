import os
import subprocess

sfx_dir = "assets/sfx"
out_sfx = "temp/steal_a_seed/sfx_track_14.wav"
os.makedirs(os.path.dirname(out_sfx), exist_ok=True)

# List of SFX events: (file, timestamp_in_sec, volume)
events = [
    ("metal_gear_alert.mp3", 0.05, 0.90),
    ("whoosh.mp3", 1.35, 0.85),
    ("bass_drop.mp3", 1.45, 0.80),
    ("vine_boom.mp3", 4.80, 0.90),
    ("metal_pipe.mp3", 6.70, 0.70), # monster chase
    ("pop.mp3", 9.80, 0.85),
    ("ding.mp3", 10.60, 0.80),
    ("bass_drop.mp3", 13.60, 0.85),
    ("hitmarker.mp3", 16.50, 0.90),
    ("ding.mp3", 16.80, 0.85), # Steal successful
    ("pop.mp3", 18.90, 0.85),
    ("ding.mp3", 20.40, 0.85), # printing 50,000 cash
    ("whoosh.mp3", 22.90, 0.90) # living endcard
]

filter_parts = []
inputs = []
for idx, (fname, t, vol) in enumerate(events):
    fpath = os.path.join(sfx_dir, fname)
    inputs.extend(["-i", fpath])
    delay_ms = int(t * 1000)
    filter_parts.append(f"[{idx}:a]adelay={delay_ms}|{delay_ms},volume={vol:.2f}[sfx_{idx}];")

mix_inputs = "".join(f"[sfx_{idx}]" for idx in range(len(events)))
filter_graph = "".join(filter_parts) + f"{mix_inputs}amix=inputs={len(events)}:duration=longest:dropout_transition=2[out]"

cmd = ["ffmpeg", "-y"] + inputs + [
    "-filter_complex", filter_graph,
    "-map", "[out]",
    "-c:a", "pcm_s16le",
    "-ar", "48000",
    "-ac", "2",
    "-t", "25.25",
    out_sfx
]

subprocess.run(cmd, check=True)
print(f"Generated precision SFX track: {out_sfx}")
