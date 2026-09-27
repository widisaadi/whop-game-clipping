import os
import math
from PIL import Image, ImageDraw, ImageFont

def get_font(size, font_name="impact.ttf"):
    font_path = os.path.join("C:/Windows/Fonts", font_name)
    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            pass
    return ImageFont.load_default()

def create_glass_card(img_path, target_w=680, radius=28, border_w=4):
    img = Image.open(img_path).convert("RGBA")
    aspect = img.height / img.width
    target_h = int(target_w * aspect)
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    ss = 4
    mask = Image.new("L", (target_w * ss, target_h * ss), 0)
    draw_m = ImageDraw.Draw(mask)
    draw_m.rounded_rectangle((0, 0, target_w * ss, target_h * ss), radius=radius * ss, fill=255)
    mask = mask.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    card_w = target_w + border_w * 2
    card_h = target_h + border_w * 2
    card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    
    bmask = Image.new("L", (card_w * ss, card_h * ss), 0)
    draw_b = ImageDraw.Draw(bmask)
    draw_b.rounded_rectangle((0, 0, card_w * ss, card_h * ss), radius=(radius + border_w) * ss, fill=255)
    bmask = bmask.resize((card_w, card_h), Image.Resampling.LANCZOS)
    
    border_layer = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    draw_border = ImageDraw.Draw(border_layer)
    for y in range(card_h):
        ratio = y / card_h
        r = int(0 * (1 - ratio) + 220 * ratio)
        g = int(220 * (1 - ratio) + 80 * ratio)
        b = int(255 * (1 - ratio) + 255 * ratio)
        draw_border.line([(0, y), (card_w, y)], fill=(r, g, b, 245))
        
    card.paste(border_layer, (0, 0), mask=bmask)
    
    glare = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw_g = ImageDraw.Draw(glare)
    pts = [(0, 0), (int(target_w * 0.70), 0), (int(target_w * 0.25), target_h), (0, target_h)]
    draw_g.polygon(pts, fill=(255, 255, 255, 35))
    
    img_with_glare = Image.alpha_composite(img, glare)
    card.paste(img_with_glare, (border_w, border_w), mask=mask)
    return card

def draw_text_with_outline(draw, pos, text, font, fill_color, outline_color, outline_w):
    x, y = pos
    for ox in range(-outline_w, outline_w + 1):
        for oy in range(-outline_w, outline_w + 1):
            if ox * ox + oy * oy <= outline_w * outline_w:
                draw.text((x + ox, y + oy), text, font=font, fill=outline_color)
    draw.text((x, y), text, font=font, fill=fill_color)

def generate_campaign_endcard(camp_name, title_text, brand_img_path, out_dir, duration=4.50, fps=30):
    os.makedirs(out_dir, exist_ok=True)
    num_frames = int(fps * duration)
    
    # Check if frames already exist
    existing = [f for f in os.listdir(out_dir) if f.endswith(".png")]
    if len(existing) >= num_frames:
        print(f"[{camp_name}] Endcard frames already exist ({len(existing)} frames). Skipping.")
        return
        
    print(f"[{camp_name}] Generating {num_frames} living endcard frames in {out_dir}...")
    W, H = 1080, 1920
    center_x = W // 2
    
    font_title = get_font(98, "impact.ttf")
    font_cta = get_font(96, "impact.ttf")
    
    tbox = font_title.getbbox(title_text)
    tw, th = tbox[2] - tbox[0], tbox[3] - tbox[1]
    
    target_card_w = max(tw, 680)
    card_base = create_glass_card(brand_img_path, target_w=target_card_w, radius=30, border_w=4)
    cw, ch = card_base.size
    
    cta_text = "LINK IN BIO"
    bbox_cta = font_cta.getbbox(cta_text)
    ctaw, ctah = bbox_cta[2] - bbox_cta[0], bbox_cta[3] - bbox_cta[1]
    
    for f in range(num_frames):
        t = f / fps
        if t < 0.35:
            progress = t / 0.35
            scale_factor = 0.6 + 0.4 * math.sin(progress * (math.pi / 2))
        else:
            scale_factor = 1.0 + 0.012 * math.sin((t - 0.35) * 2.4)
            
        float_y = 5 * math.sin(t * 2.8)
        frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        
        # 3. CTA at baseline Y = 1180
        cta_x = center_x - ctaw // 2
        cta_y = int(1180 + float_y)
        
        # 2. Card placed 24px above CTA
        card_scaled_w = int(cw * scale_factor)
        card_scaled_h = int(ch * scale_factor)
        card_scaled = card_base.resize((card_scaled_w, card_scaled_h), Image.Resampling.LANCZOS)
        card_x = center_x - card_scaled_w // 2
        card_y = cta_y - 24 - card_scaled_h
        
        # Shadow
        shadow_w = int(card_scaled_w * 0.92)
        shadow_h = int(card_scaled_h * 0.12)
        shadow = Image.new("RGBA", (shadow_w, shadow_h), (0, 0, 0, 0))
        draw_s = ImageDraw.Draw(shadow)
        draw_s.ellipse((0, 0, shadow_w, shadow_h), fill=(0, 0, 0, 95))
        frame.paste(shadow, (center_x - shadow_w // 2, card_y + card_scaled_h - 10), mask=shadow)
        
        frame.paste(card_scaled, (card_x, card_y), mask=card_scaled)
        
        # 1. Judul Game placed 24px directly above the Card
        title_x = center_x - tw // 2
        title_y = card_y - 24 - th
        
        draw_text_with_outline(
            draw, (title_x, title_y), title_text, font_title,
            fill_color=(255, 225, 0, 255), outline_color=(0, 0, 0, 255), outline_w=8
        )
        draw_text_with_outline(
            draw, (cta_x, cta_y), cta_text, font_cta,
            fill_color=(255, 255, 255, 255), outline_color=(0, 0, 0, 255), outline_w=8
        )
        
        frame.save(os.path.join(out_dir, f"frame_{f:04d}.png"), "PNG")
    print(f"[{camp_name}] Finished {num_frames} frames.")

def main():
    CAMPAIGNS = [
        ("steal_a_seed", "STEAL A SEED", "campaigns/steal_a_seed/assets/branding/game_icon.png", "temp/steal_a_seed/endcard_frames"),
        ("roll_anime_girls", "ROLL ANIME GIRLS", "campaigns/roll_anime_girls/assets/branding/000.png", "temp/roll_anime_girls/endcard_frames"),
        ("asmr_dominoes", "ASMR DOMINOES", "campaigns/asmr_dominoes/assets/branding/000.png", "temp/asmr_dominoes/endcard_frames_01"),
    ]
    for camp, title, img, out in CAMPAIGNS:
        generate_campaign_endcard(camp, title, img, out)

if __name__ == "__main__":
    main()
