"""
Slice the pixel-art reference sheets (APIgqp.jpg = redneck, S4KKpl.jpg = old man)
into clean, transparent, uniformly-anchored animation frames + a JSON manifest.

Output: game/assets/sprites/<name>/<anim>_<i>.png  and  game/assets/sprites/<name>.json
"""
import json
import os
import sys

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "game", "assets", "sprites")

KEY = np.array([179, 175, 189])          # sheet background colour
KEY_TOL = 42                             # distance below which a pixel is background
LABEL_MAX_X = 380                        # everything left of this is the row label
ROW_BANDS = [                            # (name, y0, y1) hand-tuned from band analysis
    ("attack", 55, 255),
    ("death", 285, 460),
    ("hurt", 492, 668),
    ("idle", 706, 885),
    ("walk", 908, 1094),
]
COL_GAP = 6          # >= this many empty columns => frame boundary
MIN_FRAME_W = 10     # ignore slivers


def find_bands(flags, gap):
    bands, start, run = [], None, 0
    for i, on in enumerate(flags):
        if on:
            if start is None:
                start = i
            run = 0
        else:
            if start is not None:
                run += 1
                if run >= gap:
                    bands.append((start, i - run + 1))
                    start = None
    if start is not None:
        bands.append((start, len(flags)))
    return bands


def slice_sheet(path, name):
    rgb = np.array(Image.open(path).convert("RGB")).astype(int)
    dist = np.abs(rgb - KEY).sum(2)
    keylike = dist < KEY_TOL * 3     # looks like the background colour

    # background = keylike pixels connected to the image border (flood fill),
    # so interior grey clothing is NOT punched out.
    bg = np.zeros_like(keylike)
    bg[0, :] |= keylike[0, :]
    bg[-1, :] |= keylike[-1, :]
    bg[:, 0] |= keylike[:, 0]
    bg[:, -1] |= keylike[:, -1]
    while True:
        grown = bg.copy()
        grown[1:, :] |= bg[:-1, :]
        grown[:-1, :] |= bg[1:, :]
        grown[:, 1:] |= bg[:, :-1]
        grown[:, :-1] |= bg[:, 1:]
        grown &= keylike
        if np.array_equal(grown, bg):
            break
        bg = grown
    fg = ~bg

    h, w = fg.shape
    manifest = {"name": name, "anims": {}, "frameSize": [0, 0], "anchor": [0.5, 1.0]}
    frames = []   # (anim, idx, PIL image, bbox w, h)

    for anim, y0, y1 in ROW_BANDS:
        y0, y1 = max(0, y0), min(h, y1)
        rowfg = fg[y0:y1].copy()
        rowfg[:, :LABEL_MAX_X] = False
        col_on = rowfg.any(0)
        col_bands = [(a, b) for a, b in find_bands(col_on, COL_GAP) if b - a >= MIN_FRAME_W]

        idx = 0
        for a, b in col_bands:
            sub_fg = rowfg[:, a:b]
            ys = np.where(sub_fg.any(1))[0]
            if len(ys) == 0:
                continue
            ry0, ry1 = ys[0], ys[-1] + 1
            crop_rgb = rgb[y0 + ry0:y0 + ry1, a:b].astype(np.uint8)
            crop_mask = sub_fg[ry0:ry1]

            # drop the solid-red "placeholder" silhouettes on the hurt/death rows
            r, g, bl = crop_rgb[..., 0], crop_rgb[..., 1], crop_rgb[..., 2]
            redish = (r > 150) & (g < 90) & (bl < 90) & crop_mask
            if crop_mask.sum() and redish.sum() / crop_mask.sum() > 0.55:
                continue

            rgba = np.dstack([crop_rgb, (crop_mask * 255).astype(np.uint8)])
            img = Image.fromarray(rgba, "RGBA")
            frames.append((anim, idx, img))
            idx += 1
        manifest["anims"][anim] = idx
        print(f"  {name}/{anim}: {idx} frames")

    # uniform canvas: max frame w/h, anchored bottom-centre
    fw = max(im.width for _, _, im in frames)
    fh = max(im.height for _, _, im in frames)
    fw += fw % 2
    fh += fh % 2
    manifest["frameSize"] = [fw, fh]

    # pack every frame into one horizontal-strip atlas
    n = len(frames)
    atlas = Image.new("RGBA", (fw * n, fh), (0, 0, 0, 0))
    layout = {}          # anim -> list of column indices
    for col, (anim, idx, im) in enumerate(frames):
        x = col * fw + (fw - im.width) // 2
        y = fh - im.height
        atlas.paste(im, (x, y), im)
        layout.setdefault(anim, []).append(col)
    atlas.save(os.path.join(OUT, f"{name}.png"))
    manifest["anims"] = layout
    manifest["count"] = n

    with open(os.path.join(OUT, f"{name}.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"  -> {name}: atlas {fw * n}x{fh} ({n} frames)  {layout}")


def main():
    os.makedirs(OUT, exist_ok=True)
    slice_sheet(os.path.join(ROOT, "APIgqp.jpg"), "redneck")
    slice_sheet(os.path.join(ROOT, "S4KKpl.jpg"), "oldman")


if __name__ == "__main__":
    sys.exit(main())
