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
        r = int(255 * (1 - ratio) + 0 * ratio)
        g = int(230 * (1 - ratio) + 255 * ratio)
        b = int(50 * (1 - ratio) + 120 * ratio)
        draw_border.line([(0, y), (card_w, y)], fill=(r, g, b, 245))
        
    card.paste(border_layer, (0, 0), mask=bmask)
    
    glare = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw_g = ImageDraw.Draw(glare)
    pts = [(0, 0), (int(target_w * 0.70), 0), (int(target_w * 0.25), target_h), (0, target_h)]
    draw_g.polygon(pts, fill=(255, 255, 255, 35))
    
    img_with_glare = Image.alpha_composite(img, glare)
    card.paste(img_with_glare, (border_w, border_w), mask=mask)
    return card

def create_endcard_frames(fps=30, duration=4.33):
    W, H = 1080, 1920
    center_x = W // 2
    frames_dir = "temp/steal_a_seed/endcard_frames_10"
    os.makedirs(frames_dir, exist_ok=True)
    
    num_frames = int(fps * duration)
    print(f"Generating {num_frames} clean living endcard frames ({duration:.2f}s @ {fps}fps)...")
    
    font_title = get_font(98, "impact.ttf")
    font_cta = get_font(96, "impact.ttf")
    
    t_text = "STEAL A SEED"
    tbox = font_title.getbbox(t_text)
    tw, th = tbox[2] - tbox[0], tbox[3] - tbox[1]
    
    target_card_w = max(tw, 680)
    card_base = create_glass_card(
        "campaigns/steal_a_seed/assets/branding/game_icon.png",
        target_w=target_card_w,
        radius=30,
        border_w=4
    )
    cw, ch = card_base.size
    
    cta_text = "PLAY ON ROBLOX"
    bbox_cta = font_cta.getbbox(cta_text)
    ctaw, ctah = bbox_cta[2] - bbox_cta[0], bbox_cta[3] - bbox_cta[1]
    
    def draw_text_with_outline(draw, pos, text, font, fill_color, outline_color, outline_w):
        x, y = pos
        for ox in range(-outline_w, outline_w + 1):
            for oy in range(-outline_w, outline_w + 1):
                if ox * ox + oy * oy <= outline_w * outline_w:
                    draw.text((x + ox, y + oy), text, font=font, fill=outline_color)
        draw.text((x, y), text, font=font, fill=fill_color)

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
        
        # 3. PLAY ON ROBLOX CTA - baseline at Y = 1180
        cta_x = center_x - ctaw // 2
        cta_y = int(1180 + float_y)
        
        # 2. Scaled Card with Floating Shadow placed 24px above CTA
        card_scaled_w = int(cw * scale_factor)
        card_scaled_h = int(ch * scale_factor)
        card_scaled = card_base.resize((card_scaled_w, card_scaled_h), Image.Resampling.LANCZOS)
        
        card_x = center_x - card_scaled_w // 2
        card_y = cta_y - 24 - card_scaled_h
        
        # Card shadow
        shadow_w = int(card_scaled_w * 0.92)
        shadow_h = int(card_scaled_h * 0.12)
        shadow = Image.new("RGBA", (shadow_w, shadow_h), (0, 0, 0, 0))
        draw_s = ImageDraw.Draw(shadow)
        draw_s.ellipse((0, 0, shadow_w, shadow_h), fill=(0, 0, 0, 95))
        frame.paste(shadow, (center_x - shadow_w // 2, card_y + card_scaled_h - 10), mask=shadow)
        
        frame.paste(card_scaled, (card_x, card_y), mask=card_scaled)
        
        # 1. Judul Game "STEAL A SEED" placed 24px directly above the Card
        title_x = center_x - tw // 2
        title_y = card_y - 24 - th
        
        draw_text_with_outline(
            draw, (title_x, title_y), t_text, font_title,
            fill_color=(255, 225, 0, 255), outline_color=(0, 0, 0, 255), outline_w=8
        )
        
        draw_text_with_outline(
            draw, (cta_x, cta_y), cta_text, font_cta,
            fill_color=(255, 255, 255, 255), outline_color=(0, 0, 0, 255), outline_w=8
        )
        
        frame_path = os.path.join(frames_dir, f"endcard_{f:03d}.png")
        frame.save(frame_path, "PNG")

    print(f"Generated {num_frames} frames in {frames_dir}.")

if __name__ == "__main__":
    create_endcard_frames()
