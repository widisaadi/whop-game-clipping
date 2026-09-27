import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_endcard():
    W, H = 1080, 1920
    
    # 1. Base gradient background
    base = Image.new("RGBA", (W, H), (10, 25, 45, 255))
    draw = ImageDraw.Draw(base)
    for y in range(H):
        r = int(10 + (22 - 10) * (y / H))
        g = int(24 + (60 - 24) * (y / H))
        b = int(52 + (110 - 52) * (y / H))
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))
        
    # Overlay blurred gameplay frame for rich background texture
    if os.path.exists("temp/crop_test/14_vert.jpg"):
        bg_tex = Image.open("temp/crop_test/14_vert.jpg").convert("RGBA")
        bg_tex = bg_tex.filter(ImageFilter.GaussianBlur(radius=32))
        dark = Image.new("RGBA", (W, H), (5, 12, 28, 190))
        bg_tex = Image.alpha_composite(bg_tex, dark)
        base = Image.alpha_composite(base, bg_tex)
        draw = ImageDraw.Draw(base)

    # Fonts
    font_title = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", 96)
    font_sub = ImageFont.truetype("C:/Windows/Fonts/bahnschrift.ttf", 40)
    font_btn = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", 62)
    font_tag = ImageFont.truetype("C:/Windows/Fonts/bahnschrift.ttf", 34)

    # 2. Top Badge: "NEW ROBLOX SURVIVAL EXPERIENCE"
    tag_text = "NEW ROBLOX SURVIVAL EXPERIENCE"
    bbox = draw.textbbox((0, 0), tag_text, font=font_tag)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx, ty = (W - tw) // 2, 250
    pad_x, pad_y = 28, 14
    draw.rounded_rectangle([tx - pad_x, ty - pad_y, tx + tw + pad_x, ty + th + pad_y], radius=16, fill=(245, 60, 40, 240))
    draw.text((tx, ty), tag_text, font=font_tag, fill=(255, 255, 255, 255))

    # 3. Main Title: "HOW TO FISCH"
    title_text = "HOW TO FISCH"
    tbbox = draw.textbbox((0, 0), title_text, font=font_title)
    ttw = tbbox[2] - tbbox[0]
    ttx, tty = (W - ttw) // 2, 355
    
    # Drop shadow
    for offset in range(8, 0, -2):
        draw.text((ttx + offset, tty + offset), title_text, font=font_title, fill=(0, 0, 0, 180))
    # Outline
    for ox, oy in [(-3,0), (3,0), (0,-3), (0,3), (-2,-2), (2,2), (-2,2), (2,-2)]:
        draw.text((ttx + ox, tty + oy), title_text, font=font_title, fill=(10, 20, 40, 255))
    draw.text((ttx, tty), title_text, font=font_title, fill=(255, 220, 35, 255)) # Vibrant Gold

    # 4. Tagline: "WHERE EVERY CATCH FIGHTS BACK!"
    sub_text = "WHERE EVERY CATCH FIGHTS BACK!"
    sbbox = draw.textbbox((0, 0), sub_text, font=font_sub)
    stw = sbbox[2] - sbbox[0]
    draw.text(((W - stw) // 2, 485), sub_text, font=font_sub, fill=(215, 242, 255, 255))

    # 5. Official Game Icon (Prominent and clear)
    icon_path = "assets/how_to_fisch_official_icon.png"
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert("RGBA")
        icon_size = 590
        icon = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        
        # Rounded corners mask
        mask = Image.new("L", (icon_size, icon_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, icon_size, icon_size], radius=64, fill=255)
        
        # Drop shadow behind icon
        ix = (W - icon_size) // 2
        iy = 570
        shadow = Image.new("RGBA", (icon_size + 60, icon_size + 60), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(shadow)
        sdraw.rounded_rectangle([20, 20, icon_size + 40, icon_size + 40], radius=70, fill=(0, 0, 0, 180))
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=20))
        base.paste(shadow, (ix - 30, iy - 20), shadow)

        # Outer border
        border_rect = [ix - 8, iy - 8, ix + icon_size + 8, iy + icon_size + 8]
        draw.rounded_rectangle(border_rect, radius=72, fill=(255, 255, 255, 255), outline=(255, 215, 0, 255), width=6)

        # Paste icon
        base.paste(icon, (ix, iy), mask)

    # 6. Big CTA Button: "PLAY FREE ON ROBLOX"
    btn_w, btn_h = 760, 125
    bx = (W - btn_w) // 2
    by = 1230
    # Button Shadow
    draw.rounded_rectangle([bx + 4, by + 10, bx + btn_w + 4, by + btn_h + 10], radius=32, fill=(0, 0, 0, 140))
    # Button body
    draw.rounded_rectangle([bx, by, bx + btn_w, by + btn_h], radius=32, fill=(0, 204, 102, 255), outline=(255, 255, 255, 255), width=4)
    
    # Draw vector play triangle
    tri_x = bx + 55
    tri_y = by + 40
    tri_pts = [(tri_x, tri_y), (tri_x + 35, tri_y + 22), (tri_x, tri_y + 45)]
    draw.polygon(tri_pts, fill=(255, 255, 255, 255))

    btn_text = "PLAY FREE ON ROBLOX"
    btn_bbox = draw.textbbox((0, 0), btn_text, font=font_btn)
    btn_tw, btn_th = btn_bbox[2] - btn_bbox[0], btn_bbox[3] - btn_bbox[1]
    btn_tx = bx + 115 + (btn_w - 115 - btn_tw) // 2
    btn_ty = by + (btn_h - btn_th) // 2 - 5
    draw.text((btn_tx + 2, btn_ty + 3), btn_text, font=font_btn, fill=(0, 65, 30, 255))
    draw.text((btn_tx, btn_ty), btn_text, font=font_btn, fill=(255, 255, 255, 255))

    # Save
    out_path = "assets/endcard.png"
    base.convert("RGB").save(out_path, quality=95)
    print("Updated clean endcard to", out_path)

if __name__ == "__main__":
    create_endcard()
