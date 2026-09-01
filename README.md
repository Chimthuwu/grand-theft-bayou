# Grand Theft Bayou: Louisiana Stories

A joke / experiment GTA-style game set in north Louisiana — **Chatham → Monroe → Ruston**
along US-167. Drive down the highway, jack cars, rob gas cans off the wrecks and the
strip malls, dodge Feral Hogs / Rednecks / Hoodrats, and get to the truck past the
Ruston line.

Vanilla **Three.js** (loaded from a CDN via import map), no build step.

## Run

```sh
cd game
node serve.mjs 8899
```

Open <http://localhost:8899> and hit **Start the story**.

### Controls

| | |
|---|---|
| **WASD** | drive / walk |
| **F** | jack a car / get out / enter the truck |
| **Shift** | sprint on foot · handbrake in a car |
| **Space / left click** | shoot |
| **Q / E** or **right-drag** | rotate the camera |
| **M** | mute music |

## Layout

```
game/
  index.html        menu + HUD
  serve.mjs         tiny zero-dependency static server
  src/
    main.js         everything — world build, driving, enemies, wanted system
    sprite.js       billboard sprite / atlas animation
  assets/
    sprites/        pixel-art atlases (built by tools/slice_*.py)
    models/         gltf / glb / fbx landmarks, vehicles, kit
    audio/ cover.png
tools/
    slice_sprites.py   APIgqp.jpg / S4KKpl.jpg  -> redneck / oldman atlases
    slice_swamp.py     Dead Swamp sheets        -> shroom / torch atlases
    inspect_models.py   dump gltf/glb structure
TODO.md               working notes / roadmap
```

## Assets

Built from third-party asset packs (itch.io / asset-store low-poly + pixel-art
packs). Licenses vary per pack; this repo is a personal experiment. Credits are
tracked in `TODO.md`. The original archives are **not** committed (see `.gitignore`).

The `cops` / wanted system stays dormant until you kill 12 Rednecks/Hoodrats
(`HEAT_KILLS` in `main.js`).
