import json
import os

CATALOG_PATH = "campaigns/roll_anime_girls/guide/footage_catalog.json"

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Semantic classifications based on visual review
descriptions = {
    "01_Clip 1.mp4": {
        "mechanic": "dice_rolling",
        "description": "Rolling dice for anime girls: shows Auto Roll, Skip, pulls Mythic Hu Tao (1 in 3.17B), Epic Cirno (1 in 200k), and Common Aries (1 in 19).",
        "key_elements": ["Mythic Hu Tao 1 in 3.17B", "Epic Cirno", "Common Aries", "Auto Roll UI"],
        "recommended_beat": "Beat 1 (Velocity Hook) / Beat 3 (Absurd Tool)"
    },
    "02_Clip 2.mp4": {
        "mechanic": "dice_rolling",
        "description": "High-speed rolling sequence with glowing character reveals and rarity titles.",
        "key_elements": ["Dice rolling", "Aura effects", "Character reveals"],
        "recommended_beat": "Beat 3 (The Absurd Tool / Rolling Loop)"
    },
    "03_Clip 3.mp4": {
        "mechanic": "dice_rolling",
        "description": "Continuous rolling in daytime hub, unlocking anime characters with rarity odds.",
        "key_elements": ["Roll animations", "Rarity tags", "RNG odds"],
        "recommended_beat": "Beat 3 (The Absurd Tool / Rolling Loop)"
    },
    "04_Clip 4.mp4": {
        "mechanic": "dice_rolling",
        "description": "Rolling dice animation, showing character pull reveal and inventory counter.",
        "key_elements": ["Dice roll", "Character summon", "Inventory"],
        "recommended_beat": "Beat 3 (Rolling Loop)"
    },
    "05_Clip 5.mp4": {
        "mechanic": "plot_tycoon_building",
        "description": "Placing Toby (Common, $3.45/s) and Lily (Uncommon, $18/s) on plot pads. Shows 'you earn $529.45K per hour offline!' and cash ticking up to $221.84K.",
        "key_elements": ["Plot placement", "Money generation $/s", "Offline earnings display", "Cash ticking up"],
        "recommended_beat": "Beat 2 (Core Constraint / Tycoon Base) / Beat 3 (Passive Income)"
    },
    "06_Clip 6.mp4": {
        "mechanic": "plot_tycoon_building",
        "description": "Base expansion with multiple pads filled with anime girls generating passive income.",
        "key_elements": ["Tycoon base", "Passive income", "Multiple pads"],
        "recommended_beat": "Beat 3 / Beat 4 (Progression Loop)"
    },
    "07_Clip 7.mp4": {
        "mechanic": "plot_tycoon_building",
        "description": "Walking across expanded plot pads collecting cash and managing anime girl characters.",
        "key_elements": ["Plot walking", "Cash collection", "Base expansion"],
        "recommended_beat": "Beat 4 (Progression Escalation)"
    },
    "08_Clip 8.mp4": {
        "mechanic": "plot_tycoon_building",
        "description": "Plot overview showing multiple anime girls generating passive dollars per second.",
        "key_elements": ["Passive money gen", "Pad layout", "Tycoon progression"],
        "recommended_beat": "Beat 3 / Beat 4 (Progression)"
    },
    "09_Clip 9.mp4": {
        "mechanic": "plot_tycoon_building",
        "description": "Detailed plot management, upgrading pads and checking character stats.",
        "key_elements": ["Base management", "Character stats", "Income upgrades"],
        "recommended_beat": "Beat 4 (Progression Escalation)"
    },
    "10_Clip 10.mp4": {
        "mechanic": "index_discovery",
        "description": "Complete Index menu showcase with 200+ anime girls categorized across weather types (Normal, Rainy, Holy, Lunar, GLITCHED, BlackFlash) and insane rarities up to 1 in 2 Trillion.",
        "key_elements": ["Index menu 200+ characters", "Weather categories", "Rarities up to 1 in 2T"],
        "recommended_beat": "Beat 1 (Discovery Hook) / Beat 4 (Progression)"
    },
    "19_Clip 19.mp4": {
        "mechanic": "companion_follower",
        "description": "Inspecting anime girls on plot and setting companion follower with stat boosts.",
        "key_elements": ["Companion following", "Stat boost UI", "Plot pads"],
        "recommended_beat": "Beat 3 (Follower Mechanic)"
    },
    "20_Clip 20.mp4": {
        "mechanic": "companion_follower_and_income",
        "description": "Advanced plot at Night weather: Borisov Rare (320/s), 'you earn $1.38M per hour offline!', 'On follow: +1.5% Luck, +1.5% Money', cash at $952.3K.",
        "key_elements": ["Night weather", "320/s generation", "$1.38M offline income", "+1.5% Luck & Money follow boost"],
        "recommended_beat": "Beat 4 (Progression & Multipliers Escalation)"
    },
    "25_Clip 25.mp4": {
        "mechanic": "rebirth_system",
        "description": "Full Rebirth menu: $1.02M / $1M threshold reached, clicking Rebirth button to gain x1.5 luck multiplier, Bubblegum Dice, and Extra Slot, unlocking next tier ($2.75M for x2 multiplier).",
        "key_elements": ["Rebirth button click", "x1.5 Luck multiplier", "Bubblegum Dice reward", "Cash reset from $1.02M to $0"],
        "recommended_beat": "Beat 4 (Multipliers Escalation & Rebirth)"
    },
    "28_Clip 28.mp4": {
        "mechanic": "potions_shop",
        "description": "Visiting the Potions stall in the central town hub to buy luck potions and booster drinks.",
        "key_elements": ["Potions stall", "Town hub", "Luck potions"],
        "recommended_beat": "Beat 3 (Absurd Tool / Luck Booster)"
    },
    "30_Clip 30.mp4": {
        "mechanic": "peak_endgame_base",
        "description": "God-tier endgame base: Divine pedestals with Luffy Divine (+156.248% boost) and Astolfo Divine (+62.498% boost), glowing particle auras and capes.",
        "key_elements": ["Luffy Divine", "Astolfo Divine", "Pedestals & Auras", "Endgame flex"],
        "recommended_beat": "Beat 5 (Peak Superpower Tease & Living Endcard)"
    },
    "40_Clip 40.mp4": {
        "mechanic": "insane_rng_rolls",
        "description": "Rainy weather rolling: pulling Glitched Mythic Denji (1 in 327 BILLION) and Sakura Varesa (1 in 625 QUADRILLION / 1 in 625,083,701,529,511,200).",
        "key_elements": ["Glitched Mythic Denji 1 in 327B", "Sakura Varesa 1 in 625 Quadrillion", "Rainy Weather rolling"],
        "recommended_beat": "Beat 1 (Velocity Hook) / Beat 4 (Multipliers Escalation)"
    },
    "48_Clip 48.mp4": {
        "mechanic": "town_hub_and_followers",
        "description": "Running through town past Sell stall, Potion Witch stall, accompanied by giant glowing follower companions Luffy Divine and Astolfo Divine.",
        "key_elements": ["Potion Witch stall", "Hub running", "Luffy Divine companion", "Astolfo Divine companion"],
        "recommended_beat": "Beat 3 / Beat 4 (Followers & Potions)"
    },
    "50_Clip 50.mp4": {
        "mechanic": "plot_placement_and_income",
        "description": "Placing Penelope Rare ($2.2K/s) on pad, cash jumps from $20.87K to $27.25K, demonstrating exact tycoon placement and passive cash generation.",
        "key_elements": ["Penelope Rare 2.2K/s", "Cash jumping to $27.25K", "Pad placement"],
        "recommended_beat": "Beat 2 (Base Building) / Beat 3 (Gameplay Loop)"
    }
}

for k, v in catalog.items():
    if k in descriptions:
        v.update(descriptions[k])
    else:
        # Generic classification for remaining clips
        if "Clip" in k:
            num = int(k.split("_")[0])
            if num <= 4:
                v["mechanic"] = "dice_rolling"
                v["description"] = f"Dice rolling sequence showing anime character summons."
                v["recommended_beat"] = "Beat 3 (Rolling Loop)"
            elif 5 <= num <= 24:
                v["mechanic"] = "plot_tycoon_building"
                v["description"] = f"Plot base building and passive money generation ($/s) with anime girls."
                v["recommended_beat"] = "Beat 2 / Beat 3"
            elif 25 <= num <= 27:
                v["mechanic"] = "rebirth_and_progression"
                v["description"] = f"Rebirth progression and multipliers upgrading."
                v["recommended_beat"] = "Beat 4 (Progression Escalation)"
            elif 28 <= num <= 29:
                v["mechanic"] = "potions_and_shop"
                v["description"] = f"Central town hub with Potion Witch stall and luck upgrades."
                v["recommended_beat"] = "Beat 3 (Potions & Luck)"
            elif 30 <= num <= 38:
                v["mechanic"] = "peak_endgame_base"
                v["description"] = f"Endgame tycoon base with Divine tier anime characters and massive particle auras."
                v["recommended_beat"] = "Beat 5 (Peak Superpower Tease)"
            elif 39 <= num <= 47:
                v["mechanic"] = "insane_rng_rolls"
                v["description"] = f"Rolling rare, epic, and mythic anime girls during special weather events."
                v["recommended_beat"] = "Beat 1 / Beat 4"
            else:
                v["mechanic"] = "gameplay_overview"
                v["description"] = f"General gameplay showing plot, character followers, and passive income."
                v["recommended_beat"] = "Beat 2 / Beat 3"

with open(CATALOG_PATH, "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2)

print(f"Catalog successfully enriched with semantic descriptions: {CATALOG_PATH}")
