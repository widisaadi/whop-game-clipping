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

def create_glass_card(img_path, target_w=535, radius=32, border_w=3):
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
        g = int(220 * (1 - ratio) + 245 * ratio)
        b = int(255 * (1 - ratio) + 180 * ratio)
        draw_border.line([(0, y), (card_w, y)], fill=(r, g, b, 240))
        
    card.paste(border_layer, (0, 0), mask=bmask)
    
    glare = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw_g = ImageDraw.Draw(glare)
    pts = [(0, 0), (int(target_w * 0.70), 0), (int(target_w * 0.25), target_h), (0, target_h)]
    draw_g.polygon(pts, fill=(255, 255, 255, 28))
    
    img_with_glare = Image.alpha_composite(img, glare)
    card.paste(img_with_glare, (border_w, border_w), mask=mask)
    return card

def create_endcard_frames(fps=30, duration=3.90):
    W, H = 1080, 1920
    center_x = W // 2
    frames_dir = "temp/how_to_fisch/endcard_frames_clean"
    os.makedirs(frames_dir, exist_ok=True)
    
    num_frames = int(fps * duration)
    print(f"Generating {num_frames} clean minimalist endcard frames for How to Fisch ({duration:.2f}s @ {fps}fps)...")
    
    font_title = get_font(96, "impact.ttf")
    font_cta = get_font(96, "impact.ttf")
    
    t_text = "HOW TO FISCH"
    tbox = font_title.getbbox(t_text)
    tw, th = tbox[2] - tbox[0], tbox[3] - tbox[1]
    
    target_card_w = tw
    icon_path = "campaigns/how_to_fisch/assets/branding/how_to_fisch_official_icon.png"
    card_base = create_glass_card(icon_path, target_w=target_card_w, radius=32, border_w=3)
    
    cta_text = "SEARCH ON ROBLOX"
    bbox_cta = font_cta.getbbox(cta_text)
    ctaw = bbox_cta[2] - bbox_cta[0]
    
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
        
        cta_x = center_x - ctaw // 2
        cta_y = int(1180 + float_y)
        
        curr_w = int(card_base.width * scale_factor)
        curr_h = int(card_base.height * scale_factor)
        c_img = card_base.resize((curr_w, curr_h), Image.Resampling.LANCZOS)
        
        resting_card_bottom = 1180 - 24
        resting_cy = resting_card_bottom - card_base.height // 2
        
        cx = center_x - curr_w // 2
        cy = int(resting_cy - curr_h // 2 + float_y)
        
        resting_card_top = resting_card_bottom - card_base.height
        ty = int(resting_card_top - 24 - th + float_y)
        tx = center_x - tw // 2
        
        draw.text((tx, ty + 6), t_text, font=font_title, fill=(0, 0, 0, 160), stroke_width=6, stroke_fill=(0, 0, 0, 160))
        draw.text((tx, ty), t_text, font=font_title, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=(5, 10, 20, 255))
        
        spad = 48
        shadow = Image.new("RGBA", (curr_w + spad * 2, curr_h + spad * 2), (0, 0, 0, 0))
        draw_s = ImageDraw.Draw(shadow)
        draw_s.rounded_rectangle((spad, spad + 20, spad + curr_w, spad + curr_h + 20), radius=40, fill=(0, 0, 0, 230))
        shadow = shadow.filter(ImageFilter.GaussianBlur(28))
        
        frame.paste(shadow, (cx - spad, cy - spad), mask=shadow)
        frame.paste(c_img, (cx, cy), mask=c_img)
        
        draw.text((cta_x, cta_y + 6), cta_text, font=font_cta, fill=(0, 0, 0, 160), stroke_width=6, stroke_fill=(0, 0, 0, 160))
        draw.text((cta_x, cta_y), cta_text, font=font_cta, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=(5, 10, 20, 255))
        
        frame_out = os.path.join(frames_dir, f"endcard_{f:03d}.png")
        frame.save(frame_out, "PNG")
        
    print(f"Clean minimalist endcard frames generated in {frames_dir} ({num_frames} frames).")

if __name__ == "__main__":
    create_endcard_frames(fps=30, duration=3.90)
