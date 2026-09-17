# 3MF-Split

Zerlegt eine **3MF-Datei mit vielen Objekten** in **einzelne STL-Dateien** — ein Objekt pro Datei.

Typischer Anwendungsfall: Eine Slicer-3MF (Cura/PrusaSlicer/Bambu), die ein ganzes
Bauvorhaben mit allen Einzelteilen enthält, in druckfertige Einzel-STLs aufteilen.

## Nutzung

```bash
python3 split_3mf.py <datei.3mf> [--out ordner]
```

- `<datei.3mf>` — die 3MF-Eingabedatei (ZIP-Container)
- `--out ordner` — Zielordner für die STLs (Standard: `stl_out/`)

```bash
# Beispiel
python3 split_3mf.py adderini-v2.3mf --out ~/adderini
```

## Wie es funktioniert

3MF ist ein ZIP-Container. Die eigentlichen Meshes liegen als
`3D/Objects/<name>.model` (XML mit `<vertex>`/`<triangle>`-Elementen).
Das Script:

1. Öffnet die 3MF als ZIP
2. Liest jedes Objekt-Modell in `3D/Objects/`
3. Extrahiert Vertices + Triangles
4. Schreibt pro Objekt eine **ASCII-STL** (`solid … endsolid`)

**Kein Blender nötig** — reines Python (stdlib: `zipfile` + `xml`), läuft überall.

## Ausgabe

Pro Objekt eine Datei, benannt nach dem Quell-Modell:

```
stl_out/
├── main_stock_62.stl          (44.030 Vertices — großes Teil)
├── trigger_34.stl
├── magazine_left_23.stl
├── plate_110.stl              (32 Vertices — Kleinteil)
└── … (36 Dateien bei gemischten Projekten)
```

Hinweis: Die Koordinaten sind **original aus der 3MF** — Teile behalten ihre
Bauplatten-Position aus dem Slicer. Für druckfertige Einzelteile die STLs ggf.
mit `center/` (siehe Repo) zentrieren.

## Voraussetzungen

- Python 3.8+ (keine Drittanbieter-Packages)

## Lizenz

MIT — siehe [LICENSE](../LICENSE).