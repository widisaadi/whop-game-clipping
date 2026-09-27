import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def get_font(size, name="impact.ttf"):
    font_paths = [
        f"C:/Windows/Fonts/{name}",
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

def create_rounded_card(src_path, target_w=640, radius=36, border_w=6, border_color=(255, 215, 0, 255)):
    img = Image.open(src_path).convert("RGBA")
    aspect = img.height / img.width
    target_h = int(target_w * aspect)
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    scale = 4
    mask = Image.new("L", (target_w * scale, target_h * scale), 0)
    draw_m = ImageDraw.Draw(mask)
    draw_m.rounded_rectangle((0, 0, target_w * scale, target_h * scale), radius=radius * scale, fill=255)
    mask = mask.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    rounded = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    rounded.paste(img, (0, 0), mask=mask)
    
    fw = target_w + border_w * 2
    fh = target_h + border_w * 2
    framed = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
    
    bmask = Image.new("L", (fw * scale, fh * scale), 0)
    draw_b = ImageDraw.Draw(bmask)
    draw_b.rounded_rectangle((0, 0, fw * scale, fh * scale), radius=(radius + border_w) * scale, fill=255)
    bmask = bmask.resize((fw, fh), Image.Resampling.LANCZOS)
    
    blayer = Image.new("RGBA", (fw, fh), border_color)
    framed.paste(blayer, (0, 0), mask=bmask)
    framed.paste(rounded, (border_w, border_w), mask=mask)
    return framed

def create_intro_badge():
    W, H = 1080, 1920
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    center_x = W // 2
    
    # Pill: "NEW ROBLOX GAME"
    font_pill = get_font(28, "impact.ttf")
    pill_text = "🔥 NEW ROBLOX GAME 🔥"
    pbox = font_pill.getbbox(pill_text)
    pw, ph = pbox[2] - pbox[0], pbox[3] - pbox[1]
    
    pill_w = pw + 48
    pill_h = ph + 24
    pill_x = center_x - pill_w // 2
    pill_y = 360
    
    draw.rounded_rectangle((pill_x, pill_y + 4, pill_x + pill_w, pill_y + pill_h + 4), radius=pill_h // 2, fill=(0, 0, 0, 160))
    draw.rounded_rectangle((pill_x, pill_y, pill_x + pill_w, pill_y + pill_h), radius=pill_h // 2, fill=(255, 45, 65, 255))
    draw.rounded_rectangle((pill_x, pill_y, pill_x + pill_w, pill_y + pill_h), radius=pill_h // 2, outline=(255, 220, 220, 255), width=2)
    draw.text((center_x - pw // 2, pill_y + 10), pill_text, font=font_pill, fill=(255, 255, 255, 255))
    
    # Official Card
    card_img = create_rounded_card("campaigns/tongue_escape/assets/branding/000.png", target_w=580, radius=32, border_w=6)
    
    # Shadow
    shadow_pad = 40
    sw, sh = card_img.width + shadow_pad * 2, card_img.height + shadow_pad * 2
    shadow = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw_s = ImageDraw.Draw(shadow)
    draw_s.rounded_rectangle((shadow_pad, shadow_pad + 12, shadow_pad + card_img.width, shadow_pad + card_img.height + 12), radius=36, fill=(0, 0, 0, 220))
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))
    
    card_y = pill_y + pill_h + 20
    img.paste(shadow, (center_x - shadow.width // 2, card_y - shadow_pad), mask=shadow)
    img.paste(card_img, (center_x - card_img.width // 2, card_y), mask=card_img)
    
    out_path = "temp/tongue_escape/intro_badge.png"
    img.save(out_path, "PNG")
    print(f"Created {out_path}")
    return out_path

def create_endcard_frames(fps=30, duration=4.74):
    W, H = 1080, 1920
    center_x = W // 2
    frames_dir = "temp/tongue_escape/endcard_frames"
    os.makedirs(frames_dir, exist_ok=True)
    
    num_frames = int(fps * duration)
    print(f"Generating {num_frames} animated 3D endcard frames ({duration:.2f}s @ {fps}fps)...")
    
    font_badge = get_font(28, "impact.ttf")
    font_title = get_font(92, "impact.ttf")
    font_sub = get_font(34, "bahnschrift.ttf")
    font_btn = get_font(56, "impact.ttf")
    font_bio = get_font(32, "impact.ttf")
    
    card_base = create_rounded_card("campaigns/tongue_escape/assets/branding/000.png", target_w=620, radius=36, border_w=8)
    
    for f in range(num_frames):
        t = f / fps
        # Smooth pop-in scale for first 0.4s, then gentle floating sine wave
        if t < 0.4:
            scale_factor = 0.5 + 0.5 * math.sin((t / 0.4) * (math.pi / 2))
        else:
            scale_factor = 1.0 + 0.02 * math.sin((t - 0.4) * 3.5)
            
        float_y = 6 * math.sin(t * 3.0)
        
        frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        
        # 1. Top Pill Badge: "NEW ROBLOX EXPERIENCE"
        b_text = "🔥 MUST PLAY ON ROBLOX 🔥"
        bbox = font_badge.getbbox(b_text)
        bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        badge_w, badge_h = bw + 54, bh + 24
        badge_x, badge_y = center_x - badge_w // 2, 230
        
        draw.rounded_rectangle((badge_x, badge_y + 6, badge_x + badge_w, badge_y + badge_h + 6), radius=badge_h // 2, fill=(0, 0, 0, 160))
        draw.rounded_rectangle((badge_x, badge_y, badge_x + badge_w, badge_y + badge_h), radius=badge_h // 2, fill=(255, 45, 65, 255))
        draw.rounded_rectangle((badge_x, badge_y, badge_x + badge_w, badge_y + badge_h), radius=badge_h // 2, outline=(255, 220, 220, 255), width=2)
        draw.text((center_x - bw // 2, badge_y + 11), b_text, font=font_badge, fill=(255, 255, 255, 255))
        
        # 2. Main Title: "+1 TONGUE ESCAPE"
        t_text = "+1 TONGUE ESCAPE"
        tbox = font_title.getbbox(t_text)
        tw, th = tbox[2] - tbox[0], tbox[3] - tbox[1]
        tx, ty = center_x - tw // 2, badge_y + badge_h + 20
        
        for dx in range(-6, 7):
            for dy in range(-6, 7):
                if abs(dx) + abs(dy) > 0:
                    draw.text((tx + dx, ty + dy), t_text, font=font_title, fill=(0, 0, 0, 255))
        draw.text((tx, ty + 8), t_text, font=font_title, fill=(180, 120, 0, 255))
        draw.text((tx, ty), t_text, font=font_title, fill=(255, 224, 64, 255))
        
        # 3. Subtitle
        s_text = "GROW YOUR TONGUE TO SURVIVE!"
        sbox = font_sub.getbbox(s_text)
        sw, sh = sbox[2] - sbox[0], sbox[3] - sbox[1]
        sx, sy = center_x - sw // 2, ty + th + 24
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if abs(dx) + abs(dy) > 0:
                    draw.text((sx + dx, sy + dy), s_text, font=font_sub, fill=(0, 0, 0, 220))
        draw.text((sx, sy), s_text, font=font_sub, fill=(220, 235, 255, 255))
        
        # 4. Scaled Card with Floating Shadow
        curr_w = int(card_base.width * scale_factor)
        curr_h = int(card_base.height * scale_factor)
        c_img = card_base.resize((curr_w, curr_h), Image.Resampling.LANCZOS)
        
        card_x = center_x - curr_w // 2
        card_y = int(sy + sh + 36 + float_y)
        
        # Shadow
        spad = 30
        cshadow = Image.new("RGBA", (curr_w + spad * 2, curr_h + spad * 2), (0, 0, 0, 0))
        draw_cs = ImageDraw.Draw(cshadow)
        draw_cs.rounded_rectangle((spad, spad + 14, spad + curr_w, spad + curr_h + 14), radius=40, fill=(0, 0, 0, 200))
        cshadow = cshadow.filter(ImageFilter.GaussianBlur(20))
        
        frame.paste(cshadow, (card_x - spad, card_y - spad), mask=cshadow)
        frame.paste(c_img, (card_x, card_y), mask=c_img)
        
        # 5. Big CTA Button: "PLAY FREE ON ROBLOX"
        btn_w, btn_h = 760, 120
        bx = center_x - btn_w // 2
        by = card_y + curr_h + 40
        
        # Button shadow
        draw.rounded_rectangle((bx + 4, by + 10, bx + btn_w + 4, by + btn_h + 10), radius=32, fill=(0, 0, 0, 160))
        # Button body
        draw.rounded_rectangle((bx, by, bx + btn_w, by + btn_h), radius=32, fill=(0, 204, 102, 255), outline=(255, 255, 255, 255), width=4)
        
        # Play triangle
        tri_x = bx + 55
        tri_y = by + 38
        tri_pts = [(tri_x, tri_y), (tri_x + 36, tri_y + 22), (tri_x, tri_y + 44)]
        draw.polygon(tri_pts, fill=(255, 255, 255, 255))
        
        # Button text
        btn_text = "PLAY FREE ON ROBLOX"
        bbox_btn = font_btn.getbbox(btn_text)
        btn_tw = bbox_btn[2] - bbox_btn[0]
        btn_tx = bx + 110 + (btn_w - 110 - btn_tw) // 2
        draw.text((btn_tx, by + 28), btn_text, font=font_btn, fill=(255, 255, 255, 255))
        
        # 6. Bio Link Pill: "👉 LINK IS IN BIO 👈"
        bio_text = "👉 GAME LINK IS IN MY BIO 👈"
        bbox_bio = font_bio.getbbox(bio_text)
        biow, bioh = bbox_bio[2] - bbox_bio[0], bbox_bio[3] - bbox_bio[1]
        biox = center_x - biow // 2
        bioy = by + btn_h + 30
        
        draw.rounded_rectangle((biox - 30, bioy - 10, biox + biow + 30, bioy + bioh + 12), radius=24, fill=(0, 0, 0, 180), outline=(255, 215, 0, 255), width=2)
        draw.text((biox, bioy), bio_text, font=font_bio, fill=(255, 224, 64, 255))
        
        frame_out = os.path.join(frames_dir, f"endcard_{f:03d}.png")
        frame.save(frame_out, "PNG")
        
    print(f"Endcard frames generated in {frames_dir} ({num_frames} frames).")

if __name__ == "__main__":
    os.makedirs("temp/tongue_escape", exist_ok=True)
    create_intro_badge()
    create_endcard_frames(fps=30, duration=4.74)
