"""Render reviewed short-form edits through the bundled ffmpeg-skill.

Usage: python scripts/render_retention.py campaigns/how_to_fisch/edits/09_fish_fight_back.json --dry-run
       python scripts/render_retention.py campaigns/how_to_fisch/edits/09_fish_fight_back.json

No cloud calls. Paths in an edit are workspace-relative; invoking from another cwd is safe.
"""
import argparse
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/ffmpeg-skill/scripts"
FPS = 30


def workspace_path(value):
    path = (ROOT / value).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError(f"Path must remain inside this workspace: {value}")
    return path


def number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"Expected finite numeric time, got {value!r}")
    return float(value)


def dump(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def tool(name, *args, log=None):
    cmd = [sys.executable, str(SKILL / name), *map(str, args), "--json"]
    env = dict(os.environ, FFMPEG_SKILL_NO_OVERWRITE="1", PYTHONIOENCODING="utf-8")
    result = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", timeout=1800)
    if log:
        log.write_text(result.stdout + "\n" + result.stderr, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(f"{name} failed ({result.returncode}):\n{result.stdout[-2500:]}\n{result.stderr[-1500:]}")
    return json.loads(result.stdout)


def validate(edit, catalog, probes):
    """Fail before rendering when a timeline is impossible or a shot contradicts its tags."""
    if edit.get("fps") != FPS:
        raise ValueError("This delivery pipeline requires 30 fps")
    source_duration = probes[edit["voice"]]["duration"]
    voice_total = 0.0
    remapped = []
    for segment in edit["voice_segments"]:
        start, end = number(segment["in"]), number(segment["out"])
        if not 0 <= start < end <= source_duration:
            raise ValueError("Voice cut outside source bounds")
        last = start
        for cue in segment["cues"]:
            a, b = number(cue[0]), number(cue[1])
            if not start <= a < b <= end or a < last:
                raise ValueError("Caption overlaps or falls outside its voice segment")
            if not isinstance(cue[2], str) or not cue[2].strip():
                raise ValueError("Empty caption")
            if any(c in cue[2] for c in ("{", "}", "\\", "\n", "\r")):
                raise ValueError("Caption must be plain single-line text; use | for a line break")
            lines = cue[2].split("|")
            if len(lines) > 2 or any(len(line) > 30 for line in lines):
                raise ValueError("Caption exceeds two lines / 30 characters per line")
            if b - a < 0.65:
                raise ValueError("Caption flashes too quickly; regroup words")
            remapped.append([round(voice_total + a - start, 3),
                             round(voice_total + b - start, 3), cue[2]])
            last = b
        voice_total += end - start
    if not edit["voice_segments"] or not remapped:
        raise ValueError("Empty voice/caption timeline")
    video_frames = 0
    shot_timeline = []
    for shot in edit["shots"]:
        entry = catalog[shot["clip"]]
        src = entry["src"]
        start, frames = number(shot["in"]), shot["frames"]
        if isinstance(frames, bool) or not isinstance(frames, int) or frames < 1:
            raise ValueError("Shot length must be a positive integer frame count")
        if not 0 <= start < start + frames / FPS <= probes[src]["duration"]:
            raise ValueError(f"Shot {shot['clip']} extends beyond its actual source duration")
        if not entry.get("reviewed") or not entry.get("evidence"):
            raise ValueError(f"Shot {shot['clip']} has no visual review evidence")
        if not set(shot["requires"]).issubset(entry["tags"]):
            raise ValueError(f"Shot {shot['clip']} does not support {shot['requires']}")
        anchor = number(shot.get("crop_x", 0.5))
        if not 0 <= anchor <= 1:
            raise ValueError("crop_x must lie between 0 and 1")
        shot_timeline.append({**shot, "src": src, "timeline_in": video_frames / FPS,
                              "timeline_out": (video_frames + frames) / FPS})
        video_frames += frames
    if abs(video_frames / FPS - voice_total) > 0.0001:
        raise ValueError(f"Video/voice duration mismatch: {video_frames / FPS:.3f} vs {voice_total:.3f}")
    cta = number(edit["cta_start"])
    if not 0 <= cta < voice_total or voice_total - cta > 3.5:
        raise ValueError("CTA must be inside the video and no longer than 3.5 seconds")
    if not shot_timeline or "combat" not in catalog[shot_timeline[0]["clip"]]["tags"]:
        raise ValueError("This experiment requires gameplay combat on its first frame")
    if not any("How to Fisch" in cue[2] for cue in remapped if cue[0] >= cta):
        raise ValueError("Closing captions must identify How to Fisch")
    return {"duration": round(voice_total, 3), "frames": video_frames,
            "cues": remapped, "shots": shot_timeline,
            "note": "Technical/editorial checks are not a retention prediction. Inspect the final picture and listen."}


def ass_time(seconds):
    cs = round(seconds * 100)
    return f"{cs // 360000}:{cs // 6000 % 60:02}:{cs // 100 % 60:02}.{cs % 100:02}"


def captions(plan):
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Phrase,Arial,64,&H00FFFFFF,&H00FFFFFF,&H0015100C,&H80000000,-1,0,0,0,100,100,0,0,1,4,1,2,100,190,620,1
Style: Hook,Arial,60,&H008FE9FF,&H008FE9FF,&H0015100C,&H80000000,-1,0,0,0,100,100,0,0,1,4,1,8,100,190,175,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = ["Dialogue: 1,0:00:00.00,0:00:02.70,Hook,,0,0,0,,The fish fight back."]
    for start, end, text in plan["cues"]:
        # Fixed position and stable phrase. No bouncing, zoom or colour cycling.
        text = text.replace("|", r"\N")
        events.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Phrase,,0,0,0,,{text}")
    return header + "\n".join(events) + "\n"


def join_exact(plan, shots, output, work):
    """Trim decoded A/V to exact frame/sample counts before concat.

    The bundled join.py uses container durations, including AAC padding. Its
    closest option, transition=none, accumulated 0.24s in this seven-shot edit.
    This project-specific assembly stage removes that padding at every cut.
    Other transforms, normalization, export and checks use ffmpeg-skill.
    """
    executable = shutil.which("ffmpeg")
    if not executable:
        raise ValueError("ffmpeg is not on PATH")
    command = [executable, "-hide_banner", "-loglevel", "error", "-nostdin", "-n"]
    filters, labels = [], []
    for i, (shot, source) in enumerate(zip(plan["shots"], shots)):
        command += ["-i", source["src"]]
        samples = shot["frames"] * (48000 // FPS)
        filters += [f"[{i}:v]fps={FPS},trim=end_frame={shot['frames']},setpts=PTS-STARTPTS,setsar=1[v{i}]",
                    f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_len={samples},"
                    f"atrim=end_sample={samples},asetpts=PTS-STARTPTS[a{i}]"]
        labels.append(f"[v{i}][a{i}]")
    filters.append("".join(labels) + f"concat=n={len(shots)}:v=1:a=1[v][a]")
    command += ["-filter_complex_threads", "1", "-filter_complex", ";".join(filters),
                "-map", "[v]", "-map", "[a]", "-r", str(FPS), "-fps_mode", "cfr",
                "-frames:v", str(plan["frames"]), "-t", str(plan["duration"]),
                "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", str(output)]
    dump(work / "assembly_command.json", command)
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8",
                            errors="replace", timeout=1800, cwd=ROOT)
    (work / "assembly.log").write_text(result.stderr, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(f"Frame-accurate assembly failed: {result.stderr[-2500:]}")
    check_picture(tool("probe.py", output), plan, 1080, 1350)


def check_picture(probe, plan, width, height):
    video = probe["video"]
    if (video.get("nb_frames") != plan["frames"] or video["fps"] != FPS or
            (video["width"], video["height"]) != (width, height)):
        raise ValueError("Rendered video dimensions, fps or frame count differ from planned timeline")
    if abs(probe["duration"] - plan["duration"]) > 1 / FPS:
        raise ValueError("Rendered A/V duration differs from planned timeline")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("edit")
    ap.add_argument("--dry-run", action="store_true", help="Probe and validate; write/render nothing")
    args = ap.parse_args()
    edit_path = workspace_path(args.edit)
    edit = json.loads(edit_path.read_text(encoding="utf-8"))
    catalog = json.loads(workspace_path(edit["catalog"]).read_text(encoding="utf-8"))
    input_paths = {edit["voice"], edit["music"], edit["icon"]}
    input_paths.update(catalog[s["clip"]]["src"] for s in edit["shots"])
    for value in input_paths:
        if not workspace_path(value).is_file():
            raise ValueError(f"Missing input: {value}")
    output = workspace_path(edit["output"])
    if output.suffix.lower() != ".mp4" or output in [workspace_path(p) for p in input_paths]:
        raise ValueError("Output must be a new MP4, separate from all inputs")
    artifacts = [output, output.with_suffix(".ass"), output.with_suffix(".srt"),
                 output.with_suffix(".qa.json"), output.with_name(output.stem + "_metadata.md"),
                 output.with_name(output.stem + "_sheet.png")]
    if any(p.exists() for p in artifacts):
        raise ValueError("Output or companion already exists; choose a new output basename in the edit")
    probes = {p: tool("probe.py", workspace_path(p)) for p in sorted(input_paths) if p != edit["icon"]}
    plan = validate(edit, catalog, probes)
    print(json.dumps(plan, indent=2), flush=True)
    if args.dry_run:
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    work_root = ROOT / "temp/retention_runs"
    work_root.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix=output.stem + "_", dir=work_root))
    dump(work / "edit.json", edit)
    dump(work / "probes.json", probes)
    dump(work / "timeline.json", plan)
    # The voice project performs accurate cuts at measured word boundaries, at original speed.
    voice = work / "voice.wav"
    voice_project = {"output": str(voice), "transition": {"type": "none"}, "clips": [
        {"src": str(workspace_path(edit["voice"])), "in": s["in"], "out": s["out"]}
        for s in edit["voice_segments"]]}
    dump(work / "voice_project.json", voice_project)
    tool("render.py", work / "voice_project.json", "--dry-run", log=work / "voice_plan.log")
    tool("render.py", work / "voice_project.json", log=work / "voice_render.log")
    measured_voice = tool("probe.py", voice)
    if abs(measured_voice["duration"] - plan["duration"]) > 0.02:
        raise ValueError("Rendered narration length differs from edit")
    rendered_shots = []
    for i, shot in enumerate(plan["shots"]):
        print(f"Shot {i + 1}/{len(plan['shots'])}: {shot['clip']} - {shot['purpose']}", flush=True)
        cut = work / f"shot_{i:02}_cut.mp4"
        framed = work / f"shot_{i:02}.mp4"
        cut_args = [workspace_path(shot["src"]), "--start", shot["in"], "--duration",
                    shot["frames"] / FPS, "--accurate", "-o", cut]
        tool("cut.py", *cut_args, "--dry-run", log=work / f"shot_{i:02}_cut_plan.log")
        tool("cut.py", *cut_args, log=work / f"shot_{i:02}_cut.log")
        fit_args = [cut, "--aspect", "4:5", "--fit", "crop", "--crop-x", shot.get("crop_x", 0.5),
                    "--width", 1080, "--fps", FPS, "-o", framed]
        tool("fit.py", *fit_args, "--dry-run", log=work / f"shot_{i:02}_fit_plan.log")
        tool("fit.py", *fit_args, log=work / f"shot_{i:02}_fit.log")
        probe = tool("probe.py", framed)
        if probe["video"].get("nb_frames") != shot["frames"]:
            raise ValueError(f"Shot {i} frame count drifted from plan")
        rendered_shots.append({"src": str(framed)})
    joined = work / "joined.mp4"
    join_exact(plan, rendered_shots, joined, work)
    picture = work / "picture.mp4"
    # Explicit dimensions are necessary: the bundled project renderer consumes
    # frame.width/fps at join, then its fit stage can fall back to source height.
    fit_args = [joined, "--aspect", "9:16", "--fit", "blur", "--width", 1080,
                "--height", 1920, "--fps", FPS, "-o", picture]
    tool("fit.py", *fit_args, "--dry-run", log=work / "picture_plan.log")
    tool("fit.py", *fit_args, log=work / "picture_render.log")
    check_picture(tool("probe.py", picture), plan, 1080, 1920)
    game_audio = work / "game.wav"
    tool("audio.py", picture, "-o", game_audio, log=work / "game_audio.log")
    ass = work / "captions.ass"
    ass.write_text(captions(plan), encoding="utf-8")
    def srt_time(t):
        ms = round(t * 1000)
        return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"
    (work / "captions.srt").write_text("\n\n".join(
        f"{i + 1}\n{srt_time(a)} --> {srt_time(b)}\n{text.replace('|', chr(10))}"
        for i, (a, b, text) in enumerate(plan["cues"])) + "\n", encoding="utf-8")
    delivery = work / "delivery.mp4"
    final_project = {
        "output": str(delivery), "clips": [{"src": str(picture)}], "captions": {"ass": str(ass)},
        "overlays": [{"image": str(workspace_path(edit["icon"])), "position": "top-left",
                      "start": edit["cta_start"], "end": plan["duration"], "scale": 180,
                      "margin": 160, "fade": 0.12}],
        "audio": {"replace": str(voice), "music": str(workspace_path(edit["music"])),
                  "effects": str(game_audio), "stereo": True, "duck": True,
                  "duck_amount": 10, "duck_threshold": -30, "duck_attack": 15,
                  "duck_release": 300, "music_fade_out": 0.5,
                  "stems": {"dialogue": 0, "music": -24, "effects": -22}},
        "loudness": {"lufs": -14, "tp": -1.5},
        "export": {"preset": "shorts", "crf": 18, "normalize": False},
        "check": {"platform": "shorts"}}
    dump(work / "final_project.json", final_project)
    tool("render.py", work / "final_project.json", "--dry-run", log=work / "final_plan.log")
    print("Rendering captions, voice-led mix and final Shorts export...", flush=True)
    result = tool("render.py", work / "final_project.json", log=work / "final_render.log")
    probe = tool("probe.py", delivery)
    check_picture(probe, plan, 1080, 1920)
    check = tool("check.py", delivery, "--platform", "shorts", log=work / "check.log")
    loudness = tool("loudness.py", delivery, "--measure-only", log=work / "loudness.log")
    sheet = output.with_name(output.stem + "_sheet.png")
    tool("look.py", delivery, "--tiles", "4x3", "--width", 1440, "-o", work / "sheet.png", log=work / "look.log")
    # Only verified renders are copied to the deliverables folder. Exclusive
    # creation prevents an accidental overwrite even if another job ran meanwhile.
    for source, dest in [(delivery, output), (ass, output.with_suffix(".ass")),
                         (work / "captions.srt", output.with_suffix(".srt")), (work / "sheet.png", sheet)]:
        with source.open("rb") as src, dest.open("xb") as dst:
            shutil.copyfileobj(src, dst)
    probe["file"] = str(output)
    dump(output.with_suffix(".qa.json"), {"probe": probe, "check": check, "loudness": loudness,
         "edit": str(edit_path.relative_to(ROOT)), "work": str(work.relative_to(ROOT)),
         "timeline": plan, "render_verified": result.get("verified"),
         "visual_review": "pending human/agent inspection of sheet and motion",
         "retention": "unmeasured; requires YouTube Studio after publishing"})
    metadata = "# " + edit["titles"][0] + "\n\n## Title options\n\n" + "\n".join(
        f"- {title}" for title in edit["titles"])
    metadata += "\n\n## Description\n\n" + edit["description"]
    metadata += "\n\n## Pinned comment suggestion\n\n" + edit["comment"]
    metadata += "\n\n## Hashtags\n\n#Roblox #HowToFisch #RobloxGames\n"
    output.with_name(output.stem + "_metadata.md").write_text(metadata, encoding="utf-8")
    print(f"DONE: {output}\nReview sheet: {sheet}\nLogs: {work}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, RuntimeError, subprocess.TimeoutExpired) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
