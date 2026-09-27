import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BRANDING_DIR = r"d:\create something\local\tiktokclipping\campaigns\lessons_in_love_and_hate\assets\branding"
FRAMES_DIR = r"d:\create something\local\tiktokclipping\temp\lessons_in_love_and_hate\endcard_frames"
os.makedirs(FRAMES_DIR, exist_ok=True)

def get_font(size, font_name="impact.ttf"):
    font_path = os.path.join("C:/Windows/Fonts", font_name)
    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            pass
    return ImageFont.load_default()

def create_poster_card(img_path, target_w=520, radius=28, border_w=3):
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
    
    # Rose-gold gradient border
    border_layer = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    draw_border = ImageDraw.Draw(border_layer)
    for y in range(card_h):
        ratio = y / card_h
        r = int(255 * (1 - ratio) + 244 * ratio)
        g = int(80 * (1 - ratio) + 114 * ratio)
        b = int(140 * (1 - ratio) + 182 * ratio)
        draw_border.line([(0, y), (card_w, y)], fill=(r, g, b, 240))
        
    card.paste(border_layer, (0, 0), mask=bmask)
    
    # Subtle glass glare
    glare = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw_g = ImageDraw.Draw(glare)
    pts = [(0, 0), (int(target_w * 0.65), 0), (int(target_w * 0.20), target_h), (0, target_h)]
    draw_g.polygon(pts, fill=(255, 255, 255, 24))
    
    img_with_glare = Image.alpha_composite(img, glare)
    card.paste(img_with_glare, (border_w, border_w), mask=mask)
    return card

def create_endcard_frames(fps=30, duration=4.0):
    W, H = 1080, 1920
    center_x = W // 2
    num_frames = int(fps * duration)
    print(f"Generating {num_frames} frames for Living Endcard ({duration:.1f}s @ {fps}fps)...")
    
    poster_path = os.path.join(BRANDING_DIR, "CoverComplete.png")
    logo_path = os.path.join(BRANDING_DIR, "SeriesLogo.png")
    
    poster_card = create_poster_card(poster_path, target_w=520, radius=28, border_w=3)
    card_w, card_h = poster_card.size
    
    # Pre-render Drop Shadow for Card
    shadow_pad = 40
    shadow = Image.new("RGBA", (card_w + shadow_pad * 2, card_h + shadow_pad * 2), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle((shadow_pad, shadow_pad, card_w + shadow_pad, card_h + shadow_pad), radius=28, fill=(0, 0, 0, 180))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=24))
    
    # Load and scale Series Logo
    logo_img = Image.open(logo_path).convert("RGBA")
    logo_target_w = 640
    logo_target_h = int(logo_target_w * (logo_img.height / logo_img.width))
    logo_img = logo_img.resize((logo_target_w, logo_target_h), Image.Resampling.LANCZOS)
    
    # Text fonts
    font_cta = get_font(88, "impact.ttf")
    font_sub = get_font(42, "bahnschrift.ttf")
    
    cta_text = "STREAM NOW ON SHORTS"
    cbox = font_cta.getbbox(cta_text)
    cw = cbox[2] - cbox[0]
    
    sub_text = "Official Series Available Exclusively on Shorts"
    sbox = font_sub.getbbox(sub_text)
    sw = sbox[2] - sbox[0]
    
    # Baseline layout coordinates
    base_cta_y = 1320
    base_sub_y = base_cta_y + 90
    base_card_y = base_cta_y - 28 - card_h
    base_logo_y = base_card_y - 28 - logo_target_h
    
    for i in range(num_frames):
        t = i / fps
        frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        
        # Entrance scale animation (first 0.35s)
        if t < 0.35:
            progress = t / 0.35
            # spring ease out
            c4 = (2 * math.pi) / 3
            if progress == 0:
                scale = 0.8
            else:
                scale = math.pow(2, -10 * progress) * math.sin((progress * 10 - 0.75) * c4) + 1.0
            scale = 0.8 + 0.2 * scale
            alpha_mult = min(1.0, progress * 3.0)
        else:
            scale = 1.0
            alpha_mult = 1.0
            
        # Subtle harmonic float
        float_y = int(5 * math.sin(t * 2.8))
        
        # 1. Series Logo
        logo_x = center_x - logo_target_w // 2
        logo_y = base_logo_y + float_y
        frame.paste(logo_img, (logo_x, logo_y), mask=logo_img)
        
        # 2. Poster Card Shadow & Card
        card_x = center_x - card_w // 2
        card_y = base_card_y + float_y
        frame.paste(shadow, (card_x - shadow_pad, card_y - shadow_pad + 8), mask=shadow)
        frame.paste(poster_card, (card_x, card_y), mask=poster_card)
        
        # 3. CTA Text ("STREAM NOW ON SHORTS")
        draw = ImageDraw.Draw(frame)
        cta_x = center_x - cw // 2
        cta_y = base_cta_y + float_y
        
        # Text shadow and outline
        for ox, oy in [(-3,0), (3,0), (0,-3), (0,3), (-2,-2), (2,2), (-2,2), (2,-2), (0, 4)]:
            draw.text((cta_x + ox, cta_y + oy), cta_text, font=font_cta, fill=(0, 0, 0, int(230 * alpha_mult)))
        draw.text((cta_x, cta_y), cta_text, font=font_cta, fill=(255, 255, 255, int(255 * alpha_mult)))
        
        # Subtitle label
        sub_x = center_x - sw // 2
        sub_y = base_sub_y + float_y
        for ox, oy in [(-1,-1), (1,1), (-1,1), (1,-1)]:
            draw.text((sub_x + ox, sub_y + oy), sub_text, font=font_sub, fill=(0, 0, 0, int(200 * alpha_mult)))
        draw.text((sub_x, sub_y), sub_text, font=font_sub, fill=(255, 180, 205, int(240 * alpha_mult)))
        
        out_name = os.path.join(FRAMES_DIR, f"endcard_{i:04d}.png")
        frame.save(out_name)
        
    print(f"Living Endcard frames ready in {FRAMES_DIR}")

if __name__ == "__main__":
    create_endcard_frames()
