"""Draw the app icon (the site's brand mark: dark rounded square, white download arrow).

    python assets/make_icons.py

Writes assets/icon.png (1024px), assets/icon.ico (Windows) and assets/icon.icns (macOS).
"""
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SIZE = 1024
SS = 4  # supersampling for smooth edges


def draw(size: int) -> Image.Image:
    big = size * SS
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # macOS-style margin so the icon matches other Dock icons in size.
    m = round(big * 0.1)
    d.rounded_rectangle([m, m, big - m, big - m], radius=round(big * 0.2), fill=(17, 17, 17, 255))

    # Arrow from the 24x24 brand SVG: M12 4v11  M7 10l5 5 5-5  M5 20h14, stroke 2.4.
    box = big - 2 * m
    s = box / 24 * 0.62
    ox = m + (box - 24 * s) / 2
    oy = m + (box - 24 * s) / 2
    p = lambda x, y: (ox + x * s, oy + y * s)
    w = round(2.4 * s)
    white = (255, 255, 255, 255)
    for line in ([p(12, 4), p(12, 15)], [p(7, 10), p(12, 15), p(17, 10)], [p(5, 20), p(19, 20)]):
        d.line(line, fill=white, width=w, joint="curve")
        for x, y in line:  # round caps and joins
            d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=white)
    return img.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    icon = draw(SIZE)
    icon.save(os.path.join(HERE, "icon.png"))
    icon.save(os.path.join(HERE, "icon.ico"),
              sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    icon.save(os.path.join(HERE, "icon.icns"))
    print("wrote icon.png, icon.ico, icon.icns")
