import os
import subprocess
import sys

def run_cmd(cmd, desc):
    print(f"--> {desc}...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="ignore")
    if res.returncode != 0:
        print(f"Error in {desc}:")
        print(res.stderr[-600:])
        sys.exit(1)
    return res

def main():
    os.makedirs("temp/achird_segments", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    raw_video = "temp/raw_concatenated_achird.mp4"
    segments = [
        ("assets/07_Clip 7.mp4", 0.0, 2.3, False),
        ("assets/10_Clip 10.mp4", 1.0, 1.7, False),
        ("assets/08_Clip 8.mp4", 2.0, 2.0, False),
        ("assets/05_Clip 5.mp4", 1.5, 2.0, False),
        ("assets/24_Clip 24.mp4", 0.8, 2.7, False),
        ("assets/05_Clip 5.mp4", 3.5, 2.7, False),
        ("assets/09_Clip 9.mp4", 0.5, 2.5, False),
        ("assets/13_Clip 13.mp4", 0.5, 2.1, False),
        ("assets/14_Clip 14.mp4", 1.0, 3.1, False),
        ("assets/15_Clip 15.mp4", 1.5, 1.7, False),
        ("assets/19_Clip 19.mp4", 1.0, 2.3, False),
        ("assets/31_Clip 31.mp4", 1.0, 2.1, False),
        ("assets/endcard.png", 0.0, 5.3, True)
    ]
    
    concat_list_path = "temp/concat_list_achird.txt"
    with open(concat_list_path, "w", encoding="utf-8") as clist:
        for idx, (source, start, dur, is_img) in enumerate(segments):
            seg_out = f"temp/achird_segments/seg_{idx:02d}.mp4"
            if not os.path.exists(seg_out):
                if not is_img:
                    cmd = [
                        "ffmpeg", "-y",
                        "-ss", str(start),
                        "-t", str(dur),
                        "-i", source,
                        "-vf", "crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30",
                        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                        "-af", "volume=0.25,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo",
                        "-c:a", "aac", "-b:a", "192k",
                        seg_out
                    ]
                else:
                    cmd = [
                        "ffmpeg", "-y",
                        "-loop", "1",
                        "-t", str(dur),
                        "-i", source,
                        "-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=48000:cl=stereo",
                        "-vf", "scale=1080:1920:flags=lanczos,setsar=1,fps=30",
                        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "192k",
                        "-shortest",
                        seg_out
                    ]
                run_cmd(cmd, f"Processing segment {idx+1}/{len(segments)}")
            clist.write(f"file '{os.path.abspath(seg_out).replace(chr(92), '/')}'\n")

    concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", raw_video]
    run_cmd(concat_cmd, "Concatenating segments for Achird video")

    final_output = "output/how_to_fisch_gemini_achird.mp4"
    
    # Subtitle filter with captions_gemini_achird.ass
    ass_path = os.path.abspath("subtitles/captions_gemini_achird.ass").replace("\\", "/")
    if ":" in ass_path:
        drive, rest = ass_path.split(":", 1)
        ass_filter_path = f"{drive}\\:{rest}"
    else:
        ass_filter_path = ass_path

    mix_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", "temp/gemini_voiceover_achird.wav",
        "-i", "assets/bgm.mp3",
        "-filter_complex",
        f"[0:v]subtitles='{ass_filter_path}'[v];"
        f"[0:a]volume=0.30[a_sfx];"
        f"[1:a]volume=1.20[a_vox];"
        f"[2:a]volume=0.18,afade=t=out:st=30.5:d=2.0[a_bgm];"
        f"[a_sfx][a_vox][a_bgm]amix=inputs=3:duration=first:dropout_transition=2[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", "32.5",
        final_output
    ]
    run_cmd(mix_cmd, "Rendering how_to_fisch_gemini_achird.mp4 with Achird TTS & Pop-up Subtitles")

    print(f"\nSUCCESS! Rendered final video to: {final_output}")
    print(f"File size: {os.path.getsize(final_output) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()
