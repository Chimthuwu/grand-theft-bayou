"""Slice the Dead Swamp pixel sheets (clean alpha) into packed atlases + manifests.

Outputs into game/assets/sprites/:
  voodoo.png / .json   - the Voodoo Man enemy (walk / idle / attack / death)
  shroom.png / .json   - animated glowing mushroom cluster (decor)
  torch.png  / .json   - lit bamboo torch flame (decor light)
"""
import json, os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "game", "assets", "models", "swamp")
OUT = os.path.join(ROOT, "game", "assets", "sprites")


def grid_frames(path, cols, rows):
    im = Image.open(path).convert("RGBA")
    W, H = im.size
    cw, ch = W // cols, H // rows
    arr = np.array(im)
    out = []
    for r in range(rows):
        for c in range(cols):
            cell = arr[r * ch:(r + 1) * ch, c * cw:(c + 1) * cw]
            if cell[..., 3].max() <= 8:
                out.append(None)
                continue
            ys = np.where(cell[..., 3].max(1) > 8)[0]
            xs = np.where(cell[..., 3].max(0) > 8)[0]
            out.append(Image.fromarray(cell[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1], "RGBA"))
    return out


def pack(name, frames, anims):
    frames = [f for f in frames]
    live = [f for f in frames if f is not None]
    fw = max(f.width for f in live)
    fh = max(f.height for f in live)
    fw += fw % 2; fh += fh % 2

    # remap: only keep frames referenced by an anim, in first-seen order
    order = []
    for seq in anims.values():
        for i in seq:
            if i not in order and frames[i] is not None:
                order.append(i)
    remap = {orig: k for k, orig in enumerate(order)}

    atlas = Image.new("RGBA", (fw * len(order), fh), (0, 0, 0, 0))
    for k, orig in enumerate(order):
        im = frames[orig]
        atlas.paste(im, (k * fw + (fw - im.width) // 2, fh - im.height), im)
    atlas.save(os.path.join(OUT, f"{name}.png"))

    manifest = {
        "name": name,
        "anims": {k: [remap[i] for i in seq if i in remap] for k, seq in anims.items()},
        "frameSize": [fw, fh],
        "anchor": [0.5, 1.0],
        "count": len(order),
    }
    with open(os.path.join(OUT, f"{name}.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"  {name}: atlas {fw*len(order)}x{fh} ({len(order)} frames) {manifest['anims']}")


def main():
    os.makedirs(OUT, exist_ok=True)

    # (Voodoo Man dropped — off-theme for north Louisiana.)

    # Glowing mushroom cluster - 4x4, all frames loop
    sf = grid_frames(os.path.join(SRC, "shroomie.png"), 4, 4)
    pack("shroom", sf, {"glow": [i for i in range(16) if sf[i] is not None]})

    # Bamboo torch - 4x3; row 1 (idx 4-7) is the lit flame loop
    tf = grid_frames(os.path.join(SRC, "bambusfackel.png"), 4, 3)
    lit = [i for i in (4, 5, 6, 7) if tf[i] is not None] or [i for i in range(len(tf)) if tf[i] is not None][:4]
    pack("torch", tf, {"burn": lit})


if __name__ == "__main__":
    main()
