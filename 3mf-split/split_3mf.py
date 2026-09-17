#!/usr/bin/env python3
"""
3MF-Splitter: zerlegt eine 3MF mit mehreren Objekt-Modellen in einzelne STL-Dateien.
Liest jedes Mesh in 3D/Objects/*.model (3MF-Format), schreibt je eine ASCII-STL.

USAGE: python3 split_3mf.py <datei.3mf> [--out ordner]
"""
import zipfile, os, re, sys, xml.etree.ElementTree as ET

NS = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}

def mesh_from_model(data: bytes):
    """Extrahiert (vertices, triangles) aus einer 3MF-.model-Datei (ein Mesh je Datei)."""
    root = ET.fromstring(data)
    # Mesh kann unter <build> oder direkt <mesh> sein; meist <resources><object><mesh>
    for obj in root.iter(f"{{{NS['m']}}}object"):
        for mesh in obj.iter(f"{{{NS['m']}}}mesh"):
            verts, tris = [], []
            for v in mesh.iter(f"{{{NS['m']}}}vertex"):
                verts.append((float(v.get("x")), float(v.get("y")), float(v.get("z"))))
            for t in mesh.iter(f"{{{NS['m']}}}triangle"):
                tris.append((int(t.get("v1")), int(t.get("v2")), int(t.get("v3"))))
            if verts and tris:
                return verts, tris
    return None, None

def write_ascii_stl(path, verts, tris, name):
    with open(path, "w") as f:
        f.write(f"solid {name}\n")
        for v in verts:
            f.write(f"  vertex {v[0]:f} {v[1]:f} {v[2]:f}\n")
        for t in tris:
            f.write(f"  facet normal 0 0 0\n    outer loop\n")
            for idx in t:
                v = verts[idx]
                f.write(f"      vertex {v[0]:f} {v[1]:f} {v[2]:f}\n")
            f.write("    endloop\n  endfacet\n")
        f.write(f"endsolid {name}\n")

def main():
    if len(sys.argv) < 2:
        print("USAGE: split_3mf.py <datei.3mf> [--out ordner]"); sys.exit(1)
    src = sys.argv[1]
    out = sys.argv[sys.argv.index("--out")+1] if "--out" in sys.argv else "stl_out"

    z = zipfile.ZipFile(src)
    mods = sorted(n for n in z.namelist() if n.endswith(".model") and "/Objects/" in n)
    print(f"Objekte gefunden: {len(mods)}")
    os.makedirs(out, exist_ok=True)

    stats = []
    for mod in mods:
        data = z.read(mod)
        verts, tris = mesh_from_model(data)
        base = os.path.basename(mod).replace(".model", "").replace(".stl", "")
        # Bereinigen: doppelte Endung wie 'pistol body 1.stl_101' -> 'pistol body 1_101'
        base = re.sub(r"\.stl_\d+$", "_\\1", mod.split("/")[-1].replace(".model","")) if False else base
        safe = re.sub(r"[^\w\- ]+", "_", base).strip()
        if not verts or not tris:
            print(f"  ⚠️  {base}: kein Mesh (übersprungen)")
            continue
        outfile = os.path.join(out, f"{safe}.stl")
        write_ascii_stl(outfile, verts, tris, safe)
        stats.append((safe, len(verts), len(tris)))
        print(f"  ✅ {safe}.stl  ({len(verts)} Vertices, {len(tris)} Triangles)")

    print(f"\nFERTIG: {len(stats)} STL-Dateien nach '{out}/'")
    return stats

if __name__ == "__main__":
    main()