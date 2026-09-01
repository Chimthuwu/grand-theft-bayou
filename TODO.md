# GRAND THEFT BAYOU: Louisiana Stories — TODO / progress

GTA-style joke game. North Louisiana: **Chatham → Monroe → Ruston** along US-167.
Built from dropped asset packs. Vanilla Three.js (CDN import map), no build step.

## How to run

```
cd game
node serve.mjs 8899          # NOT 5173 — that's the Euclydia dev server
```
http://localhost:8899 → **Start the story**.

Controls: **WASD** drive/walk · **F** jack & exit vehicle (also enter truck) ·
**Shift** sprint / handbrake · **Space/Click** shoot · **Q/E** rotate camera · **M** music.

## Status — PLAYABLE

- **Title screen** shows the provided cover art (`assets/cover.png`).
- **Theme music** (`assets/audio/theme.mp3`) loops on Start, M to mute.
- **Driving**: 25 drivable vehicles (PSX pack + Designersoup cars incl. the DeLorean
  at the pumps). Arcade handling, chase cam, handbrake, road-kill.
- **On foot**: redneck billboard sprite, auto-aim rifle, sprint/stamina.
- **Enemies** (only these three): **Feral Hogs** (3D, charge), **Rednecks** & **Hoodrats**
  (billboard sprites). 16 spawned, herding you north. Voodoo Man fully removed.
- **Everything lines US-167** now — one continuous strip you drive past:
  `LANDMARKS` list in main.js = **9 Popeyes** + the **6twelve** (right at the spawn) +
  Tony's Pizza + the taco stand (`Tacos.glb`), alternating sides, each with a car
  park + parked cars + an **asphalt apron linking it to the highway**.
  - *Chatham* (spawn): trailer park (stylised mobile homes + 4 pedestrian FBX),
    "Bienvenue en Louisiane" sign, a few torches/shrooms, 2 shacks.
  - *Ruston* (north): two rows of `Buildings.glb` shopfronts, asphalt lot, the truck.
  - Water towers CHATHAM / MONROE / RUSTON.
- **Real models now used** for the key businesses:
  - **6twelve** — `sixtwelve/6twelve.fbx` (the small 1 MB pack, not the old 960-node one).
  - **BurgerPiz** — `burgerpiz/BurgerPiz.glb`, filtered to just the `BurgerPiz_*` meshes
    (dropped its background city + interior clutter → 9 meshes).
  - **Taco stand** — `Tacos.glb`, filtered to the stand + food meshes.
  - Stylised `makeSixtwelve` / `makePizzeria` kept as fallbacks if a load fails.
- **Shacks Shanties Sheds** pack (blend-only) → stylised `makeShed / makeBarrel /
  makePallet / makeFence` using the pack's corrugated / chainlink / barrel / pallet
  textures. Built a fenced **junkyard** (46, 92) + sheds in the trailer park.
- GLB mesh-culling (`loadGLB` cullRe/keepRe) took the scene from ~2200 meshes to ~930.
- Torch/shroom "weird orange orb" halos removed; torches near spawn have real lights.
- Redneck/Hoodrat sprite tints softened (were near-solid red/blue at distance).
- **Pickups**: 4-of-5 gas cans (goal), Popeyes buckets (+28 HP), $ cash counter.
- **Wanted / Sheriff**: dormant until you kill **12 Rednecks/Hoodrats combined**
  (`HEAT_KILLS` in main.js), then it kicks in at 2 stars and cruisers spawn.
- Win = 4 cans + reach truck → "left the parish". Die → **WASTED**. (BUSTED wired for later.)

## Asset usage

| pack | in game? |
|---|---|
| `APIgqp.jpg` / `S4KKpl.jpg` | player + Redneck / Hoodrat sprites (`tools/slice_sprites.py`) |
| `Dead Swamp` | glowing mushrooms, bamboo torches (`tools/slice_swamp.py`). Voodoo-man sprite dropped entirely. |
| `PSX_Vehicle_Pack` | wrecks, parked cars, the escape truck, sheriff proto |
| `Designersoup Low Poly Car Pack` | drivable cars incl. DeLorean |
| `Gas_station` (6twelve) | strip landmark (FBX) |
| `Buildings.glb` | Ruston shopfronts |
| `Tacos.glb` | taco truck on the strip |
| `Trailer_Park` characters | pedestrians |
| `Urban_Modular_Demo` | shack walls, streetlamp, stop sign |
| `TownTileSet` | copied, not wired (GLB has no embedded textures) |
| **NOT USED (off-theme / unusable):** Downtown City MegaKit (dense city — dropped), Retro PSX Mansion, Trashville, Pizzeria_Scene.glb (100 MB), "Shacks Shanties Sheds" (.blend only), Modular Village / RCC / azul / PP furniture (2D tilesets) |

## Now / Next / Later

**Now**
- [ ] Playtest in a *foreground* window (automation tab can't run the loop).
- [ ] Taco stand (`Tacos.glb`) is ~358 meshes — biggest single draw cost. Swap for a
      stylised taco truck if framerate suffers.
- [ ] Torch sprites still read as carved poles more than flames — bigger flame frame or a 3D torch.
- [ ] Tune car handling + enemy aggro while driving.

**Next**
- [ ] Make the Sheriff escapable — currently no give-up timer once they're active.
      Tune `HEAT_KILLS`, spawn count, ram damage.
- [ ] Mission structure ("Louisiana Stories" — a few numbered jobs per town).
- [ ] Minimap / waypoint arrow (easy to get lost on the highway).
- [ ] Distinct 3D or sprite art for Hoodrat (currently the old-man sheet tinted).
- [ ] Wire Trailer_Park.fbx scene + Tacos_Props / Pizzeria props as set dressing.
- [ ] Airboat (cover art!) for the bayou stretches.

**Later**
- [ ] Actually drive the escape truck out instead of instant win.
- [ ] Radio stations / more tracks.
- [ ] Pedestrian AI (walk, flee, get in cars).

## Open questions
- Cops: how weak? (spawn distance, count, give-up timer)
- Map scale feel OK, or tighten the three towns closer together?
