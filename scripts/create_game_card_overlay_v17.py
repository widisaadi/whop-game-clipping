import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def get_font(size, name="impact.ttf"):
    font_paths = [
        f"C:/Windows/Fonts/{name}",
        "C:/Windows/Fonts/impact.ttf",
        "C:/Windows/Fonts/arialbd.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_text_with_outline(draw, pos, text, font, fill_color, outline_color, outline_w=8, shadow_dist=6):
    x, y = pos
    # Shadow
    for dx in range(-shadow_dist, shadow_dist + 1):
        for dy in range(1, shadow_dist + 1):
            if dx*dx + dy*dy <= shadow_dist*shadow_dist:
                draw.text((x + dx, y + dy + 4), text, font=font, fill=(0, 0, 0, 180))
    # Outline
    for dx in range(-outline_w, outline_w + 1):
        for dy in range(-outline_w, outline_w + 1):
            if dx*dx + dy*dy <= outline_w*outline_w:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
    # Fill
    draw.text((x, y), text, font=font, fill=fill_color)

def generate_overlay():
    W, H = 1080, 1920
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Top Title: +1 TONGUE ESCAPE
    font_title = get_font(102, "impact.ttf")
    title_text = "+1 TONGUE ESCAPE"
    bbox = font_title.getbbox(title_text)
    tw = bbox[2] - bbox[0]
    tx = (W - tw) // 2
    ty = 320
    draw_text_with_outline(draw, (tx, ty), title_text, font_title, (255, 230, 0, 255), (0, 0, 0, 255), outline_w=9, shadow_dist=6)

    # 2. Rounded Game Card: 000.png
    src_card = "campaigns/tongue_escape/assets/branding/000.png"
    card_img = Image.open(src_card).convert("RGBA")
    card_w = 880
    card_h = int(card_w * (card_img.height / card_img.width))
    card_img = card_img.resize((card_w, card_h), Image.Resampling.LANCZOS)

    # Rounded corners & shadow
    scale = 4
    mask = Image.new("L", (card_w * scale, card_h * scale), 0)
    draw_m = ImageDraw.Draw(mask)
    draw_m.rounded_rectangle((0, 0, card_w * scale, card_h * scale), radius=28 * scale, fill=255)
    mask = mask.resize((card_w, card_h), Image.Resampling.LANCZOS)

    rounded_card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    rounded_card.paste(card_img, (0, 0), mask=mask)

    cx = (W - card_w) // 2
    cy = 470

    # Card shadow
    shadow_img = Image.new("RGBA", (card_w + 40, card_h + 40), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_img)
    s_draw.rounded_rectangle((10, 15, card_w + 30, card_h + 35), radius=30, fill=(0, 0, 0, 160))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(12))
    img.paste(shadow_img, (cx - 20, cy - 10), mask=shadow_img)

    # Paste rounded card
    img.paste(rounded_card, (cx, cy), mask=mask)

    out_path = "temp/tongue_escape/game_card_overlay_v17.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")
    print(f"Generated {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    generate_overlay()
