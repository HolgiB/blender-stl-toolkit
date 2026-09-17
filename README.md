# Blender STL-Toolkit

Headless-Blender-Werkzeuge zur STL-Nachbearbeitung unter Linux (ohne GUI).

## Komponenten

### `center/` — Batch-Centering
Zentriert STL-Dateien (Bounding-Box-Zentrum auf Ursprung) für den 3D-Druck.

- `batch_center.py` — Python-Script: verschiebt jede STL so, dass die Bounding-Box zentriert liegt
- `center_stl.sh` — Wrapper für einzelne Datei

```bash
python3 center/batch_center.py <datei.stl>     # einzeln
python3 center/batch_center.py <ordner/ >      # alle im Ordner
```

### `repair/` — Batch-Reparatur
Repariert beschädigte/fehlerhafte STL-Dateien automatisch (Mesh-Repair via Blender).

- `batch_repair_stl_with_log_nocube.py` — Python-Script mit Logging
- `run_repair.sh` — Wrapper

```bash
python3 repair/batch_repair_stl_with_log_nocube.py <datei.stl>
```

### `3mf-split/` — 3MF in Einzel-STLs zerlegen
Trennt eine 3MF-Sammeldatei (z.B. Slicer-Export mit vielen Teilen) in **eine STL pro Objekt**.

```bash
python3 3mf-split/split_3mf.py <datei.3mf> --out ~/stl_out
```

Reines Python (stdlib) — kein Blender nötig. Details: [3mf-split/README.md](3mf-split/README.md).

## Voraussetzungen

- Blender (headless: `blender --background --python ...`), Python 3
- Linux

## Lizenz

MIT — siehe [LICENSE](LICENSE).

## Herkunft

Zusammenführung von `blender-center-stl` und `Blender---Batch-fixing-STL-files`.
