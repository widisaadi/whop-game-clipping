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
    
    glare = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw_g = ImageDraw.Draw(glare)
    pts = [(0, 0), (int(target_w * 0.70), 0), (int(target_w * 0.25), target_h), (0, target_h)]
    draw_g.polygon(pts, fill=(255, 255, 255, 28))
    
    img_with_glare = Image.alpha_composite(img, glare)
    card.paste(img_with_glare, (border_w, border_w), mask=mask)
    return card

def render_comparison(var_name):
    W, H = 1080, 1920
    center_x = W // 2
    frame = Image.new("RGBA", (W, H), (10, 14, 23, 255))
    draw = ImageDraw.Draw(frame)
    
    font_title = get_font(96, "impact.ttf")
    font_bio = get_font(96, "impact.ttf") # Exact same font and size
    
    # 1. Judul Game ONLY at top
    t_text = "+1 TONGUE ESCAPE"
    tbox = font_title.getbbox(t_text)
    tw, th = tbox[2] - tbox[0], tbox[3] - tbox[1]
    tx, ty = center_x - tw // 2, 220
    
    draw.text((tx, ty + 6), t_text, font=font_title, fill=(0, 0, 0, 160), stroke_width=6, stroke_fill=(0, 0, 0, 160))
    draw.text((tx, ty), t_text, font=font_title, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=(5, 10, 20, 255))
    
    # 2. Foto seukuran judul game
    target_card_w = tw
    card_base = create_glass_card("campaigns/tongue_escape/assets/branding/000.png", target_w=target_card_w, radius=32, border_w=3)
    
    cw, ch = card_base.size
    cx = center_x - cw // 2
    cy = ty + th + 36
    
    spad = 48
    shadow = Image.new("RGBA", (cw + spad * 2, ch + spad * 2), (0, 0, 0, 0))
    draw_s = ImageDraw.Draw(shadow)
    draw_s.rounded_rectangle((spad, spad + 20, spad + cw, spad + ch + 20), radius=40, fill=(0, 0, 0, 230))
    shadow = shadow.filter(ImageFilter.GaussianBlur(28))
    frame.paste(shadow, (cx - spad, cy - spad), mask=shadow)
    frame.paste(card_base, (cx, cy), mask=card_base)
    
    # Center Subtitle at Y = 975 (simulated)
    draw.text((center_x - 170, 950), "TONGUE ESCAPE", font=get_font(84, "impact.ttf"), fill=(255, 224, 64, 160), stroke_width=6, stroke_fill=(0, 0, 0, 160))
    
    # 3. LINK IN BIO
    bio_text = "LINK IN BIO"
    bbox_b = font_bio.getbbox(bio_text)
    biow, bioh = bbox_b[2] - bbox_b[0], bbox_b[3] - bbox_b[1]
    bio_x = center_x - biow // 2
    
    if var_name == "v1_button":
        # Inside radiant cyber button
        btn_w = biow + 140
        btn_h = 136
        bx = center_x - btn_w // 2
        by = 1080
        
        btn_glow = Image.new("RGBA", (btn_w + 60, btn_h + 60), (0, 0, 0, 0))
        draw_bg = ImageDraw.Draw(btn_glow)
        draw_bg.rounded_rectangle((30, 36, 30 + btn_w, 36 + btn_h), radius=36, fill=(0, 245, 160, 80))
        btn_glow = btn_glow.filter(ImageFilter.GaussianBlur(18))
        frame.paste(btn_glow, (bx - 30, by - 30), mask=btn_glow)
        
        draw.rounded_rectangle((bx, by, bx + btn_w, by + btn_h), radius=34, fill=(0, 235, 175, 255), outline=(255, 255, 255, 200), width=3)
        draw.text((bio_x, by + 28), bio_text, font=font_bio, fill=(10, 25, 47, 255))
        
    elif var_name == "v2_frosted":
        # Inside dark frosted glass capsule with cyan border
        pill_w = biow + 120
        pill_h = 136
        px = center_x - pill_w // 2
        py = 1080
        
        draw.rounded_rectangle((px, py, px + pill_w, py + pill_h), radius=34, fill=(15, 23, 42, 235), outline=(0, 240, 255, 210), width=3)
        draw.text((bio_x, py + 32), bio_text, font=font_bio, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=(5, 10, 20, 255))
        
    elif var_name == "v3_pure_title_match":
        # Standalone matching title styling exactly: pure white face with dark outline and drop shadow
        py = 1100
        draw.text((bio_x, py + 6), bio_text, font=font_bio, fill=(0, 0, 0, 160), stroke_width=6, stroke_fill=(0, 0, 0, 160))
        draw.text((bio_x, py), bio_text, font=font_bio, fill=(255, 224, 64, 255), stroke_width=6, stroke_fill=(5, 10, 20, 255))
        
    out_file = f"temp/test/compare_{var_name}.png"
    frame.save(out_file)
    print(f"Saved {out_file}")

if __name__ == "__main__":
    for v in ["v1_button", "v2_frosted", "v3_pure_title_match"]:
        render_comparison(v)
