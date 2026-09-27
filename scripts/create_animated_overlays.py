import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def get_font(size):
    p = "C:/Windows/Fonts/impact.ttf"
    if os.path.exists(p):
        return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def create_rounded_icon(src_path, size, radius=65, border_w=8, border_color=(255, 224, 64, 255)):
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

def create_3d_text_image(text, font_size, fill_color=(255, 225, 55, 255), depth=16):
    font = get_font(font_size)
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    pad_x, pad_y = 60, 60
    W = tw + pad_x * 2
    H = th + depth + pad_y * 2
    
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tx = pad_x - bbox[0]
    ty = pad_y - bbox[1]
    
    outline_w = max(5, int(font_size * 0.07))
    
    # 1. Ambient Drop Shadow
    shadow_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_s = ImageDraw.Draw(shadow_img)
    for dx in range(-outline_w - 4, outline_w + 5):
        for dy in range(-outline_w - 4, outline_w + 5):
            draw_s.text((tx + dx, ty + depth + 14 + dy), text, font=font, fill=(0, 0, 0, 200))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(14))
    img.paste(shadow_img, (0, 0), mask=shadow_img)
    
    # 2. Black outline for depth slices
    draw = ImageDraw.Draw(img)
    for d in range(depth, -1, -1):
        for ox in range(-outline_w, outline_w + 1):
            for oy in range(-outline_w, outline_w + 1):
                if ox*ox + oy*oy <= outline_w * outline_w + 1:
                    draw.text((tx + ox, ty + d + oy), text, font=font, fill=(0, 0, 0, 255))
                    
    # 3. Extrusion gradient
    for d in range(depth, 0, -1):
        ratio = d / depth
        r = int(150 * (1 - ratio * 0.45))
        g = int(90 * (1 - ratio * 0.45))
        b = int(12)
        draw.text((tx, ty + d), text, font=font, fill=(r, g, b, 255))
        
    # 4. Front Face
    draw.text((tx, ty), text, font=font, fill=fill_color)
    # Highlight
    draw.text((tx, ty - 1), text, font=font, fill=(255, 255, 210, 190))
    
    return img

def create_shadowed_icon(src_path, size, radius=65, border_w=8):
    framed = create_rounded_icon(src_path, size, radius, border_w)
    pad = 60
    total_w = framed.width + pad * 2
    total_h = framed.height + pad * 2
    
    img = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))
    draw_s = ImageDraw.Draw(shadow)
    draw_s.rounded_rectangle((pad, pad + 24, pad + framed.width, pad + framed.height + 24), radius=radius + border_w, fill=(0, 0, 0, 240))
    shadow = shadow.filter(ImageFilter.GaussianBlur(28))
    
    img.paste(shadow, (0, 0), mask=shadow)
    img.paste(framed, (pad, pad), mask=framed)
    return img

def ease_out_elastic(t):
    # t from 0.0 to 1.0 -> returns scale with spring overshoot
    if t <= 0: return 0.0
    if t >= 1: return 1.0
    p = 0.4
    return math.pow(2, -10 * t) * math.sin((t - p / 4) * (2 * math.pi) / p) + 1.0

def ease_out_back(t, s=1.70158):
    if t <= 0: return 0.0
    if t >= 1: return 1.0
    t -= 1
    return t * t * ((s + 1) * t + s) + 1.0

def ease_in_back(t, s=1.70158):
    if t <= 0: return 0.0
    if t >= 1: return 1.0
    return t * t * ((s + 1) * t - s)

def generate_intro_frames(out_dir, total_frames=72, fps=30):
    os.makedirs(out_dir, exist_ok=True)
    
    # Clean, luxury floating game icon for intro (no redundant text, subtitles already show title)
    icon_master = create_shadowed_icon("assets/how_to_fisch_official_icon.png", size=360, radius=60, border_w=8)
    
    center_x = 1080 // 2
    base_center_y = 620 # Sits comfortably above subtitle at y=980
    
    print(f"Rendering {total_frames} clean intro icon frames into {out_dir}...")
    for f in range(total_frames):
        canvas = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        
        if f < 10:
            pass
        elif 10 <= f < 22:
            # High-energy spring pop-in (12 frames = 0.40s)
            progress = (f - 10) / 11.0
            scale = ease_out_elastic(progress)
            
            w = max(1, int(icon_master.width * scale))
            h = max(1, int(icon_master.height * scale))
            scaled = icon_master.resize((w, h), Image.Resampling.BILINEAR)
            canvas.paste(scaled, (center_x - w // 2, base_center_y - h // 2), mask=scaled)
        elif 22 <= f < 52:
            # Smooth floating breathing idle
            idle_t = (f - 22) / 30.0
            y_offset = int(math.sin(idle_t * math.pi * 2 * 1.0) * 10)
            
            scaled = icon_master
            w, h = scaled.width, scaled.height
            canvas.paste(scaled, (center_x - w // 2, (base_center_y + y_offset) - h // 2), mask=scaled)
        elif 52 <= f < 60:
            # Fast smooth whoosh exit
            progress = (f - 52) / 8.0
            scale = max(0.01, 1.0 - ease_in_back(progress, s=1.8))
            w = max(1, int(icon_master.width * scale))
            h = max(1, int(icon_master.height * scale))
            scaled = icon_master.resize((w, h), Image.Resampling.BILINEAR)
            canvas.paste(scaled, (center_x - w // 2, base_center_y - h // 2), mask=scaled)
        else:
            pass
            
        frame_path = os.path.join(out_dir, f"intro_{f:03d}.png")
        canvas.save(frame_path, "PNG")

def generate_endcard_frames(out_dir, total_frames=158, fps=30):
    os.makedirs(out_dir, exist_ok=True)
    
    # Master elements for endcard: EXACTLY 1 Title and 1 Logo as requested!
    title_master = create_3d_text_image("HOW TO FISCH", font_size=115, fill_color=(255, 225, 55, 255), depth=18)
    icon_master = create_shadowed_icon("assets/how_to_fisch_official_icon.png", size=500, radius=75, border_w=10)
    
    center_x = 1080 // 2
    base_title_y = 440
    base_icon_y = 850
    
    print(f"Rendering {total_frames} endcard frames into {out_dir}...")
    for f in range(total_frames):
        canvas = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        
        # 1. Entrance (0 to 14 = 0.46s): Explosive elastic pop-in
        if f < 14:
            progress = f / 13.0
            scale = ease_out_elastic(progress)
            
            # Title
            tw = max(1, int(title_master.width * scale))
            th = max(1, int(title_master.height * scale))
            scaled_t = title_master.resize((tw, th), Image.Resampling.BILINEAR)
            canvas.paste(scaled_t, (center_x - tw // 2, base_title_y - th // 2), mask=scaled_t)
            
            # Icon (slight delay in spring for organic feel)
            progress_icon = max(0.0, (f - 2) / 12.0)
            scale_i = ease_out_elastic(progress_icon)
            iw = max(1, int(icon_master.width * scale_i))
            ih = max(1, int(icon_master.height * scale_i))
            scaled_i = icon_master.resize((iw, ih), Image.Resampling.BILINEAR)
            canvas.paste(scaled_i, (center_x - iw // 2, base_icon_y - ih // 2), mask=scaled_i)
            
        elif 14 <= f < 142:
            # Floating Idle breathing
            idle_t = (f - 14) / 30.0
            # Title floats gently
            t_y_off = int(math.sin(idle_t * math.pi * 2 * 0.8) * 8)
            canvas.paste(title_master, (center_x - title_master.width // 2, (base_title_y + t_y_off) - title_master.height // 2), mask=title_master)
            
            # Icon floats with slight counter-phase for rich 3D depth
            i_y_off = int(math.cos(idle_t * math.pi * 2 * 0.8) * 10)
            canvas.paste(icon_master, (center_x - icon_master.width // 2, (base_icon_y + i_y_off) - icon_master.height // 2), mask=icon_master)
            
        else:
            # Final 16 frames: Smooth exit
            progress = (f - 142) / 15.0
            scale = max(0.01, 1.0 - ease_in_back(progress, s=1.8))
            
            tw = max(1, int(title_master.width * scale))
            th = max(1, int(title_master.height * scale))
            scaled_t = title_master.resize((tw, th), Image.Resampling.BILINEAR)
            canvas.paste(scaled_t, (center_x - tw // 2, base_title_y - th // 2), mask=scaled_t)
            
            iw = max(1, int(icon_master.width * scale))
            ih = max(1, int(icon_master.height * scale))
            scaled_i = icon_master.resize((iw, ih), Image.Resampling.BILINEAR)
            canvas.paste(scaled_i, (center_x - iw // 2, base_icon_y - ih // 2), mask=scaled_i)
            
        frame_path = os.path.join(out_dir, f"endcard_{f:03d}.png")
        canvas.save(frame_path, "PNG")

if __name__ == "__main__":
    generate_intro_frames("temp/intro_frames", total_frames=72)
    generate_endcard_frames("temp/endcard_frames", total_frames=158)
    print("Done generating all animation frames!")
