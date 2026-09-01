import * as THREE from "three";

const loader = new THREE.TextureLoader();

export function loadAtlas(name) {
  return Promise.all([
    fetch(`./assets/sprites/${name}.json`).then((r) => r.json()),
    new Promise((res, rej) => loader.load(`./assets/sprites/${name}.png`, res, undefined, rej)),
  ]).then(([manifest, tex]) => {
    tex.magFilter = THREE.NearestFilter;
    tex.minFilter = THREE.NearestFilter;
    tex.generateMipmaps = false;
    tex.colorSpace = THREE.SRGBColorSpace;
    return { manifest, tex };
  });
}

/**
 * A camera-facing animated sprite driven by a horizontal-strip atlas.
 * worldHeight = how tall the sprite should be in metres.
 */
export class AnimatedSprite extends THREE.Object3D {
  constructor({ manifest, tex }, worldHeight = 2) {
    super();
    this.manifest = manifest;
    this.count = manifest.count;
    const [fw, fh] = manifest.frameSize;
    this.aspect = fw / fh;

    this.texture = tex.clone();
    this.texture.needsUpdate = true;
    this.texture.repeat.set(1 / this.count, 1);

    this.material = new THREE.MeshBasicMaterial({
      map: this.texture,
      transparent: true,
      alphaTest: 0.5,
      side: THREE.DoubleSide,
      depthWrite: true,
    });

    const h = worldHeight;
    const w = h * this.aspect;
    this.mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, h), this.material);
    this.mesh.position.y = h / 2;
    this.mesh.renderOrder = 1;
    this.add(this.mesh);

    // soft blob shadow
    this.blob = new THREE.Mesh(
      new THREE.CircleGeometry(w * 0.34, 16),
      new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.32, depthWrite: false })
    );
    this.blob.rotation.x = -Math.PI / 2;
    this.blob.position.y = 0.03;
    this.add(this.blob);

    this.anim = null;
    this.frames = [];
    this.time = 0;
    this.fps = 8;
    this.loop = true;
    this.finished = false;
    this.flip = 1;
    this.play(Object.keys(manifest.anims)[0]);
  }

  play(anim, { fps = 8, loop = true, force = false } = {}) {
    if (this.anim === anim && !force) return;
    if (!this.manifest.anims[anim]) return;
    this.anim = anim;
    this.frames = this.manifest.anims[anim];
    this.fps = fps;
    this.loop = loop;
    this.time = 0;
    this.finished = false;
    this._apply(0);
  }

  _apply(i) {
    const col = this.frames[i];
    this.texture.offset.x = col / this.count;
  }

  setFlip(dir) {
    // dir < 0 -> face left
    this.flip = dir < 0 ? -1 : 1;
  }

  setTint(hex) {
    this.material.color.setHex(hex);
  }

  update(dt, camera) {
    this.time += dt;
    const total = this.frames.length;
    let i = Math.floor(this.time * this.fps);
    if (i >= total) {
      if (this.loop) i %= total;
      else { i = total - 1; this.finished = true; }
    }
    this._apply(i);

    // face camera on Y only, keep upright, apply horizontal flip
    if (camera) {
      const dx = camera.position.x - this.position.x;
      const dz = camera.position.z - this.position.z;
      this.mesh.rotation.y = Math.atan2(dx, dz);
    }
    this.mesh.scale.x = this.flip;
  }
}
