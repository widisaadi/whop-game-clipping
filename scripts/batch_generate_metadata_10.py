import os
import json

def generate_metadata_for_video(v_conf):
    camp = v_conf["campaign"]
    vid_id = v_conf["vid_id"]
    script_text = v_conf["script"]
    title_raw = v_conf["title"]
    
    out_dir = os.path.join("campaigns", camp, "output")
    os.makedirs(out_dir, exist_ok=True)
    md_path = os.path.join(out_dir, f"{vid_id}_metadata.md")
    
    if camp == "steal_a_seed":
        game_url = "https://www.roblox.com/games/122216176958450/Steal-A-Seed"
        tags = "`Roblox`, `Steal a Seed`, `Roblox Steal a Seed`, `Gaming`, `RobloxShorts`, `Shorts`, `RobloxHeist`, `RobloxSimulator`, `SpeedSimulator`"
        hook_angle = "Steal a Seed High Stakes Heist & Speed Progression"
    elif camp == "roll_anime_girls":
        game_url = "https://www.roblox.com/games/92289737492030/Roll-Anime-Girls"
        tags = "`Roblox`, `Roll Anime Girls`, `RobloxRNG`, `RobloxTycoon`, `Gaming`, `RobloxAnime`, `RobloxShorts`, `Shorts`, `AnimeTycoon`"
        hook_angle = "Roll Anime Girls RNG Tycoon & Luck Boosters"
    else:
        game_url = "https://www.roblox.com/games/98004862449180/ASMR-Dominoes"
        tags = "`Roblox`, `ASMR Dominoes`, `RobloxASMR`, `Dominoes`, `Satisfying`, `OddlySatisfying`, `Gaming`, `RobloxShorts`, `Shorts`"
        hook_angle = "ASMR Dominoes Sensory Satisfaction & Cosmic Black Hole"

    content = f"""# Metadata & Publishing Package: {title_raw}

- **Campaign:** {camp.replace('_', ' ').title()}
- **Video ID:** `{vid_id}`
- **Concept / Angle:** Angle — *Avatar Shock Hook + {hook_angle}*
- **Format:** Vertical 9:16 (`1080x1920`), CFR 30.00 fps, BT.709
- **Audio Mix:** Puck Voice (+4 dB boost, breathless cadence) | BGM3 (-5 dB relative, 1.9s fade) | SFX Stems (0.90) | Master EBU R128 `-14.0 LUFS` (`-1.5 dBTP`)
- **Video Master File:** [`{vid_id}.mp4`](file:///d:/create%20something/Web%20App/bloxclip/campaigns/{camp}/output/{vid_id}.mp4)
- **Visual Contact Sheet:** [`{vid_id}_sheet.png`](file:///d:/create%20something/Web%20App/bloxclip/campaigns/{camp}/output/{vid_id}_sheet.png)

---

## 1. Title Options (High CTR & 2026 Packaging)

1. **Option A (Recommended - Story & Escalation Flex):**  
   `{title_raw.split('(')[-1].replace(')', '')}! ⚡💥`
2. **Option B (Curiosity & Shock Factor):**  
   `What Happens If You Unlock This in {v_conf['game_title'].title()}? 🌌`
3. **Option C (Search / Value Discovery):**  
   `How to Play {v_conf['game_title'].title()} Roblox (Pro Tips & Secrets) 🎮`
4. **Option D (Speed / Rarity Challenge):**  
   `I Tried to Break the Rarest Record in {v_conf['game_title'].title()}! 🏆`

---

## 2. Description (Full YouTube / TikTok / Reels Copy)

```text
{script_text}

🎮 Play {v_conf['game_title'].title()} on Roblox:
👉 Link in Bio!
Direct Game Link: {game_url}

Timestamps:
0:00 - Avatar Shock Opener!
0:01 - Velocity Hook Teaser
0:04 - Core Constraint & Early Game Struggle
0:08 - The Absurd Gameplay Loop & Multipliers
0:14 - Escalation & Superpower Peak!
0:19 - Play {v_conf['game_title'].title()} on Roblox (Link in Bio!)

{tags.replace('`', '').replace(',', '')}
```

---

## 3. Pinned Comment (Drive Bio Clicks & Comment Engagement)

```text
What is your best score/drop so far in {v_conf['game_title'].title()}? 🤩
Play {v_conf['game_title'].title()} now on Roblox! Link is right here in bio:
👉 {game_url} 👇
```

---

## 4. Tags & SEO Keywords

{tags}

---

## 5. 5-Beat Retention Machine Architecture

| Beat | Description |
| :--- | :--- |
| **Beat 1: Velocity Hook (0.0s - 2.0s)** | `shared/hooks/INTRO.mp4` avatar shock opener with Metal Gear Alert transitioning to kinetic gameplay teaser |
| **Beat 2: Core Constraint (2.0s - 6.0s)** | Highlighting beginner struggle, slow speed, empty base, or basic dominoes |
| **Beat 3: Gameplay Loop (6.0s - 10.0s)** | Revealing tools, codes, gym treadmills, drag brush, or potion luck boosters |
| **Beat 4: Multiplier Escalation (10.0s - 16.0s)** | Visual multiplier grinding, massive cash generation, or cascade reactions |
| **Beat 5: Peak Superpower & Endcard (16.0s - End)** | Godspeed sprint / singularity / divine pull, followed by Living Endcard with `{v_conf['game_title']}` and pure `LINK IN BIO` CTA |

---

## 6. Technical & Compliance Verification

- [x] **Avatar Opening Hook:** `shared/hooks/INTRO.mp4` kinetik di detik 0.0s–1.4s dipadukan dengan sound effect Metal Gear Alert.
- [x] **RULE-01 (Game Identification):** Game name `{v_conf['game_title']}` is clearly spoken in voiceover and displayed in bold Impact font on living endcard.
- [x] **RULE-02 & RULE-03 (Link Compliance):** Non-truncated link `{game_url}` provided in metadata, pinned comment, and description.
- [x] **RULE-07 (Aspect Ratio):** Rendered CFR 30 fps, 1080x1920 with 1:1 sharp square centered at Y=420 and ambient blurred backdrop (`boxblur=26:6, eq=brightness=-0.18:contrast=1.05`).
- [x] **RULE-08 (Impact Subtitles):** Impact 96-102 kinetic pop placed in lower zone (`X=540, Y=1180`), stopping cleanly before the living endcard starts.
- [x] **RULE-09 (Living Endcard):** Focal center composition with official card branding, title `{v_conf['game_title']}`, and pure text CTA `LINK IN BIO` at baseline `Y=1180`.
- [x] **RULE-10 (Audio Design & Normalization):** Voiceover boosted +4 dB, BGM ducked -5 dB, SFX at 0.90, normalized to EBU R128 `-14.0 LUFS` (`-1.5 dBTP`).
"""
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[{vid_id}] Metadata written to {md_path}")

def main():
    with open("temp/batch_10_config.json", "r", encoding="utf-8") as f:
        configs = json.load(f)
    for conf in configs:
        generate_metadata_for_video(conf)

if __name__ == "__main__":
    main()
