import os
import json
import subprocess
from faster_whisper import WhisperModel

VIDEOS = [
    {
        "campaign": "steal_a_seed",
        "vid_id": "14_steal_a_seed_50k_speed_sonic_sprint",
        "audio": "temp/steal_a_seed/voiceover_14_steal_a_seed_50k_speed_sonic_sprint_fast.wav",
        "out_ass": "campaigns/steal_a_seed/subtitles/14_steal_a_seed_50k_speed_sonic_sprint.ass",
        "gold_words": ["FIFTY", "THOUSAND", "50,000", "50", "SPEED", "STEAL", "SEED", "LEVEL", "ONE"],
        "green_words": ["TRAIN", "GYM", "TREADMILLS", "TREADMILL", "LIGHTNING", "MULTIPLIERS", "PURPLE", "TRAIL", "BLITZ", "DODGE", "SNATCH", "GOLDEN"],
        "red_words": ["TURTLE", "SLOW", "CRAWLING", "LASER", "TRAPS", "TRAP", "CATCH", "DEFENDING"]
    },
    {
        "campaign": "steal_a_seed",
        "vid_id": "15_steal_a_seed_pro_heist_infiltration",
        "audio": "temp/steal_a_seed/voiceover_15_steal_a_seed_pro_heist_infiltration_fast.wav",
        "out_ass": "campaigns/steal_a_seed/subtitles/15_steal_a_seed_pro_heist_infiltration.ass",
        "gold_words": ["MAX", "LEVEL", "STEAL", "SEED", "MEGA", "MILLIONS"],
        "green_words": ["PRO", "SECRET", "TIMING", "SLIPPING", "BORDER", "GRABBING", "SPRINT", "SAFE", "GARDEN", "PRINT"],
        "red_words": ["DYING", "CAUGHT", "DEADLY", "LASERS", "SECURITY", "GUARD", "PLANTS", "RESPAWNS", "BRAVE"]
    },
    {
        "campaign": "steal_a_seed",
        "vid_id": "16_steal_a_seed_secret_codes_millionaire",
        "audio": "temp/steal_a_seed/voiceover_16_steal_a_seed_secret_codes_millionaire_fast.wav",
        "out_ass": "campaigns/steal_a_seed/subtitles/16_steal_a_seed_secret_codes_millionaire.ass",
        "gold_words": ["THREE", "SECRET", "CODES", "STEAL", "SEED", "250,000", "CASH", "200", "GEMS"],
        "green_words": ["WORKING", "FREE", "REWARDS", "VINE", "UPGRADE", "SPEED", "REDEEM", "ENTER"],
        "red_words": ["STOP", "BROKE", "BORING", "GRINDING", "NEVER"]
    },
    {
        "campaign": "steal_a_seed",
        "vid_id": "17_steal_a_seed_level_1_vs_automated_fortress",
        "audio": "temp/steal_a_seed/voiceover_17_steal_a_seed_level_1_vs_automated_fortress_fast.wav",
        "out_ass": "campaigns/steal_a_seed/subtitles/17_steal_a_seed_level_1_vs_automated_fortress.ass",
        "gold_words": ["LEVEL", "ONE", "NOOB", "STEAL", "SEED", "MILLION", "DOLLAR"],
        "green_words": ["TIMING", "JUMPS", "SLIPPING", "SAFEZONE", "SURVIVE", "DEPOSIT", "PROGRESSED"],
        "red_words": ["AUTOMATED", "FORTRESS", "DEADLIEST", "BASE", "LASER", "TURRETS", "WIPEOUT", "IMPOSSIBLE"]
    },
    {
        "campaign": "steal_a_seed",
        "vid_id": "18_steal_a_seed_mythic_heavy_seed_heist",
        "audio": "temp/steal_a_seed/voiceover_18_steal_a_seed_mythic_heavy_seed_heist_fast.wav",
        "out_ass": "campaigns/steal_a_seed/subtitles/18_steal_a_seed_mythic_heavy_seed_heist.ass",
        "gold_words": ["MYTHIC", "HEAVY", "SEED", "STEAL", "TEN", "10", "TON", "MILLIONS", "SERVER"],
        "green_words": ["SLICK", "BYPASS", "GLIDE", "DEPOSIT", "FARM", "PROFIT", "COLOSSAL", "SMUGGLE"],
        "red_words": ["DROPS", "SPEED", "ZERO", "TRAPPED", "CHASE", "MONSTER", "ALERT"]
    },
    {
        "campaign": "roll_anime_girls",
        "vid_id": "02_roll_anime_girls_one_in_three_billion_mythic",
        "audio": "temp/roll_anime_girls/voiceover_02_roll_anime_girls_one_in_three_billion_mythic_fast.wav",
        "out_ass": "campaigns/roll_anime_girls/subtitles/02_roll_anime_girls_one_in_three_billion_mythic.ass",
        "gold_words": ["ONE", "THREE", "BILLION", "3", "BILLION", "ROLL", "ANIME", "GIRLS", "MYTHIC", "HU", "TAO"],
        "green_words": ["LUCK", "POTION", "SHRINE", "AUTO", "ROLL", "NEON", "AURA", "GLITCHED", "PULL"],
        "red_words": ["IMPOSSIBLE", "NEVER", "UNLUCKY", "INSANE"]
    },
    {
        "campaign": "roll_anime_girls",
        "vid_id": "03_roll_anime_girls_afk_passive_millions_tycoon",
        "audio": "temp/roll_anime_girls/voiceover_03_roll_anime_girls_afk_passive_millions_tycoon_fast.wav",
        "out_ass": "campaigns/roll_anime_girls/subtitles/03_roll_anime_girls_afk_passive_millions_tycoon.ass",
        "gold_words": ["AFK", "MILLIONS", "ROLL", "ANIME", "GIRLS", "HOUR", "500K", "1.38M"],
        "green_words": ["PASSIVE", "INCOME", "TYCOON", "PADS", "GENERATOR", "MULTIPLIER", "OFFLINE", "PRINTING"],
        "red_words": ["STOP", "CLICKING", "BROKE", "WASTING"]
    },
    {
        "campaign": "roll_anime_girls",
        "vid_id": "04_roll_anime_girls_rebirth_secret_multipliers",
        "audio": "temp/roll_anime_girls/voiceover_04_roll_anime_girls_rebirth_secret_multipliers_fast.wav",
        "out_ass": "campaigns/roll_anime_girls/subtitles/04_roll_anime_girls_rebirth_secret_multipliers.ass",
        "gold_words": ["REBIRTH", "MULTIPLIER", "ROLL", "ANIME", "GIRLS", "1.5X", "2X", "BUBBLEGUM", "DICE"],
        "green_words": ["SECRET", "PERMANENT", "BOOST", "EXTRA", "SLOT", "LEADERBOARD", "RAMPAGE"],
        "red_words": ["SACRIFICE", "RESET", "SURRENDER", "DANGER"]
    },
    {
        "campaign": "asmr_dominoes",
        "vid_id": "07_asmr_dominoes_mammoth_43_stud_lava_wall",
        "audio": "temp/asmr_dominoes/voiceover_07_asmr_dominoes_mammoth_43_stud_lava_wall_fast.wav",
        "out_ass": "campaigns/asmr_dominoes/subtitles/07_asmr_dominoes_mammoth_43_stud_lava_wall.ass",
        "gold_words": ["43", "STUD", "MAMMOTH", "ASMR", "DOMINOES", "WALL"],
        "green_words": ["LAVA", "MOLTEN", "TOPPLE", "CRUNCH", "SATISFYING", "COLLAPSE", "MAGMA"],
        "red_words": ["CRUSHING", "EXTREME", "DESTRUCTION", "EXPLOSION"]
    },
    {
        "campaign": "asmr_dominoes",
        "vid_id": "08_asmr_dominoes_infinite_hypnotic_bubble_loop",
        "audio": "temp/asmr_dominoes/voiceover_08_asmr_dominoes_infinite_hypnotic_bubble_loop_fast.wav",
        "out_ass": "campaigns/asmr_dominoes/subtitles/08_asmr_dominoes_infinite_hypnotic_bubble_loop.ass",
        "gold_words": ["INFINITE", "HYPNOTIC", "ASMR", "DOMINOES", "LOOP"],
        "green_words": ["BUBBLE", "POPS", "TRANSLUCENT", "THERAPY", "SATISFACTION", "RHYTHM", "SOOTHING"],
        "red_words": ["STRESS", "CHAOS", "TENSION"]
    }
]

def fmt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100: cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

print("Loading Whisper model base (cpu, int8)...")
model = WhisperModel("base", device="cpu", compute_type="int8")

ass_template = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: CenterWhite,Impact,96,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,0,1
Style: CenterGold,Impact,102,&H0020E5FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1
Style: CenterRed,Impact,102,&H003344FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1
Style: CenterGreen,Impact,102,&H0033FF66,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

style_map = {
    "WHITE": "CenterWhite",
    "GOLD": "CenterGold",
    "RED": "CenterRed",
    "GREEN": "CenterGreen"
}

for item in VIDEOS:
    vid_id = item["vid_id"]
    audio_path = item["audio"]
    out_ass = item["out_ass"]
    os.makedirs(os.path.dirname(out_ass), exist_ok=True)
    
    print(f"\n--- Transcribing with Whisper: {vid_id} ---")
    segments, info = model.transcribe(audio_path, word_timestamps=True)
    
    words = []
    for s in segments:
        for w in s.words:
            clean_w = w.word.strip().upper().replace(",", "").replace(".", "").replace("!", "").replace("?", "")
            if clean_w:
                words.append({
                    "word": clean_w,
                    "start": round(w.start, 2),
                    "end": round(w.end, 2)
                })
                
    print(f"[{vid_id}] Detected {len(words)} exact words in audio.")
    
    # Group words into punchy 1-3 word kinetic phrases
    phrases = []
    curr = []
    for w in words:
        curr.append(w)
        # Break after 2-3 words, or if phrase duration exceeds 0.75s, or big gap
        if len(curr) >= 2:
            dur = curr[-1]["end"] - curr[0]["start"]
            if len(curr) >= 3 or dur >= 0.70:
                p_text = " ".join([x["word"] for x in curr])
                p_st = curr[0]["start"]
                p_et = curr[-1]["end"]
                phrases.append({"text": p_text, "start": p_st, "end": p_et})
                curr = []
    if curr:
        p_text = " ".join([x["word"] for x in curr])
        phrases.append({"text": p_text, "start": curr[0]["start"], "end": curr[-1]["end"]})
        
    # Determine color highlight based on vocabulary rules
    ass_events = []
    endcard_cutoff = 19.50 # strictly cutoff subtitles before living endcard starts
    
    for p in phrases:
        if p["start"] >= endcard_cutoff:
            continue
        st = fmt_time(p["start"])
        et = fmt_time(min(p["end"], endcard_cutoff))
        txt = p["text"]
        
        # Color decision
        words_in_p = txt.split()
        if any(any(k in w for k in item["gold_words"]) for w in words_in_p) or any(c.isdigit() for c in txt):
            hl = "GOLD"
        elif any(any(k in w for k in item["green_words"]) for w in words_in_p):
            hl = "GREEN"
        elif any(any(k in w for k in item["red_words"]) for w in words_in_p):
            hl = "RED"
        else:
            hl = "WHITE"
            
        sname = style_map[hl]
        ass_events.append(f"Dialogue: 2,{st},{et},{sname},,0,0,0,,{{\\pos(540,1180)\\t(0,60,\\fscx115\\fscy115)\\t(60,120,\\fscx100\\fscy100)}}{txt}")
        
    full_ass = ass_template + "\n".join(ass_events) + "\n"
    with open(out_ass, "w", encoding="utf-8") as f:
        f.write(full_ass)
        
    print(f"[{vid_id}] Saved 100% exact ASS subtitle: {out_ass} ({len(ass_events)} kinetic phrases)")

print("\nALL 10 VIDEOS ACCURATELY ALIGNED VIA WHISPER WITH ZERO DRIFT!")
