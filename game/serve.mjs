// Minimal static file server for Escape The Bayou. No dependencies.
//   node serve.mjs [port]
import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { extname, join, normalize } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL(".", import.meta.url));
const PORT = Number(process.argv[2]) || 5173;

const TYPES = {
  ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript",
  ".css": "text/css", ".json": "application/json", ".png": "image/png",
  ".jpg": "image/jpeg", ".gif": "image/gif", ".svg": "image/svg+xml",
  ".glb": "model/gltf-binary", ".gltf": "model/gltf+json", ".bin": "application/octet-stream",
  ".fbx": "application/octet-stream", ".wav": "audio/wav", ".mp3": "audio/mpeg",
};

createServer(async (req, res) => {
  try {
    let path = decodeURIComponent(new URL(req.url, "http://x").pathname);
    if (path === "/") path = "/index.html";
    const full = normalize(join(ROOT, path));
    if (!full.startsWith(ROOT)) { res.writeHead(403).end("no"); return; }
    const info = await stat(full);
    if (info.isDirectory()) { res.writeHead(403).end("dir"); return; }
    const body = await readFile(full);
    res.writeHead(200, {
      "content-type": TYPES[extname(full).toLowerCase()] || "application/octet-stream",
      "cache-control": "no-cache",
    });
    res.end(body);
  } catch {
    res.writeHead(404).end("404");
  }
}).listen(PORT, () => console.log(`Escape The Bayou -> http://localhost:${PORT}`));
