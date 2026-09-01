"""Build a 1200x630 Open Graph card for Discord/Twitter/etc from the cover art."""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COVER = os.path.join(ROOT, "game", "assets", "cover.png")
OUT = os.path.join(ROOT, "og.png")
W, H = 1200, 630

FI = "C:/Windows/Fonts/impact.ttf"
FA = "C:/Windows/Fonts/arialbd.ttf"
FT = "C:/Windows/Fonts/timesbi.ttf"

cover = Image.open(COVER).convert("RGB")

# --- background: blurred, darkened, zoomed cover ---
bg = cover.copy()
scale = max(W / bg.width, H / bg.height) * 1.15
bg = bg.resize((int(bg.width * scale), int(bg.height * scale)))
bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2,
              (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
bg = bg.filter(ImageFilter.GaussianBlur(14))
bg = ImageEnhance.Brightness(bg).enhance(0.42)
bg = ImageEnhance.Color(bg).enhance(0.8)
card = bg

# --- sharp cover pinned to the right ---
ch = H
cw = int(cover.width * ch / cover.height)
sharp = cover.resize((cw, ch))
card.paste(sharp, (W - cw, 0))
# feather the left edge of the cover into the bg
grad = Image.new("L", (220, H), 0)
gd = ImageDraw.Draw(grad)
for x in range(220):
    gd.line([(x, 0), (x, H)], fill=int(255 * (1 - x / 220)))
card.paste(bg.crop((W - cw - 220, 0, W - cw, H)), (W - cw - 220, 0), grad)

# --- left-hand text ---
d = ImageDraw.Draw(card)

def shadowed(xy, text, font, fill, sh=(0, 0, 0), off=4):
    d.text((xy[0] + off, xy[1] + off), text, font=font, fill=sh)
    d.text(xy, text, font=font, fill=fill)

title1 = ImageFont.truetype(FI, 104)
title2 = ImageFont.truetype(FT, 60)
tag = ImageFont.truetype(FA, 40)
sub = ImageFont.truetype(FA, 27)

x = 60
shadowed((x, 96),  "GRAND THEFT", title1, "#f4f1e6")
shadowed((x, 196), "BAYOU",       title1, "#f4f1e6")
shadowed((x + 4, 312), "Louisiana Stories", title2, "#e7a63b")

# accent rule
d.rectangle((x, 392, x + 150, 398), fill="#e7a63b")

shadowed((x, 430), "The Hogs are waiting for you.", tag, "#f0e8d8")
shadowed((x, 486), "Will you survive the Bayou?",  tag, "#ff5a3c")

d.text((x, 560), "CHATHAM  ·  MONROE  ·  RUSTON", font=sub, fill="#b9c4a8")

card.save(OUT)
card.save(os.path.join(ROOT, "og2.png"))  # cache-bust copy
print("wrote", OUT, "+ og2.png", card.size)
