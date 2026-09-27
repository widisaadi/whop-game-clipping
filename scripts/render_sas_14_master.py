import os
import subprocess
import shutil
import json

def run_cmd(cmd, desc):
    print(f"\n--- {desc} ---", flush=True)
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="ignore")
    if res.returncode != 0:
        print(f"Error in {desc}:", flush=True)
        print(res.stderr[-800:], flush=True)
        raise RuntimeError(f"Command failed: {desc}")
    return res

def main():
    camp = "steal_a_seed"
    vid_id = "14_steal_a_seed_50k_speed_sonic_sprint"
    
    out_dir = os.path.join("campaigns", camp, "output")
    temp_dir = os.path.join("temp", camp)
    seg_dir = os.path.join(temp_dir, f"segments_{vid_id}")
    
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)
    if os.path.exists(seg_dir):
        shutil.rmtree(seg_dir)
    os.makedirs(seg_dir, exist_ok=True)
    
    final_output = os.path.join(out_dir, f"{vid_id}.mp4")
    sheet_output = os.path.join(out_dir, f"{vid_id}_sheet.png")
    
    vo_path = os.path.join(temp_dir, "voiceover_14_fast.wav")
    sfx_track = os.path.join(temp_dir, "sfx_track_14.wav")
    ass_path = os.path.join("campaigns", camp, "subtitles", f"{vid_id}.ass")
    endcard_frames_pattern = "temp/steal_a_seed/endcard_frames/frame_%04d.png"
    
    segments = [
        ("shared/hooks/INTRO.mp4", 0.0, 1.40, "intro_clip"),
        ("campaigns/steal_a_seed/assets/clips/31_Clip 31.mp4", 0.0, 3.40, "blurred_bg"),
        ("campaigns/steal_a_seed/assets/clips/27_Clip 27.mp4", 0.0, 5.00, "blurred_bg"),
        ("campaigns/steal_a_seed/assets/clips/23_Clip 23.mp4", 0.0, 3.80, "blurred_bg"),
        ("campaigns/steal_a_seed/assets/clips/24_Clip 24.mp4", 0.0, 2.90, "blurred_bg"),
        ("campaigns/steal_a_seed/assets/clips/27_Clip 27.mp4", 5.0, 2.40, "blurred_bg"),
        ("campaigns/steal_a_seed/assets/clips/04_Clip 4.mp4", 0.0, 4.08, "blurred_bg"),
        ("campaigns/steal_a_seed/assets/clips/31_Clip 31.mp4", 3.5, 2.27, "endcard_anim")
    ]
    
    total_dur = sum(s[2] for s in segments)
    print(f"Target Video Duration: {total_dur:.2f}s", flush=True)
    
    concat_list_path = os.path.join(temp_dir, f"concat_list_{vid_id}.txt")
    raw_video = os.path.join(temp_dir, f"raw_concatenated_{vid_id}.mp4")
    
    with open(concat_list_path, "w", encoding="utf-8") as clist:
        for idx, (source, start, dur, otype) in enumerate(segments):
            seg_out = os.path.join(seg_dir, f"seg_{idx:02d}.mp4")
            if otype == "intro_clip":
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-vf", "scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p",
                    "-af", "volume=0.10,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-video_track_timescale", "15360",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    seg_out
                ]
            elif otype == "endcard_anim":
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-start_number", "0",
                    "-framerate", "30",
                    "-i", endcard_frames_pattern,
                    "-filter_complex",
                    "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=26:6,eq=brightness=-0.18:contrast=1.05[bg];"
                    "[bg][1:v]overlay=0:0,fps=30,setsar=1,format=yuv420p[v];"
                    "[0:a]volume=0.25,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a]",
                    "-map", "[v]",
                    "-map", "[a]",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-video_track_timescale", "15360",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    seg_out
                ]
            else:
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-filter_complex",
                    "[0:v]split[fg_raw][bg_raw];"
                    "[bg_raw]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=26:6,eq=brightness=-0.18:contrast=1.05[bg];"
                    "[fg_raw]scale=1080:1080:force_original_aspect_ratio=increase,crop=1080:1080:(in_w-out_w)/2:(in_h-out_h)/2[fg];"
                    "[bg][fg]overlay=0:420,fps=30,setsar=1,format=yuv420p[v];"
                    "[0:a]volume=0.30,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a]",
                    "-map", "[v]",
                    "-map", "[a]",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-video_track_timescale", "15360",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    seg_out
                ]
            run_cmd(cmd, f"Rendering Seg {idx+1}/{len(segments)} ({dur:.2f}s)")
            clist.write(f"file '{os.path.abspath(seg_out).replace(chr(92), '/')}'\n")
            
    # Concat
    run_cmd(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", raw_video], f"Concatenating {vid_id}")
    
    # Mix Audio & Subtitles
    temp_master = os.path.join(temp_dir, f"master_{vid_id}.mp4")
    abs_ass = os.path.abspath(ass_path).replace("\\", "/")
    if ":" in abs_ass:
        drive, rest = abs_ass.split(":", 1)
        ass_filter_path = f"{drive}\\:{rest}"
    else:
        ass_filter_path = abs_ass
        
    fade_st = max(0.0, total_dur - 1.9)
    mix_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", vo_path,
        "-i", "assets/bgm3.mp3",
        "-i", sfx_track,
        "-filter_complex",
        f"[0:v]subtitles='{ass_filter_path}'[v];"
        f"[0:a]volume=0.18[a_game];"
        f"[1:a]volume=1.35,volume=4dB[a_vox];"
        f"[2:a]volume=0.22,volume=-5dB,afade=t=out:st={fade_st:.1f}:d=1.9[a_bgm];"
        f"[3:a]volume=0.90[a_sfx];"
        f"[a_game][a_vox][a_bgm][a_sfx]amix=inputs=4:duration=first:dropout_transition=2[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", "30",
        "-c:a", "aac", "-b:a", "256k",
        "-t", f"{total_dur:.2f}",
        temp_master
    ]
    run_cmd(mix_cmd, f"Mixing Master with Subtitles & Audio for {vid_id}")
    
    # Loudness Normalization EBU R128 (-14.0 LUFS)
    loudness_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/loudness.py",
        temp_master,
        "-I", "-14",
        "--tp", "-1.5",
        "-o", final_output,
        "--overwrite"
    ]
    run_cmd(loudness_cmd, f"2-Pass Loudness Normalization (-14.0 LUFS)")
    
    # Retag Color Space to BT.709
    retag_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/color.py",
        final_output,
        "--retag", "bt709",
        "--overwrite"
    ]
    run_cmd(retag_cmd, f"Retagging color space BT.709")
    retagged_file = os.path.join(out_dir, f"{vid_id}_retag.mp4")
    if os.path.exists(retagged_file):
        try:
            if os.path.exists(final_output):
                os.remove(final_output)
            os.replace(retagged_file, final_output)
        except Exception:
            pass
            
    # Contact Sheet
    look_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/look.py",
        final_output,
        "--tiles", "3x2",
        "-o", sheet_output,
        "--overwrite"
    ]
    run_cmd(look_cmd, f"Generating visual contact sheet")
    
    print(f"\n[SUCCESS] Master Video Rendered: {final_output} ({os.path.getsize(final_output)/(1024*1024):.2f} MB)", flush=True)

if __name__ == "__main__":
    main()
