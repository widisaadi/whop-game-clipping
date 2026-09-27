import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def get_font(size, font_name="bahnschrift.ttf"):
    font_path = os.path.join("C:/Windows/Fonts", font_name)
    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            pass
    return ImageFont.load_default()

def create_glass_card(img_path, target_w=580, radius=32, border_w=3):
    img = Image.open(img_path).convert("RGBA")
    aspect = img.height / img.width
    target_h = int(target_w * aspect)
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Rounded corners with antialiasing (4x supersampling)
    ss = 4
    mask = Image.new("L", (target_w * ss, target_h * ss), 0)
    draw_m = ImageDraw.Draw(mask)
    draw_m.rounded_rectangle((0, 0, target_w * ss, target_h * ss), radius=radius * ss, fill=255)
    mask = mask.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Outer card canvas
    card_w = target_w + border_w * 2
    card_h = target_h + border_w * 2
    card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    
    # Border mask
    bmask = Image.new("L", (card_w * ss, card_h * ss), 0)
    draw_b = ImageDraw.Draw(bmask)
    draw_b.rounded_rectangle((0, 0, card_w * ss, card_h * ss), radius=(radius + border_w) * ss, fill=255)
    bmask = bmask.resize((card_w, card_h), Image.Resampling.LANCZOS)
    
    # Multi-stop subtle neon specular rim (Cyan to Violet to Emerald)
    border_layer = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    draw_border = ImageDraw.Draw(border_layer)
    for y in range(card_h):
        ratio = y / card_h
        r = int(0 * (1 - ratio) + 0 * ratio)
        g = int(240 * (1 - ratio) + 245 * ratio)
        b = int(255 * (1 - ratio) + 160 * ratio)
        draw_border.line([(0, y), (card_w, y)], fill=(r, g, b, 240))
        
    card.paste(border_layer, (0, 0), mask=bmask)
    
    # Subtle glass glare diagonal sweep on image
    glare = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw_g = ImageDraw.Draw(glare)
    pts = [(0, 0), (int(target_w * 0.70), 0), (int(target_w * 0.25), target_h), (0, target_h)]
    draw_g.polygon(pts, fill=(255, 255, 255, 30))
    
    img_with_glare = Image.alpha_composite(img, glare)
    card.paste(img_with_glare, (border_w, border_w), mask=mask)
    
    return card

def render_sample_frame(t=1.5, variant="emerald_gradient"):
    W, H = 1080, 1920
    center_x = W // 2
    frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(frame)
    
    # Deep cinematic backdrop wash (vignette wash)
    # Simulated background for preview
    preview_bg = Image.new("RGBA", (W, H), (10, 14, 23, 255))
    frame.paste(preview_bg, (0, 0))
    
    # Ambient radial light behind the card (subtle cyan/teal glow)
    glow_size = 900
    glow_img = Image.new("RGBA", (glow_size, glow_size), (0, 0, 0, 0))
    draw_glow = ImageDraw.Draw(glow_img)
    draw_glow.ellipse((100, 100, glow_size - 100, glow_size - 100), fill=(0, 220, 255, 25))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(120))
    frame.paste(glow_img, (center_x - glow_size // 2, 350), mask=glow_img)
    
    # Typography
    font_badge = get_font(24, "bahnschrift.ttf")
    font_title = get_font(84, "impact.ttf")
    font_sub = get_font(26, "bahnschrift.ttf")
    font_btn = get_font(50, "bahnschrift.ttf")
    font_bio = get_font(26, "bahnschrift.ttf")
    
    # 1. Top Minimalist Status Pill (No emojis! Clean active indicator dot)
    badge_text = "OFFICIAL ROBLOX EXPERIENCE"
    bbox_b = font_badge.getbbox(badge_text)
    bw = bbox_b[2] - bbox_b[0]
    bh = bbox_b[3] - bbox_b[1]
    
    pill_w = bw + 74
    pill_h = 42
    pill_x = center_x - pill_w // 2
    pill_y = 175
    
    # Frosted glass background for pill
    draw.rounded_rectangle((pill_x, pill_y, pill_x + pill_w, pill_y + pill_h), radius=pill_h // 2, 
                           fill=(15, 23, 42, 230), outline=(255, 255, 255, 50), width=2)
    # Glowing emerald status dot
    dot_x, dot_y = pill_x + 24, pill_y + pill_h // 2
    dot_r = 5
    draw.ellipse((dot_x - dot_r - 2, dot_y - dot_r - 2, dot_x + dot_r + 2, dot_y + dot_r + 2), fill=(16, 185, 129, 90))
    draw.ellipse((dot_x - dot_r, dot_y - dot_r, dot_x + dot_r, dot_y + dot_r), fill=(52, 211, 153, 255))
    # Text
    draw.text((dot_x + 16, pill_y + 8), badge_text, font=font_badge, fill=(241, 245, 249, 255))
    
    # 2. Main Title: "+1 TONGUE ESCAPE" (Wide, majestic, high-contrast)
    t_text = "+1 TONGUE ESCAPE"
    tbox = font_title.getbbox(t_text)
    tw, th = tbox[2] - tbox[0], tbox[3] - tbox[1]
    tx, ty = center_x - tw // 2, pill_y + pill_h + 24
    
    # Outer crisp stroke & drop shadows FIRST
    for d in range(2, 12, 2):
        draw.text((tx, ty + d), t_text, font=font_title, fill=(0, 0, 0, 160 - d * 12))
    for dx in range(-5, 6):
        for dy in range(-5, 6):
            if abs(dx) + abs(dy) > 0:
                draw.text((tx + dx, ty + dy), t_text, font=font_title, fill=(5, 10, 20, 255))
    # Face LAST (so nothing cuts across it)
    draw.text((tx, ty), t_text, font=font_title, fill=(255, 255, 255, 255))
    
    # 3. Subtitle: Tracked geometric clean text (Proper spacing below title)
    s_text = "G R O W   Y O U R   T O N G U E   T O   S U R V I V E"
    sbox = font_sub.getbbox(s_text)
    sw, sh = sbox[2] - sbox[0], sbox[3] - sbox[1]
    sx, sy = center_x - sw // 2, ty + th + 26
    draw.text((sx, sy + 2), s_text, font=font_sub, fill=(0, 0, 0, 220))
    draw.text((sx, sy), s_text, font=font_sub, fill=(56, 189, 248, 255)) # Electric Cyan
    
    # 4. Floating Game Bento Card with Multi-layer Shadow
    float_y = 6 * math.sin(t * 3.0)
    card_base = create_glass_card("campaigns/tongue_escape/assets/branding/000.png", target_w=570, radius=30, border_w=3)
    
    cw, ch = card_base.size
    cx = center_x - cw // 2
    cy = int(sy + sh + 28 + float_y)
    
    # High-end blurred shadow
    spad = 44
    shadow = Image.new("RGBA", (cw + spad * 2, ch + spad * 2), (0, 0, 0, 0))
    draw_s = ImageDraw.Draw(shadow)
    draw_s.rounded_rectangle((spad, spad + 18, spad + cw, spad + ch + 18), radius=38, fill=(0, 0, 0, 220))
    shadow = shadow.filter(ImageFilter.GaussianBlur(26))
    
    frame.paste(shadow, (cx - spad, cy - spad), mask=shadow)
    frame.paste(card_base, (cx, cy), mask=card_base)
    
    # 5. Bottom CTA Button: Starts at Y = 1080 (leaves Y=920-1040 100% free for subtitles at Y=975)
    btn_w, btn_h = 750, 114
    bx = center_x - btn_w // 2
    by = 1080
    
    ss = 4
    if variant == "emerald_gradient":
        # Ambient button glow
        btn_glow = Image.new("RGBA", (btn_w + 60, btn_h + 60), (0, 0, 0, 0))
        draw_bg = ImageDraw.Draw(btn_glow)
        draw_bg.rounded_rectangle((30, 36, 30 + btn_w, 36 + btn_h), radius=36, fill=(0, 245, 160, 75))
        btn_glow = btn_glow.filter(ImageFilter.GaussianBlur(18))
        frame.paste(btn_glow, (bx - 30, by - 30), mask=btn_glow)
        
        # High-res button surface
        btn_surf = Image.new("RGBA", (btn_w * ss, btn_h * ss), (0, 0, 0, 0))
        draw_btn = ImageDraw.Draw(btn_surf)
        
        # Smooth horizontal gradient
        for x in range(btn_w * ss):
            ratio = x / (btn_w * ss)
            cr = int(0 * (1 - ratio) + 0 * ratio)
            cg = int(245 * (1 - ratio) + 217 * ratio)
            cb = int(160 * (1 - ratio) + 245 * ratio)
            draw_btn.line([(x, 0), (x, btn_h * ss)], fill=(cr, cg, cb, 255))
            
        # Angled specular sheen using alpha composite
        sheen_layer = Image.new("RGBA", (btn_w * ss, btn_h * ss), (0, 0, 0, 0))
        draw_sh = ImageDraw.Draw(sheen_layer)
        sheen_center = ((t * 400) % (btn_w + 500) - 250) * ss
        sheen_w = 70 * ss
        for i in range(-int(sheen_w), int(sheen_w)):
            px = sheen_center + i
            alpha = int(70 * (1 - abs(i) / sheen_w))
            draw_sh.line([(px - 35 * ss, 0), (px + 35 * ss, btn_h * ss)], fill=(255, 255, 255, alpha), width=ss)
            
        btn_surf = Image.alpha_composite(btn_surf, sheen_layer)
            
        # Button mask
        btn_mask = Image.new("L", (btn_w * ss, btn_h * ss), 0)
        draw_bm = ImageDraw.Draw(btn_mask)
        draw_bm.rounded_rectangle((0, 0, btn_w * ss, btn_h * ss), radius=28 * ss, fill=255)
        
        btn_final = btn_surf.resize((btn_w, btn_h), Image.Resampling.LANCZOS)
        btn_mask_final = btn_mask.resize((btn_w, btn_h), Image.Resampling.LANCZOS)
        frame.paste(btn_final, (bx, by), mask=btn_mask_final)
        
        # Crisp inner highlight border
        draw.rounded_rectangle((bx, by, bx + btn_w, by + btn_h), radius=28, outline=(255, 255, 255, 180), width=2)
        
        # Play Icon (sharp geometric equilateral triangle)
        play_x = bx + 60
        play_y = by + 37
        pts = [(play_x, play_y), (play_x + 30, play_y + 19), (play_x, play_y + 38)]
        draw.polygon(pts, fill=(10, 25, 47, 255))
        
        # Button Text: Pure obsidian contrast
        btn_text = "PLAY FREE ON ROBLOX"
        bbox_btn = font_btn.getbbox(btn_text)
        btn_tw = bbox_btn[2] - bbox_btn[0]
        btn_tx = bx + 105 + (btn_w - 105 - btn_tw) // 2
        draw.text((btn_tx, by + 28), btn_text, font=font_btn, fill=(10, 25, 47, 255))
        
    # 6. Bio Link Pill (Minimalist geometric indicator)
    bio_text = "SEARCH EXPERIENCE  •  DIRECT LINK IN BIO  >"
    bbox_bio = font_bio.getbbox(bio_text)
    biow = bbox_bio[2] - bbox_bio[0]
    bioh = bbox_bio[3] - bbox_bio[1]
    
    bpill_w = biow + 64
    bpill_h = 46
    biox = center_x - bpill_w // 2
    bioy = by + btn_h + 26
    
    draw.rounded_rectangle((biox, bioy, biox + bpill_w, bioy + bpill_h), radius=bpill_h // 2,
                           fill=(15, 23, 42, 230), outline=(255, 255, 255, 45), width=2)
    draw.text((center_x - biow // 2, bioy + 9), bio_text, font=font_bio, fill=(203, 213, 225, 255))
    
    out_file = f"temp/test/gpt_taste_endcard_{variant}.png"
    frame.save(out_file)
    print(f"Sample frame rendered: {out_file}")

if __name__ == "__main__":
    render_sample_frame(t=1.5, variant="emerald_gradient")
