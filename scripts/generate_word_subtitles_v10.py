import sys
import os
import re
from faster_whisper import WhisperModel

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"

def generate_subtitles():
    audio_path = "temp/voiceover_v10_fast.wav"
    out_ass = "campaigns/how_to_fisch/subtitles/captions_v10.ass"
    os.makedirs("campaigns/how_to_fisch/subtitles", exist_ok=True)
    
    print(f"Loading faster-whisper model for {audio_path}...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path, word_timestamps=True)
    
    words_list = []
    for s in segments:
        for w in s.words:
            clean_word = w.word.strip().upper()
            clean_word = re.sub(r"[^\w\s\?!,]", "", clean_word).strip()
            if clean_word:
                words_list.append({
                    "start": w.start,
                    "end": max(w.end, w.start + 0.16),
                    "word": clean_word
                })
                
    print(f"Total raw words: {len(words_list)}")
    
    ass_lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: WordWhite,Impact,76,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,7,4,5,60,60,60,1",
        "Style: WordGold,Impact,84,&H0020E5FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,60,1",
        "Style: WordRed,Impact,84,&H003344FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,60,1",
        "Style: WordGreen,Impact,84,&H0033FF66,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,60,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]

    i = 0
    while i < len(words_list):
        w_obj = words_list[i]
        word = w_obj["word"].replace(",", "").replace(".", "").replace("!", "").replace("?", "")
        
        if word == "HOW" and i + 2 < len(words_list) and "FISH" in words_list[i+2]["word"]:
            chunk_words = [words_list[i], words_list[i+1], words_list[i+2]]
            chunk_words[2]["word"] = "FISCH"
            i += 3
        elif word == "LIVING" and i + 1 < len(words_list) and "BURRITOS" in words_list[i+1]["word"]:
            chunk_words = [words_list[i], words_list[i+1]]
            i += 2
        elif word == "MUTANT" and i + 1 < len(words_list) and "BEAST" in words_list[i+1]["word"]:
            chunk_words = [words_list[i], words_list[i+1]]
            i += 2
        elif word == "OCEAN" and i + 1 < len(words_list) and "MONSTERS" in words_list[i+1]["word"]:
            chunk_words = [words_list[i], words_list[i+1]]
            i += 2
        elif word == "PLAY" and i + 1 < len(words_list) and "NOW" in words_list[i+1]["word"]:
            chunk_words = [words_list[i], words_list[i+1]]
            i += 2
        else:
            chunk_words = [w_obj]
            i += 1
            
        start_t = chunk_words[0]["start"]
        end_t = chunk_words[-1]["end"]
        if end_t - start_t < 0.18:
            end_t = start_t + 0.18
            
        text_str = " ".join(c["word"] for c in chunk_words)
        text_str = text_str.replace("FISH", "FISCH")
        
        style = "WordWhite"
        if any(k in text_str for k in ["HOW TO FISCH", "ROBLOX", "WEIRDEST", "BURRITOS", "MONSTERS"]):
            style = "WordGold"
        elif any(k in text_str for k in ["MUTANT", "PUNCH", "SHOTGUNS", "CROWBARS"]):
            style = "WordRed"
        elif any(k in text_str for k in ["PLAY RIGHT NOW", "CASH", "OVERPOWERED"]):
            style = "WordGreen"
            
        # Endcard starts at 27.20s
        y_pos = 1460 if start_t >= 27.20 else 980
        
        anim_tag = r"{\fscx125\fscy125\t(0,70,\fscx100\fscy100)}"
        pos_tag = f"{{\\pos(540,{y_pos})}}"
        
        start_str = format_time(start_t)
        end_str = format_time(end_t)
        
        line = f"Dialogue: 0,{start_str},{end_str},{style},,0,0,0,,{pos_tag}{anim_tag}{text_str}"
        ass_lines.append(line)
        
    with open(out_ass, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines))
        
    print(f"Generated {len(ass_lines) - 15} subtitle events in {out_ass}!")

if __name__ == "__main__":
    generate_subtitles()
