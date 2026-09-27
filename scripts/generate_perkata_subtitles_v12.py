import json
import os
import re

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"

def main():
    with open("temp/v12_whisper_words.json", "r", encoding="utf-8") as f:
        words = json.load(f)

    out_ass = "campaigns/how_to_fisch/subtitles/captions_v12_perkata.ass"
    os.makedirs("campaigns/how_to_fisch/subtitles", exist_ok=True)

    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: WordWhite,Impact,92,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,60,1
Style: WordGold,Impact,98,&H0020E5FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,60,1
Style: WordRed,Impact,98,&H003344FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,60,1
Style: WordGreen,Impact,98,&H0033FF66,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    events = []
    total_words = len(words)

    for i in range(total_words):
        w = words[i]
        word_text = w["word"].upper()
        # Clean punctuation for text logic, keep essential
        clean_w = re.sub(r"[^\w]", "", word_text)

        # Fix spelling for campaign requirement: FISH -> FISCH
        if clean_w in ["FISH", "FISH,"]:
            word_text = "FISCH"
            clean_w = "FISCH"
        if clean_w == "SQUAT": # whisper might transcribe squad as squat
            word_text = "SQUAD"
            clean_w = "SQUAD"

        start_t = w["start"]

        # Calculate natural end time so it NEVER disappears too quickly
        if i + 1 < total_words:
            next_start = words[i + 1]["start"]
            # If gap to next word is small (<0.35s), hold until next word starts (smooth reading)
            if next_start - w["end"] < 0.35:
                end_t = next_start
            else:
                # Pause between phrases, hold word for a comfortable moment
                end_t = min(w["end"] + 0.28, next_start)
        else:
            end_t = w["end"] + 0.35

        # Ensure minimum screen presence of 0.22s so viewer's brain can register it
        if end_t - start_t < 0.22:
            end_t = start_t + 0.22

        # Style selection
        style = "WordWhite"
        if clean_w in ["ROBLOX", "HOW", "FISCH", "MOTORBOAT", "SHOTGUNS", "TITANS", "BOUNTY", "GRANNY"]:
            style = "WordGold"
        elif clean_w in ["MUTANT", "MONSTERS", "BLAST", "SURVIVE", "STORMY", "FUN"]:
            style = "WordRed"
        elif clean_w in ["PLAY", "NOW", "CASH", "BURRITO", "FAST", "CREW", "WIN"]:
            style = "WordGreen"

        # Position: Endcard starts at ~24.60s
        y_pos = 1460 if start_t >= 24.60 else 980

        # Subtle pop animation on entry
        anim_tag = r"{\fscx120\fscy120\t(0,50,\fscx100\fscy100)}"
        pos_tag = f"{{\\pos(540,{y_pos})}}"

        start_str = format_time(start_t)
        end_str = format_time(end_t)

        line = f"Dialogue: 0,{start_str},{end_str},{style},,0,0,0,,{pos_tag}{anim_tag}{word_text}"
        events.append(line)

    with open(out_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")

    print(f"Generated {len(events)} word-by-word subtitle events in {out_ass}!")

if __name__ == "__main__":
    main()
