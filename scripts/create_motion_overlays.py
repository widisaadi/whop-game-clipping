import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def get_font(size, bold=True):
    font_paths = [
        "C:/Windows/Fonts/impact.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/seguiui.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def create_rounded_icon(src_path, size, radius, border_w=6, border_color=(255, 224, 64, 255)):
    base_img = Image.open(src_path).convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)
    scale = 4
    mask = Image.new("L", (size * scale, size * scale), 0)
    draw_m = ImageDraw.Draw(mask)
    draw_m.rounded_rectangle((0, 0, size * scale, size * scale), radius=radius * scale, fill=255)
    mask = mask.resize((size, size), Image.Resampling.LANCZOS)
    
    rounded = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    rounded.paste(base_img, (0, 0), mask=mask)
    
    total_size = size + border_w * 2
    framed = Image.new("RGBA", (total_size, total_size), (0, 0, 0, 0))
    
    border_mask = Image.new("L", (total_size * scale, total_size * scale), 0)
    draw_bm = ImageDraw.Draw(border_mask)
    draw_bm.rounded_rectangle((0, 0, total_size * scale, total_size * scale), radius=(radius + border_w) * scale, fill=255)
    border_mask = border_mask.resize((total_size, total_size), Image.Resampling.LANCZOS)
    
    border_layer = Image.new("RGBA", (total_size, total_size), border_color)
    framed.paste(border_layer, (0, 0), mask=border_mask)
    framed.paste(rounded, (border_w, border_w), mask=mask)
    
    return framed

def create_intro_badge():
    W, H = 1080, 1920
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    center_x = W // 2
    draw = ImageDraw.Draw(img)
    
    # 1. Pill above icon: "NEW ROBLOX EXPERIENCE"
    font_pill = get_font(28)
    pill_text = "NEW ROBLOX EXPERIENCE"
    pbox = font_pill.getbbox(pill_text)
    pw, ph = pbox[2] - pbox[0], pbox[3] - pbox[1]
    
    pill_w = pw + 48
    pill_h = ph + 22
    pill_x = center_x - pill_w // 2
    pill_y = 440
    
    draw.rounded_rectangle((pill_x, pill_y + 4, pill_x + pill_w, pill_y + pill_h + 4), radius=pill_h // 2, fill=(0, 0, 0, 150))
    draw.rounded_rectangle((pill_x, pill_y, pill_x + pill_w, pill_y + pill_h), radius=pill_h // 2, fill=(255, 45, 65, 255))
    draw.rounded_rectangle((pill_x, pill_y, pill_x + pill_w, pill_y + pill_h), radius=pill_h // 2, outline=(255, 200, 200, 200), width=2)
    draw.text((center_x - pw // 2, pill_y + 9), pill_text, font=font_pill, fill=(255, 255, 255, 255))
    
    # 2. Rounded Icon (380x380) with deep gold frame and shadow
    icon_size = 380
    radius = 60
    border_w = 8
    icon_framed = create_rounded_icon("assets/how_to_fisch_official_icon.png", icon_size, radius, border_w, (255, 224, 64, 255))
    
    shadow_pad = 45
    shadow = Image.new("RGBA", (icon_framed.width + shadow_pad * 2, icon_framed.height + shadow_pad * 2), (0, 0, 0, 0))
    draw_s = ImageDraw.Draw(shadow)
    draw_s.rounded_rectangle((shadow_pad, shadow_pad + 18, shadow_pad + icon_framed.width, shadow_pad + icon_framed.height + 18), radius=radius, fill=(0, 0, 0, 230))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    
    icon_y = pill_y + pill_h + 24
    img.paste(shadow, (center_x - shadow.width // 2, icon_y - shadow_pad), mask=shadow)
    img.paste(icon_framed, (center_x - icon_framed.width // 2, icon_y), mask=icon_framed)
    
    out_path = "assets/intro_badge.png"
    img.save(out_path, "PNG")
    print(f"Created updated {out_path} (icon ends at y={icon_y + icon_framed.height})")

def create_endcard_overlay():
    W, H = 1080, 1920
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center_x = W // 2
    
    # 1. Top Badge: "NEW ROBLOX SURVIVAL EXPERIENCE"
    font_badge = get_font(26)
    b_text = "NEW ROBLOX SURVIVAL EXPERIENCE"
    bbox = font_badge.getbbox(b_text)
    bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    pad_x, pad_y = 32, 12
    badge_w = bw + pad_x * 2
    badge_h = bh + pad_y * 2
    badge_x = center_x - badge_w // 2
    badge_y = 230
    
    draw.rounded_rectangle((badge_x, badge_y + 6, badge_x + badge_w, badge_y + badge_h + 6), radius=badge_h // 2, fill=(0, 0, 0, 140))
    draw.rounded_rectangle((badge_x, badge_y, badge_x + badge_w, badge_y + badge_h), radius=badge_h // 2, fill=(255, 45, 65, 255))
    draw.rounded_rectangle((badge_x, badge_y, badge_x + badge_w, badge_y + badge_h), radius=badge_h // 2, outline=(255, 180, 190, 200), width=2)
    draw.text((center_x - bw // 2, badge_y + pad_y - 2), b_text, font=font_badge, fill=(255, 255, 255, 255))
    
    # 2. Main Title: "HOW TO FISCH"
    font_title = get_font(90)
    t_text = "HOW TO FISCH"
    tbox = font_title.getbbox(t_text)
    tw, th = tbox[2] - tbox[0], tbox[3] - tbox[1]
    tx = center_x - tw // 2
    ty = badge_y + badge_h + 24
    
    for dx in range(-5, 6):
        for dy in range(-5, 6):
            if abs(dx) + abs(dy) > 0:
                draw.text((tx + dx, ty + dy), t_text, font=font_title, fill=(0, 0, 0, 255))
    draw.text((tx, ty + 8), t_text, font=font_title, fill=(180, 120, 0, 255))
    draw.text((tx, ty), t_text, font=font_title, fill=(255, 224, 64, 255))
    
    # 3. Subtitle: "WHERE EVERY CATCH FIGHTS BACK!"
    font_sub = get_font(32)
    s_text = "WHERE EVERY CATCH FIGHTS BACK!"
    sbox = font_sub.getbbox(s_text)
    sw, sh = sbox[2] - sbox[0], sbox[3] - sbox[1]
    sx = center_x - sw // 2
    sy = ty + th + 26
    
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if abs(dx) + abs(dy) > 0:
                draw.text((sx + dx, sy + dy), s_text, font=font_sub, fill=(0, 0, 0, 220))
    draw.text((sx, sy), s_text, font=font_sub, fill=(220, 235, 255, 255))
    
    # 4. Official Game Icon with Luxury Frame
    icon_size = 520
    radius = 75
    border_w = 8
    icon_framed = create_rounded_icon("assets/how_to_fisch_official_icon.png", icon_size, radius, border_w, (255, 224, 64, 255))
    
    # Ambient deep shadow
    s_pad = 60
    shadow = Image.new("RGBA", (icon_framed.width + s_pad * 2, icon_framed.height + s_pad * 2), (0, 0, 0, 0))
    draw_s = ImageDraw.Draw(shadow)
    draw_s.rounded_rectangle((s_pad, s_pad + 20, s_pad + icon_framed.width, s_pad + icon_framed.height + 20), radius=radius, fill=(0, 0, 0, 240))
    shadow = shadow.filter(ImageFilter.GaussianBlur(25))
    
    icon_y = sy + sh + 45
    img.paste(shadow, (center_x - shadow.width // 2, icon_y - s_pad), mask=shadow)
    img.paste(icon_framed, (center_x - icon_framed.width // 2, icon_y), mask=icon_framed)
    
    # 5. CTA Button: "PLAY FREE ON ROBLOX"
    btn_w = 780
    btn_h = 114
    btn_x = center_x - btn_w // 2
    btn_y = icon_y + icon_framed.height + 55
    
    btn_shadow = Image.new("RGBA", (btn_w + 40, btn_h + 40), (0, 0, 0, 0))
    draw_bs = ImageDraw.Draw(btn_shadow)
    draw_bs.rounded_rectangle((20, 25, 20 + btn_w, 25 + btn_h), radius=btn_h // 2, fill=(0, 200, 80, 160))
    btn_shadow = btn_shadow.filter(ImageFilter.GaussianBlur(14))
    img.paste(btn_shadow, (btn_x - 20, btn_y - 15), mask=btn_shadow)
    
    draw.rounded_rectangle((btn_x, btn_y + 8, btn_x + btn_w, btn_y + btn_h + 8), radius=btn_h // 2, fill=(0, 110, 45, 255))
    draw.rounded_rectangle((btn_x, btn_y, btn_x + btn_w, btn_y + btn_h), radius=btn_h // 2, fill=(0, 220, 100, 255))
    draw.rounded_rectangle((btn_x, btn_y, btn_x + btn_w, btn_y + btn_h), radius=btn_h // 2, outline=(180, 255, 200, 230), width=4)
    
    tri_x = btn_x + 55
    tri_y = btn_y + btn_h // 2
    tri_r = 18
    draw.polygon([(tri_x, tri_y - tri_r), (tri_x + int(tri_r * 1.5), tri_y), (tri_x, tri_y + tri_r)], fill=(6, 16, 30, 255))
    
    font_btn = get_font(42)
    btn_text = "PLAY FREE ON ROBLOX"
    bbox_btn = font_btn.getbbox(btn_text)
    btn_tw = bbox_btn[2] - bbox_btn[0]
    draw.text((center_x - btn_tw // 2 + 20, btn_y + (btn_h - (bbox_btn[3] - bbox_btn[1])) // 2 - 2), btn_text, font=font_btn, fill=(6, 16, 30, 255))
    
    out_path = "assets/endcard_overlay.png"
    img.save(out_path, "PNG")
    print(f"Created {out_path}")

if __name__ == "__main__":
    create_intro_badge()
    create_endcard_overlay()
