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
    
    # Gold & Emerald Money Border gradient
    border_layer = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    draw_border = ImageDraw.Draw(border_layer)
    for y in range(card_h):
        ratio = y / card_h
        # Gold to rich emerald green gradient
        r = int(255 * (1 - ratio) + 30 * ratio)
        g = int(215 * (1 - ratio) + 230 * ratio)
        b = int(0 * (1 - ratio) + 90 * ratio)
        draw_border.line([(0, y), (card_w, y)], fill=(r, g, b, 245))
        
    card.paste(border_layer, (0, 0), mask=bmask)
    
    # Subtle glass glare diagonal sweep
    glare = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw_g = ImageDraw.Draw(glare)
    pts = [(0, 0), (int(target_w * 0.70), 0), (int(target_w * 0.25), target_h), (0, target_h)]
    draw_g.polygon(pts, fill=(255, 255, 255, 30))
    
    img_with_glare = Image.alpha_composite(img, glare)
    card.paste(img_with_glare, (border_w, border_w), mask=mask)
    return card

def create_endcard_frames(fps=30, duration=3.90):
    W, H = 1080, 1920
    center_x = W // 2
    frames_dir = "temp/money_roll/endcard_frames"
    os.makedirs(frames_dir, exist_ok=True)
    
    num_frames = int(fps * duration)
    print(f"Generating {num_frames} +1 Money Roll Living Endcard frames ({duration:.2f}s @ {fps}fps)...")
    
    font_title = get_font(96, "impact.ttf")
    font_code = get_font(88, "impact.ttf")
    font_sub = get_font(68, "impact.ttf")
    
    t_text = "+1 MONEY ROLL"
    tbox = font_title.getbbox(t_text)
    tw, th = tbox[2] - tbox[0], tbox[3] - tbox[1]
    
    code_text = "CODE: 3694-1078-5324"
    cbox = font_code.getbbox(code_text)
    cw, ch = cbox[2] - cbox[0], cbox[3] - cbox[1]
    
    play_text = "PLAY ON FORTNITE"
    pbox = font_sub.getbbox(play_text)
    pw, ph = pbox[2] - pbox[0], pbox[3] - pbox[1]
    
    target_card_w = 700
    card_base = create_glass_card("campaigns/money_roll/assets/branding/000_IMAGE.png", target_w=target_card_w, radius=28, border_w=4)
    
    for f in range(num_frames):
        t = f / fps
        
        # Entrance pop-in (0-0.35s) then floating breathing
        if t < 0.35:
            progress = t / 0.35
            scale_factor = 0.6 + 0.4 * math.sin(progress * (math.pi / 2))
        else:
            scale_factor = 1.0 + 0.012 * math.sin((t - 0.35) * 2.4)
            
        float_y = 6 * math.sin(t * 2.8)
        
        frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        
        # Sizing card
        curr_w = int(card_base.width * scale_factor)
        curr_h = int(card_base.height * scale_factor)
        c_img = card_base.resize((curr_w, curr_h), Image.Resampling.LANCZOS)
        
        # Focal center placement:
        # Title Y ~ 530, Card center Y ~ 820, Code Y ~ 1080, Play Y ~ 1180
        cx = center_x - curr_w // 2
        cy = int(600 + float_y)
        
        # Title above card
        ty = int(cy - th - 24)
        tx = center_x - tw // 2
        
        # Code directly below card
        code_y = int(cy + curr_h + 24)
        code_x = center_x - cw // 2
        
        # Play on Fortnite below code
        play_y = int(code_y + ch + 18)
        play_x = center_x - pw // 2
        
        # Draw Title (+1 MONEY ROLL)
        draw.text((tx, ty + 6), t_text, font=font_title, fill=(0, 0, 0, 180), stroke_width=8, stroke_fill=(0, 0, 0, 180))
        draw.text((tx, ty), t_text, font=font_title, fill=(255, 255, 255, 255), stroke_width=8, stroke_fill=(10, 20, 15, 255))
        
        # Drop shadow behind card
        spad = 48
        shadow = Image.new("RGBA", (curr_w + spad * 2, curr_h + spad * 2), (0, 0, 0, 0))
        draw_s = ImageDraw.Draw(shadow)
        draw_s.rounded_rectangle((spad, spad + 16, spad + curr_w, spad + curr_h + 16), radius=36, fill=(0, 0, 0, 220))
        shadow = shadow.filter(ImageFilter.GaussianBlur(26))
        
        frame.paste(shadow, (cx - spad, cy - spad), mask=shadow)
        frame.paste(c_img, (cx, cy), mask=c_img)
        
        # Draw Island Code (CODE: 3694-1078-5324) in High-Visibility Gold
        draw.text((code_x, code_y + 6), code_text, font=font_code, fill=(0, 0, 0, 180), stroke_width=8, stroke_fill=(0, 0, 0, 180))
        draw.text((code_x, code_y), code_text, font=font_code, fill=(255, 220, 32, 255), stroke_width=8, stroke_fill=(15, 25, 10, 255))
        
        # Draw PLAY ON FORTNITE
        draw.text((play_x, play_y + 6), play_text, font=font_sub, fill=(0, 0, 0, 180), stroke_width=6, stroke_fill=(0, 0, 0, 180))
        draw.text((play_x, play_y), play_text, font=font_sub, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=(15, 25, 10, 255))
        
        frame_out = os.path.join(frames_dir, f"endcard_{f:03d}.png")
        frame.save(frame_out, "PNG")
        
    print(f"Endcard frames successfully generated in {frames_dir} ({num_frames} frames).")

if __name__ == "__main__":
    create_endcard_frames(fps=30, duration=3.90)
