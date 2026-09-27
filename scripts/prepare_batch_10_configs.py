import os
import json
import base64
import wave
import subprocess
import time
import urllib.request

API_KEY = os.environ.get("GEMINI_API_KEY", "")

VIDEOS_CONFIG = [
    # --- STEAL A SEED (5 Videos: 14 to 18) ---
    {
        "campaign": "steal_a_seed",
        "vid_id": "14_steal_a_seed_50k_speed_sonic_sprint",
        "title": "Steal a Seed Video 14 (50,000 Speed Sonic Sprint vs Base Lasers)",
        "script": (
            "This is what happens when you train up to fifty thousand speed in Steal a Seed! "
            "At level one, you're a slow turtle crawling through base laser traps. "
            "Until you grind the gym treadmills, stack lightning multipliers, and ignite a purple particle trail! "
            "Now you can blitz past defending players, dodge every single trap, and snatch the heaviest golden seeds! "
            "Can your friends catch you? Game is called Steal a Seed on Roblox, link in bio!"
        ),
        "segments": [
            ("shared/hooks/INTRO.mp4", 0.00, 1.40, "intro_clip"),
            ("campaigns/steal_a_seed/assets/clips/31_Clip 31.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/27_Clip 27.mp4", 0.00, 3.70, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/24_Clip 24.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/31_Clip 31.mp4", 4.00, 4.20, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/36_Clip 36.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/31_Clip 31.mp4", 8.00, 3.80, "endcard_anim"),
        ],
        "game_title": "STEAL A SEED",
        "brand_card": "campaigns/steal_a_seed/assets/branding/game_icon.png"
    },
    {
        "campaign": "steal_a_seed",
        "vid_id": "15_steal_a_seed_pro_heist_infiltration",
        "title": "Steal a Seed Video 15 (How to Steal Seeds from Max Level Players Without Dying)",
        "script": (
            "How to steal the rarest seeds from max level players without ever getting caught! "
            "Pro bases are surrounded by high-tech security, deadly lasers, and giant guard plants. "
            "The secret is timing the guard patrol, slipping through the side border, and grabbing the mega seed! "
            "Sprint back across the safe line before the base owner respawns, plant it in your garden, and print millions! "
            "Are you brave enough to heist? Game is called Steal a Seed on Roblox, link in bio!"
        ),
        "segments": [
            ("shared/hooks/INTRO.mp4", 0.00, 1.40, "intro_clip"),
            ("campaigns/steal_a_seed/assets/clips/10_Clip 10.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/27_Clip 27.mp4", 3.00, 3.70, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/14_Clip 14.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/18_Clip 18.mp4", 0.00, 4.00, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/33_Clip 33.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/29_Clip 29.mp4", 0.00, 3.80, "endcard_anim"),
        ],
        "game_title": "STEAL A SEED",
        "brand_card": "campaigns/steal_a_seed/assets/branding/game_icon.png"
    },
    {
        "campaign": "steal_a_seed",
        "vid_id": "16_steal_a_seed_secret_codes_millionaire",
        "title": "Steal a Seed Video 16 (The 3 Secret Working Codes That Broke Steal a Seed)",
        "script": (
            "These three secret working codes in Steal a Seed will make you an instant millionaire! "
            "Grinding from zero cash takes hours if you don't know the developer gifts. "
            "Type ADMINABUSE for two hundred free gems, FREEZING for a rare vine seed, and thirty-five k likes for two hundred fifty thousand cash! "
            "Spend that cash on max speed treadmills and watch your character break the sound barrier! "
            "Claim them before they expire! Game is called Steal a Seed on Roblox, link in bio!"
        ),
        "segments": [
            ("shared/hooks/INTRO.mp4", 0.00, 1.40, "intro_clip"),
            ("campaigns/steal_a_seed/assets/clips/04_Clip 4.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/09_Clip 9.mp4", 0.00, 3.70, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/04_Clip 4.mp4", 4.00, 4.00, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/24_Clip 24.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/31_Clip 31.mp4", 0.00, 4.00, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/31_Clip 31.mp4", 5.00, 3.80, "endcard_anim"),
        ],
        "game_title": "STEAL A SEED",
        "brand_card": "campaigns/steal_a_seed/assets/branding/game_icon.png"
    },
    {
        "campaign": "steal_a_seed",
        "vid_id": "17_steal_a_seed_level_1_vs_automated_fortress",
        "title": "Steal a Seed Video 17 (Level 1 Beginner Garden vs Level 100 Automated Seed Fortress)",
        "script": (
            "Level one beginner garden versus level one hundred automated seed fortress! "
            "At level one, you only have a sad patch of dirt and one tiny seedling. "
            "At level one hundred, you unlock automated laser turrets, multi-tiered gardens, and legendary plants! "
            "Every harvest automatically generates millions of cash while you sprint across the map stealing more! "
            "What level is your garden? Game is called Steal a Seed on Roblox, link in bio!"
        ),
        "segments": [
            ("shared/hooks/INTRO.mp4", 0.00, 1.40, "intro_clip"),
            ("campaigns/steal_a_seed/assets/clips/01_Clip 1.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/07_Clip 7.mp4", 0.00, 3.70, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/23_Clip 23.mp4", 0.00, 4.20, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/27_Clip 27.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/36_Clip 36.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/36_Clip 36.mp4", 4.00, 3.80, "endcard_anim"),
        ],
        "game_title": "STEAL A SEED",
        "brand_card": "campaigns/steal_a_seed/assets/branding/game_icon.png"
    },
    {
        "campaign": "steal_a_seed",
        "vid_id": "18_steal_a_seed_mythic_heavy_seed_heist",
        "title": "Steal a Seed Video 18 (I Stole the Heaviest Mythic Seed in Roblox)",
        "script": (
            "I broke into the forbidden zone and stole the heaviest mythic seed in Roblox! "
            "This seed weighs eleven kilograms and cuts your sprint speed in half while carrying it! "
            "You have to jump through desert spikes, outrun armed defenders, and sprint to the border! "
            "Plant it down and it generates fifty thousand cash every single second! "
            "Could you carry this seed? Game is called Steal a Seed on Roblox, link in bio!"
        ),
        "segments": [
            ("shared/hooks/INTRO.mp4", 0.00, 1.40, "intro_clip"),
            ("campaigns/steal_a_seed/assets/clips/15_Clip 15.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/26_Clip 26.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/28_Clip 28.mp4", 0.00, 4.00, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/36_Clip 36.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/31_Clip 31.mp4", 0.00, 3.90, "blurred_bg"),
            ("campaigns/steal_a_seed/assets/clips/36_Clip 36.mp4", 4.00, 3.80, "endcard_anim"),
        ],
        "game_title": "STEAL A SEED",
        "brand_card": "campaigns/steal_a_seed/assets/branding/game_icon.png"
    },

    # --- ROLL ANIME GIRLS (3 Videos: 02, 03, 04) ---
    {
        "campaign": "roll_anime_girls",
        "vid_id": "02_roll_anime_girls_one_in_three_billion_mythic",
        "title": "Roll Anime Girls Video 02 (From 1 in 10 Common to 1 in 3 Billion Mythic Hu Tao)",
        "script": (
            "I started with a common character and tried to roll the one in three billion Mythic Hu Tao! "
            "At the start, your luck is so low you only pull one in nineteen commons. "
            "Until you visit the potion witch, chug luck boosters, and activate auto roll! "
            "The screen flashes gold, a divine anime girl drops, and your plot starts printing passive millions! "
            "Can you beat my luck? Game is called Roll Anime Girls on Roblox, link in bio!"
        ),
        "segments": [
            ("shared/hooks/INTRO.mp4", 0.00, 1.40, "intro_clip"),
            ("campaigns/roll_anime_girls/assets/clips/03_Clip 3.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/roll_anime_girls/assets/clips/06_Clip 6.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/roll_anime_girls/assets/clips/01_Clip 1.mp4", 0.00, 4.00, "blurred_bg"),
            ("campaigns/roll_anime_girls/assets/clips/14_Clip 14.mp4", 0.00, 4.00, "blurred_bg"),
            ("campaigns/roll_anime_girls/assets/clips/28_Clip 28.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/roll_anime_girls/assets/clips/01_Clip 1.mp4", 2.00, 3.80, "endcard_anim"),
        ],
        "game_title": "ROLL ANIME GIRLS",
        "brand_card": "campaigns/roll_anime_girls/assets/branding/000.png"
    },
    {
        "campaign": "roll_anime_girls",
        "vid_id": "03_roll_anime_girls_afk_passive_millions_tycoon",
        "title": "Roll Anime Girls Video 03 (How to Make Passive Billions While Completely AFK in Roblox)",
        "script": (
            "This Roblox RNG game literally prints money for you even while you are completely offline! "
            "You start on an empty plot with zero cash, but every anime girl you roll earns passive income. "
            "Place them on your base, equip companions to boost production, and upgrade your plot multipliers! "
            "Go to sleep, log back in, and collect millions of cash ready for your next rebirth! "
            "Start building your empire! Game is called Roll Anime Girls on Roblox, link in bio!"
        ),
        "segments": [
            ("shared/hooks/INTRO.mp4", 0.00, 1.40, "intro_clip"),
            ("campaigns/roll_anime_girls/assets/clips/10_Clip 10.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/roll_anime_girls/assets/clips/13_Clip 13.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/roll_anime_girls/assets/clips/27_Clip 27.mp4", 0.00, 4.00, "blurred_bg"),
            ("campaigns/roll_anime_girls/assets/clips/36_Clip 36.mp4", 0.00, 4.00, "blurred_bg"),
            ("campaigns/roll_anime_girls/assets/clips/14_Clip 14.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/roll_anime_girls/assets/clips/36_Clip 36.mp4", 2.00, 3.80, "endcard_anim"),
        ],
        "game_title": "ROLL ANIME GIRLS",
        "brand_card": "campaigns/roll_anime_girls/assets/branding/000.png"
    },
    {
        "campaign": "roll_anime_girls",
        "vid_id": "04_roll_anime_girls_rebirth_secret_multipliers",
        "title": "Roll Anime Girls Video 04 (The Rebirth Secret Nobody Tells You in Roll Anime Girls)",
        "script": (
            "The biggest mistake everyone makes in Roll Anime Girls is forgetting to rebirth! "
            "Rebirthing resets your base, so most beginner players are terrified to press the button. "
            "But every rebirth grants permanent luck multipliers and unlocks secret high-tier roll tables! "
            "You climb back up ten times faster, unlocking divine characters in just a few rolls! "
            "How many times have you rebirthed? Game is called Roll Anime Girls on Roblox, link in bio!"
        ),
        "segments": [
            ("shared/hooks/INTRO.mp4", 0.00, 1.40, "intro_clip"),
            ("campaigns/roll_anime_girls/assets/clips/02_Clip 2.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/roll_anime_girls/assets/clips/24_Clip 24.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/roll_anime_girls/assets/clips/31_Clip 31.mp4", 0.00, 4.00, "blurred_bg"),
            ("campaigns/roll_anime_girls/assets/clips/44_Clip 44.mp4", 0.00, 4.00, "blurred_bg"),
            ("campaigns/roll_anime_girls/assets/clips/18_Clip 18.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/roll_anime_girls/assets/clips/44_Clip 44.mp4", 2.00, 3.80, "endcard_anim"),
        ],
        "game_title": "ROLL ANIME GIRLS",
        "brand_card": "campaigns/roll_anime_girls/assets/branding/000.png"
    },

    # --- ASMR DOMINOES (2 Videos: 07, 08) ---
    {
        "campaign": "asmr_dominoes",
        "vid_id": "07_asmr_dominoes_mammoth_43_stud_lava_wall",
        "title": "ASMR Dominoes Video 07 (The 3-Second Mammoth Domino Wall Challenge)",
        "script": (
            "This is what happens when you build a mammoth forty-three stud domino wall in Roblox! "
            "Placing giant dominoes one by one is impossible, but the drag brush spawns hundreds in three seconds. "
            "Crank the size slider to maximum mammoth height and equip the glowing molten lava skin! "
            "Hit topple mode, and watch towering volcanic pillars collapse in a massive fiery cascade! "
            "Most satisfying sound ever! Game is called ASMR Dominoes on Roblox, link in bio!"
        ),
        "segments": [
            ("shared/hooks/INTRO.mp4", 0.00, 1.40, "intro_clip"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_3s_build.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_Lava_topple.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_Topple_Crunch.mp4", 0.00, 4.00, "blurred_bg"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_Lava_topple.mp4", 5.00, 4.00, "blurred_bg"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_BlackHole.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_BlackHole.mp4", 12.00, 3.80, "endcard_anim"),
        ],
        "game_title": "ASMR DOMINOES",
        "brand_card": "campaigns/asmr_dominoes/assets/branding/000.png"
    },
    {
        "campaign": "asmr_dominoes",
        "vid_id": "08_asmr_dominoes_infinite_hypnotic_bubble_loop",
        "title": "ASMR Dominoes Video 08 (The Impossible Infinite Domino Loop - Most Relaxing ASMR)",
        "script": (
            "If you need instant stress relief, this infinite bubble domino loop is pure magic! "
            "Normal dominoes just click, but this secret skin bursts rainbow soap bubbles on every hit. "
            "Form a giant spiral track, equip custom whisper pop sounds, and trigger the chain reaction! "
            "Thousands of iridescent bubbles float into the sky before a cosmic black hole singularity swallows them whole! "
            "Put on headphones for this! Game is called ASMR Dominoes on Roblox, link in bio!"
        ),
        "segments": [
            ("shared/hooks/INTRO.mp4", 0.00, 1.40, "intro_clip"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_Bubbles.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_Spiral.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_Short_Chain.mp4", 0.00, 4.00, "blurred_bg"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_Sounds_Showcase.mp4", 0.00, 4.00, "blurred_bg"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_BlackHole.mp4", 0.00, 3.80, "blurred_bg"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_BlackHole.mp4", 12.00, 3.80, "endcard_anim"),
        ],
        "game_title": "ASMR DOMINOES",
        "brand_card": "campaigns/asmr_dominoes/assets/branding/000.png"
    }
]

def main():
    print(f"Total videos to batch produce: {len(VIDEOS_CONFIG)}")
    with open("temp/batch_10_config.json", "w", encoding="utf-8") as f:
        json.dump(VIDEOS_CONFIG, f, indent=2)
    print("Saved configuration to temp/batch_10_config.json")

if __name__ == "__main__":
    os.makedirs("temp", exist_ok=True)
    main()
