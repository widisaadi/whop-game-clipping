import os
import shutil

def safe_copy(src, dst):
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        print(f"Copied: {src} -> {dst}")
    else:
        print(f"Warning: Source not found: {src}")

def safe_move(src, dst):
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)
        print(f"Moved: {src} -> {dst}")
    else:
        print(f"Warning: Source not found: {src}")

def main():
    print("=== STARTING WORKSPACE REORGANIZATION ===")
    
    # 1. Output Final Delivery
    final_files = [
        "output/how_to_fisch_island_expedition.mp4",
        "output/how_to_fisch_island_expedition_sheet.png",
        "output/how_to_fisch_weapons_raid.mp4",
        "output/how_to_fisch_weapons_raid_sheet.png"
    ]
    for f in final_files:
        if os.path.exists(f):
            dest = os.path.join("campaigns/how_to_fisch/output/final_delivery", os.path.basename(f))
            safe_copy(f, dest)

    # 2. Output Drafts Archive (Move older drafts)
    draft_files = [
        "output/how_to_fisch_01_v01.mp4",
        "output/how_to_fisch_01_v02.mp4",
        "output/how_to_fisch_bang_motion.mp4",
        "output/how_to_fisch_combat_bosses.mp4",
        "output/how_to_fisch_gemini_achird.mp4",
        "output/how_to_fisch_gemini_kore.mp4"
    ]
    for f in draft_files:
        if os.path.exists(f):
            dest = os.path.join("campaigns/how_to_fisch/output/drafts_archive", os.path.basename(f))
            safe_move(f, dest)

    # 3. Output QA Inspection Folders
    qa_dirs = [
        "output/qa_achird_frames",
        "output/qa_cinematic_frames",
        "output/qa_gemini_frames",
        "output/qa_v2_frames",
        "output/qa_v3_frames",
        "output/qa_v4_frames"
    ]
    for qd in qa_dirs:
        if os.path.exists(qd):
            dest = os.path.join("campaigns/how_to_fisch/output/qa_inspection", os.path.basename(qd))
            safe_move(qd, dest)

    # 4. Shared Hooks
    safe_copy("INTRO.mp4", "shared/hooks/INTRO.mp4")
    if os.path.exists("INTRO_sheet.png"):
        safe_copy("INTRO_sheet.png", "shared/hooks/INTRO_sheet.png")

    # 5. Shared SFX
    if os.path.exists("assets/sfx"):
        for item in os.listdir("assets/sfx"):
            src = os.path.join("assets/sfx", item)
            dst = os.path.join("shared/sfx", item)
            safe_copy(src, dst)

    # 6. Campaign Assets - Clips (38 raw footage clips)
    if os.path.exists("assets"):
        for f in os.listdir("assets"):
            if f.endswith(".mp4") and ("Clip" in f):
                src = os.path.join("assets", f)
                dst = os.path.join("campaigns/how_to_fisch/assets/clips", f)
                safe_copy(src, dst)

    # 7. Campaign Assets - Branding
    brand_assets = [
        "assets/how_to_fisch_official_icon.png",
        "assets/intro_badge.png",
        "assets/endcard.png",
        "assets/endcard_overlay.png"
    ]
    for b in brand_assets:
        if os.path.exists(b):
            dst = os.path.join("campaigns/how_to_fisch/assets/branding", os.path.basename(b))
            safe_copy(b, dst)

    # 8. Campaign Assets - Audio
    audio_assets = [
        "assets/bgm.mp3",
        "assets/voiceover_achird.mp3",
        "temp/voiceover_v5_tight.wav",
        "temp/voiceover_v6_tight.wav"
    ]
    for a in audio_assets:
        if os.path.exists(a):
            dst = os.path.join("campaigns/how_to_fisch/assets/audio", os.path.basename(a))
            safe_copy(a, dst)

    # 9. Campaign Subtitles
    if os.path.exists("subtitles"):
        for sub in os.listdir("subtitles"):
            if sub.endswith(".ass"):
                src = os.path.join("subtitles", sub)
                dst = os.path.join("campaigns/how_to_fisch/subtitles", sub)
                safe_copy(src, dst)

    print("\n=== WORKSPACE REORGANIZATION COMPLETE ===")

if __name__ == "__main__":
    main()
