import bpy
import os
from mathutils import Vector

# ============================================================
# CONFIG
# ============================================================

INPUT_DIR = "/home/hb/data/3D Druck/1 - Center STL/in"
OUTPUT_DIR = "/home/hb/data/3D Druck/1 - Center STL/out"

RECURSIVE = True
EXPORT_BINARY_STL = True

# ============================================================
# HELPERS
# ============================================================


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)



def get_all_stl_files(root):
    files = []

    if RECURSIVE:
        for path, _, filenames in os.walk(root):
            for f in filenames:
                if f.lower().endswith('.stl'):
                    files.append(os.path.join(path, f))
    else:
        for f in os.listdir(root):
            if f.lower().endswith('.stl'):
                files.append(os.path.join(root, f))

    return files



def import_stl(path):
    bpy.ops.wm.stl_import(filepath=path)



def export_stl(path):
    bpy.ops.wm.stl_export(
        filepath=path,
        export_selected_objects=True,
        ascii_format=not EXPORT_BINARY_STL,
    )



def get_imported_objects(before_names):
    return [obj for obj in bpy.data.objects if obj.name not in before_names]



def center_object(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Bounding box center in world coordinates
    bbox = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

    center = sum(bbox, Vector()) / 8

    # STRICT TRANSFORM ONLY
    # move object so bbox center is at world origin
    obj.location -= center

    obj.select_set(False)



def ensure_output_path(input_file):
    rel = os.path.relpath(input_file, INPUT_DIR)
    out = os.path.join(OUTPUT_DIR, rel)

    os.makedirs(os.path.dirname(out), exist_ok=True)

    return out


# ============================================================
# MAIN
# ============================================================


os.makedirs(OUTPUT_DIR, exist_ok=True)

stl_files = get_all_stl_files(INPUT_DIR)

print(f"Found {len(stl_files)} STL files")

for idx, stl in enumerate(stl_files, start=1):
    print(f"[{idx}/{len(stl_files)}] Processing: {stl}")

    clear_scene()

    before = set(obj.name for obj in bpy.data.objects)

    try:
        import_stl(stl)

        imported = get_imported_objects(before)

        if not imported:
            print(f"[WARN] No objects imported: {stl}")
            continue

        for obj in imported:
            center_object(obj)

        # select imported objects for export
        bpy.ops.object.select_all(action='DESELECT')

        for obj in imported:
            obj.select_set(True)

        out = ensure_output_path(stl)

        export_stl(out)

        print(f"[OK] Exported: {out}")

    except Exception as e:
        print(f"[ERROR] Failed processing {stl}")
        print(e)

print("Done")