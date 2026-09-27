import os
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

def draw_3d_text(draw_target, pos, text, font, fill_color=(255, 230, 70, 255), depth=14):
    tx, ty = pos
    outline_w = 7
    
    # 1. Ambient Drop Shadow
    shadow_img = Image.new("RGBA", draw_target.size, (0, 0, 0, 0))
    draw_s = ImageDraw.Draw(shadow_img)
    for dx in range(-outline_w - 4, outline_w + 5):
        for dy in range(-outline_w - 4, outline_w + 5):
            draw_s.text((tx + dx, ty + depth + 14 + dy), text, font=font, fill=(0, 0, 0, 180))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(12))
    draw_target.paste(shadow_img, (0, 0), mask=shadow_img)
    
    # 2. Black outline for extrusion
    draw = ImageDraw.Draw(draw_target)
    for d in range(depth, -1, -1):
        # Outline for this depth slice
        for ox in range(-outline_w, outline_w + 1):
            for oy in range(-outline_w, outline_w + 1):
                if ox*ox + oy*oy <= outline_w * outline_w + 1:
                    draw.text((tx + ox, ty + d + oy), text, font=font, fill=(0, 0, 0, 255))
    
    # 3. Extrusion gradient slices
    for d in range(depth, 0, -1):
        ratio = d / depth
        # Dark brown-gold gradient
        r = int(140 * (1 - ratio * 0.5))
        g = int(85 * (1 - ratio * 0.5))
        b = int(10)
        draw.text((tx, ty + d), text, font=font, fill=(r, g, b, 255))
        
    # 4. Front Face
    draw.text((tx, ty), text, font=font, fill=fill_color)
    
    # 5. Top highlight edge
    draw.text((tx, ty - 1), text, font=font, fill=(255, 255, 200, 180))

def main():
    os.makedirs("temp/test_3d", exist_ok=True)
    W, H = 1080, 1920
    img = Image.new("RGBA", (W, H), (15, 25, 45, 255)) # test backdrop
    
    center_x = W // 2
    
    # 1. 3D Title "HOW TO FISCH"
    font_title = get_font(105)
    t_text = "HOW TO FISCH"
    bbox = font_title.getbbox(t_text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = center_x - tw // 2
    ty = 420
    
    draw_3d_text(img, (tx, ty), t_text, font_title, fill_color=(255, 225, 55, 255), depth=16)
    
    # 2. Official Logo with deep ambient floating shadow
    icon_size = 480
    framed_icon = create_rounded_icon("assets/how_to_fisch_official_icon.png", icon_size, radius=70, border_w=10)
    
    pad = 60
    shadow = Image.new("RGBA", (framed_icon.width + pad * 2, framed_icon.height + pad * 2), (0, 0, 0, 0))
    draw_s = ImageDraw.Draw(shadow)
    draw_s.rounded_rectangle((pad, pad + 24, pad + framed_icon.width, pad + framed_icon.height + 24), radius=75, fill=(0, 0, 0, 240))
    shadow = shadow.filter(ImageFilter.GaussianBlur(28))
    
    icon_y = ty + th + 100
    img.paste(shadow, (center_x - shadow.width // 2, icon_y - pad), mask=shadow)
    img.paste(framed_icon, (center_x - framed_icon.width // 2, icon_y), mask=framed_icon)
    
    out_path = "temp/test_3d/test_endcard_frame.jpg"
    img.convert("RGB").save(out_path, "JPEG", quality=95)
    print(f"Generated test frame: {out_path}")

if __name__ == "__main__":
    main()
