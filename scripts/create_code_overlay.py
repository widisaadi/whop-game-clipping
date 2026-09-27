import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size, font_name="impact.ttf"):
    font_path = os.path.join("C:/Windows/Fonts", font_name)
    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            pass
    return ImageFont.load_default()

def create_code_badge():
    os.makedirs("temp/steal_a_seed", exist_ok=True)
    out_path = "temp/steal_a_seed/code_badge_35klikes.png"
    
    W, H = 820, 260
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Outer dark container with golden glow border
    draw.rounded_rectangle([0, 0, W, H], radius=24, fill=(15, 18, 25, 235), outline=(255, 215, 0, 255), width=5)
    
    # Header banner
    draw.rounded_rectangle([20, 18, W - 20, 68], radius=12, fill=(255, 180, 0, 240))
    f_header = get_font(34, "impact.ttf")
    header_text = "SECRET WORKING CODE"
    bbox_h = draw.textbbox((0, 0), header_text, font=f_header)
    tw_h = bbox_h[2] - bbox_h[0]
    draw.text(((W - tw_h) // 2, 24), header_text, fill=(0, 0, 0, 255), font=f_header)
    
    # Code box container
    draw.rounded_rectangle([35, 82, W - 35, 180], radius=16, fill=(28, 35, 48, 255), outline=(0, 255, 102, 255), width=4)
    f_code = get_font(68, "impact.ttf")
    code_text = "35KLIKES"
    bbox_c = draw.textbbox((0, 0), code_text, font=f_code)
    tw_c = bbox_c[2] - bbox_c[0]
    
    # Shadow and text for code
    draw.text(((W - tw_c) // 2 + 3, 94 + 3), code_text, fill=(0, 0, 0, 200), font=f_code)
    draw.text(((W - tw_c) // 2, 94), code_text, fill=(0, 255, 102, 255), font=f_code)
    
    # Reward subtext
    f_rew = get_font(38, "impact.ttf")
    rew_text = "REWARD: +$250,000 CASH!"
    bbox_r = draw.textbbox((0, 0), rew_text, font=f_rew)
    tw_r = bbox_r[2] - bbox_r[0]
    draw.text(((W - tw_r) // 2 + 2, 196 + 2), rew_text, fill=(0, 0, 0, 200), font=f_rew)
    draw.text(((W - tw_r) // 2, 196), rew_text, fill=(255, 255, 255, 255), font=f_rew)
    
    img.save(out_path)
    print(f"Created code badge: {out_path} ({W}x{H})")

if __name__ == "__main__":
    create_code_badge()
