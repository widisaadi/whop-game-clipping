import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def get_font(size, font_name="impact.ttf"):
    font_path = os.path.join("C:/Windows/Fonts", font_name)
    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            pass
    return ImageFont.load_default()

def create_glass_card(img_path, target_w=740, radius=32, border_w=3):
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
        r = int(0 * (1 - ratio) + 0 * ratio)
        g = int(240 * (1 - ratio) + 245 * ratio)
        b = int(255 * (1 - ratio) + 160 * ratio)
        draw_border.line([(0, y), (card_w, y)], fill=(r, g, b, 240))
        
    card.paste(border_layer, (0, 0), mask=bmask)
    
    # Subtle glass glare diagonal sweep
    glare = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw_g = ImageDraw.Draw(glare)
    pts = [(0, 0), (int(target_w * 0.70), 0), (int(target_w * 0.25), target_h), (0, target_h)]
    draw_g.polygon(pts, fill=(255, 255, 255, 28))
    
    img_with_glare = Image.alpha_composite(img, glare)
    card.paste(img_with_glare, (border_w, border_w), mask=mask)
    return card

def render_layout(case_name="case_a"):
    W, H = 1080, 1920
    center_x = W // 2
    frame = Image.new("RGBA", (W, H), (10, 14, 23, 255))
    draw = ImageDraw.Draw(frame)
    
    # Fonts
    # User: "font dan sizenya sesuai dengan judul game"
    font_title = get_font(92, "impact.ttf")
    font_bio = get_font(92, "impact.ttf") # Same font and size as title!
    
    # 1. Judul Game ONLY at the top (no official roblox experience, no grow your tongue to survive)
    t_text = "+1 TONGUE ESCAPE"
    tbox = font_title.getbbox(t_text)
    tw, th = tbox[2] - tbox[0], tbox[3] - tbox[1]
    
    # Position title nicely at the top
    tx, ty = center_x - tw // 2, 210
    
    # Crisp drop shadow & outline
    draw.text((tx, ty + 6), t_text, font=font_title, fill=(0, 0, 0, 160), stroke_width=6, stroke_fill=(0, 0, 0, 160))
    draw.text((tx, ty), t_text, font=font_title, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=(5, 10, 20, 255))
    
    # 2. Foto digedein seukuran judul game!
    # Title width is tw (~700-740px). Let's make card target_w exactly tw!
    target_card_w = max(tw, 740)
    card_base = create_glass_card("campaigns/tongue_escape/assets/branding/000.png", target_w=target_card_w, radius=32, border_w=3)
    
    cw, ch = card_base.size
    cx = center_x - cw // 2
    cy = ty + th + 36 # Right below the game title
    
    # Blurred drop shadow
    spad = 48
    shadow = Image.new("RGBA", (cw + spad * 2, ch + spad * 2), (0, 0, 0, 0))
    draw_s = ImageDraw.Draw(shadow)
    draw_s.rounded_rectangle((spad, spad + 20, spad + cw, spad + ch + 20), radius=40, fill=(0, 0, 0, 230))
    shadow = shadow.filter(ImageFilter.GaussianBlur(28))
    frame.paste(shadow, (cx - spad, cy - spad), mask=shadow)
    frame.paste(card_base, (cx, cy), mask=card_base)
    
    # Card ends at cy + ch = 210 + 72 + 36 + 524 = 842!
    # Subtitle is at Y = 975! (Leaves 133px clearance before subtitle!)
    
    # Simulated Subtitle at Y = 975 (from video)
    draw.text((center_x - 180, 950), "TONGUE ESCAPE", font=get_font(84, "impact.ttf"), fill=(255, 224, 64, 180), stroke_width=6, stroke_fill=(0, 0, 0, 180))
    
    if case_name == "case_a":
        # Case A: Both PLAY FREE ON ROBLOX button + LINK IN BIO (size 92 Impact)
        # Button
        btn_w, btn_h = 750, 108
        bx = center_x - btn_w // 2
        by = 1070
        
        btn_glow = Image.new("RGBA", (btn_w + 50, btn_h + 50), (0, 0, 0, 0))
        draw_bg = ImageDraw.Draw(btn_glow)
        draw_bg.rounded_rectangle((25, 30, 25 + btn_w, 30 + btn_h), radius=32, fill=(0, 245, 160, 65))
        btn_glow = btn_glow.filter(ImageFilter.GaussianBlur(16))
        frame.paste(btn_glow, (bx - 25, by - 25), mask=btn_glow)
        
        draw.rounded_rectangle((bx, by, bx + btn_w, by + btn_h), radius=28, fill=(0, 230, 180, 255), outline=(255, 255, 255, 180), width=2)
        btn_font = get_font(48, "bahnschrift.ttf")
        b_txt = "PLAY FREE ON ROBLOX"
        bb = btn_font.getbbox(b_txt)
        draw.text((bx + (btn_w - (bb[2]-bb[0]))//2, by + 26), b_txt, font=btn_font, fill=(10, 25, 47, 255))
        
        # LINK IN BIO below button (Font & Size matching game title: Impact 92)
        bio_text = "LINK IN BIO"
        bbox_b = font_bio.getbbox(bio_text)
        biow = bbox_b[2] - bbox_b[0]
        bio_x = center_x - biow // 2
        bio_y = by + btn_h + 28
        
        # Draw clean glowing pill or styled text
        pill_w = biow + 80
        pill_h = 110
        px = center_x - pill_w // 2
        draw.rounded_rectangle((px, bio_y - 12, px + pill_w, bio_y + pill_h - 12), radius=32, fill=(15, 23, 42, 230), outline=(0, 240, 255, 180), width=3)
        draw.text((bio_x, bio_y + 4), bio_text, font=font_bio, fill=(255, 224, 64, 255), stroke_width=6, stroke_fill=(0, 0, 0, 255))
        
    elif case_name == "case_b":
        # Case B: The button IS the LINK IN BIO (Impact 92, matching game title)
        btn_w, btn_h = 760, 130
        bx = center_x - btn_w // 2
        by = 1080
        
        # Glowing radiant button
        btn_glow = Image.new("RGBA", (btn_w + 60, btn_h + 60), (0, 0, 0, 0))
        draw_bg = ImageDraw.Draw(btn_glow)
        draw_bg.rounded_rectangle((30, 36, 30 + btn_w, 36 + btn_h), radius=36, fill=(0, 245, 160, 85))
        btn_glow = btn_glow.filter(ImageFilter.GaussianBlur(18))
        frame.paste(btn_glow, (bx - 30, by - 30), mask=btn_glow)
        
        # Gradient fill
        draw.rounded_rectangle((bx, by, bx + btn_w, by + btn_h), radius=32, fill=(0, 235, 175, 255), outline=(255, 255, 255, 200), width=3)
        
        bio_text = "LINK IN BIO"
        bbox_b = font_bio.getbbox(bio_text)
        biow = bbox_b[2] - bbox_b[0]
        bio_x = center_x - biow // 2
        draw.text((bio_x, by + 26), bio_text, font=font_bio, fill=(10, 25, 47, 255), stroke_width=4, stroke_fill=(255, 255, 255, 120))
        
    elif case_name == "case_c":
        # Case C: Minimalist Pure Text/Pill LINK IN BIO (matching How to Fisch 08 style with Impact 92)
        bio_text = "LINK IN BIO"
        bbox_b = font_bio.getbbox(bio_text)
        biow = bbox_b[2] - bbox_b[0]
        bio_x = center_x - biow // 2
        bio_y = 1100
        
        pill_w = biow + 90
        pill_h = 120
        px = center_x - pill_w // 2
        
        # Frosted glass capsule with cyan glowing border
        draw.rounded_rectangle((px, bio_y, px + pill_w, bio_y + pill_h), radius=36, fill=(15, 23, 42, 235), outline=(0, 240, 255, 200), width=3)
        draw.text((bio_x, bio_y + 18), bio_text, font=font_bio, fill=(255, 224, 64, 255), stroke_width=6, stroke_fill=(5, 10, 20, 255))
        
    out_file = f"temp/test/layout_{case_name}.png"
    frame.save(out_file)
    print(f"Saved {out_file}")

if __name__ == "__main__":
    for c in ["case_a", "case_b", "case_c"]:
        render_layout(c)
