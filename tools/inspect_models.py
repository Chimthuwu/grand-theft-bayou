"""Quick structural dump of GLB / GLTF files: meshes, nodes, materials, images, bbox-ish."""
import json, struct, sys, os

def read_glb(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:4] == b"glTF":
        jlen = struct.unpack("<I", data[12:16])[0]
        return json.loads(data[20:20 + jlen])
    return json.loads(data)  # .gltf

for path in sys.argv[1:]:
    try:
        j = read_glb(path)
    except Exception as e:
        print(f"{path}: ERR {e}"); continue
    meshes = [m.get("name") for m in j.get("meshes", [])]
    nodes = [n.get("name") for n in j.get("nodes", [])]
    mats = [m.get("name") for m in j.get("materials", [])]
    imgs = [i.get("name") or i.get("uri") for i in j.get("images", [])]
    # rough vertex count
    verts = 0
    for a in j.get("accessors", []):
        if a.get("type") == "VEC3":
            verts = max(verts, a.get("count", 0))
    print(f"\n=== {os.path.basename(path)} ===")
    print(f"  nodes({len(nodes)}): {nodes[:30]}")
    print(f"  meshes({len(meshes)}): {meshes[:30]}")
    print(f"  materials({len(mats)}): {mats[:30]}")
    print(f"  images({len(imgs)}): {imgs[:30]}")
    print(f"  ~maxVEC3 accessor count: {verts}")
