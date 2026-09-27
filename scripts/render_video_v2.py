import os
import subprocess
import sys

def run_cmd(cmd, desc):
    print(f"--> {desc}...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="ignore")
    if res.returncode != 0:
        print(f"Error in {desc}:")
        print(res.stderr[-800:])
        sys.exit(1)
    return res

def main():
    os.makedirs("temp/v2_segments", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    # 7 gameplay cuts + 1 blurred gameplay endcard cut
    segments = [
        # 1. 0.0s - 3.4s (3.4s): "Wait, why does a Roblox fishing game have guns?!"
        ("assets/25_Clip 25.mp4", 0.5, 3.4, False),
        
        # 2. 3.4s - 6.7s (3.3s): "Welcome to How to Fisch, where the fish fight back!"
        ("assets/35_Clip 35.mp4", 0.5, 3.3, False),
        
        # 3. 6.7s - 11.2s (4.5s): "You start with a basic rod, but out here you need real weapons to survive."
        ("assets/27_Clip 27.mp4", 0.5, 4.5, False),
        
        # 4a. 11.2s - 13.8s (2.6s): "You can blast mutant sea beasts on land..."
        ("assets/21_Clip 21.mp4", 0.2, 2.6, False),
        
        # 4b. 13.8s - 16.5s (2.7s): "...craft special burrito bait, and upgrade your gear."
        ("assets/26_Clip 26.mp4", 1.0, 2.7, False),
        
        # 5. 16.5s - 20.8s (4.3s): "Until you face insane legendary bosses, like the Sun Fish Boss..."
        ("assets/33_Clip 33.mp4", 0.8, 4.3, False),
        
        # 6. 20.8s - 23.5s (2.7s): "...and the deadly Piranha Boss!"
        ("assets/38_Clip 38.mp4", 1.5, 2.7, False),
        
        # 7. 23.5s - 28.5s (5.0s): Endcard: "Think you can survive? Search How to Fisch on Roblox and play right now!"
        ("assets/37_Clip 37.mp4", 1.0, 5.0, "blurred_endcard")
    ]

    concat_list_path = "temp/concat_list_v2.txt"
    with open(concat_list_path, "w", encoding="utf-8") as clist:
        for idx, (source, start, dur, kind) in enumerate(segments):
            seg_out = f"temp/v2_segments/seg_{idx:02d}.mp4"
            if kind != "blurred_endcard":
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", str(start),
                    "-t", str(dur),
                    "-i", source,
                    "-vf", "crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-af", "volume=0.20,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo",
                    "-c:a", "aac", "-b:a", "192k",
                    seg_out
                ]
            else:
                # Living blurred gameplay background + endcard_overlay.png
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", str(start),
                    "-t", str(dur),
                    "-i", source,
                    "-i", "assets/endcard_overlay.png",
                    "-filter_complex", (
                        "[0:v]crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920:flags=lanczos,"
                        "gblur=sigma=22:steps=3,eq=brightness=-0.08:contrast=1.1,fps=30[bg];"
                        "[1:v]scale=1080:1920[ov];"
                        "[bg][ov]overlay=0:0[v]"
                    ),
                    "-map", "[v]",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-af", "volume=0.15,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo",
                    "-c:a", "aac", "-b:a", "192k",
                    seg_out
                ]
            run_cmd(cmd, f"Processing segment {idx+1}/{len(segments)}")
            clist.write(f"file '{os.path.abspath(seg_out)}'\n")

    raw_video = "temp/raw_concatenated_v2.mp4"
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy",
        raw_video
    ]
    run_cmd(concat_cmd, "Concatenating segments for Video 2")

    final_output = "output/how_to_fisch_combat_bosses.mp4"
    ass_subtitles = "subtitles/captions_v2.ass"
    ass_escaped = ass_subtitles.replace("\\", "/").replace(":", "\\:")

    # Intro badge pops in at 3.6s to 5.4s (over How to Fisch welcome)
    filter_complex = (
        f"[0:v][1:v]overlay=0:0:enable='between(t,3.6,5.4)'[v_badge];"
        f"[v_badge]ass='{ass_escaped}'[v_out];"
        "[2:a]volume=1.45,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[vo];"
        "[3:a]volume=0.16,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[bgm];"
        "[0:a]volume=0.35,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[sfx];"
        "[vo][bgm][sfx]amix=inputs=3:duration=first:weights=1.0 0.5 0.5[a_out]"
    )

    final_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", "assets/intro_badge.png",
        "-i", "temp/voiceover_v2.wav",
        "-i", "assets/bgm.mp3",
        "-filter_complex", filter_complex,
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-t", "28.5",
        "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        final_output
    ]

    run_cmd(final_cmd, "Rendering how_to_fisch_combat_bosses.mp4 with Intro Badge & Endcard")
    print(f"\nSUCCESS! Rendered final cinematic video to: {final_output}")
    print(f"File size: {os.path.getsize(final_output) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()
