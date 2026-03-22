"""
utils/favicon.py
Genera el favicon de la aplicación con PIL
"""
from PIL import Image, ImageDraw, ImageFont
import os

def generar_favicon(ruta: str = "assets/favicon.png", size: int = 64) -> str:
    os.makedirs(os.path.dirname(ruta) or ".", exist_ok=True)
    img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Fondo circular azul
    draw.ellipse([2, 2, size-2, size-2], fill=(27, 79, 114, 255))

    # Letra E centrada
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size//2)
    except Exception:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), "E", font=font)
    tw   = bbox[2] - bbox[0]
    th   = bbox[3] - bbox[1]
    x    = (size - tw) // 2
    y    = (size - th) // 2 - 2
    draw.text((x, y), "E", fill=(255, 255, 255, 255), font=font)

    img.save(ruta)
    return ruta
