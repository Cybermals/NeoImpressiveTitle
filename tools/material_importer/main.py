from argparse import ArgumentParser
from pathlib import Path

import tomli_w

from ast import MaterialLibrary


# Parse command-line arguments
parser = ArgumentParser()
parser.add_argument("in_folder", type=Path, help="a folder of Ogre material scripts to import")
parser.add_argument("out_file", type=Path, help="the material library file to output")
args = parser.parse_args()

# Walk the source folder
mat_lib = MaterialLibrary()

for folder, folders, files in args.in_folder.walk():
    # Iterate over the .material files
    for file in files:
        # Build full path
        path = folder / file

        # Skip files which aren't .material files
        if path.suffix != ".material":
            continue

        # Open the file and parse it
        with open(path, "r") as f:
            print(f"Parsing '{path}'...")
            mat_lib.parse(f)

# Iterate over parsed materials
materials = {}

for name, mat in mat_lib:
    # Convert parsed material
    material = {
        "texture_stages": []
    }

    for i, technique in enumerate(mat):
        # We only support 1 technique per material
        if i > 0:
            print(f"{name}: WARNING: We only support 1 technique per material.")
            break

        # Iterate over passes
        for i, _pass in enumerate(technique):
            # We only support 1 pass per material
            if i > 0:
                print(f"{name}: WARNING: We only support 1 pass per technique.")
                break

            # Cull mode?
            if _pass.cull_hardware:
                material["cull"] = _pass.cull_hardware

            # Alpha rejection?
            if _pass.alpha_rejection:
                material["alpha_rejection"] = _pass.alpha_rejection

            # Ambient?
            if _pass.ambient:
                material["ambient"] = [float(n) for n in _pass.ambient.split(" ")]

            # Diffuse?
            if _pass.diffuse:
                material["diffuse"] = [float(n) for n in _pass.diffuse.split(" ")]

            # Specular?
            if _pass.specular:
                material["specular"] = [float(n) for n in _pass.specular.split(" ")]

            # Emissive?
            if _pass.emissive:
                material["emission"] = [float(n) for n in _pass.emissive.split(" ")]

            # Depth write?
            if _pass.depth_write:
                material["depth_write"] = _pass.depth_write == "on"

            # Scene blend?
            if _pass.scene_blend:
                material["blend_mode"] = _pass.scene_blend

            # Lighting?
            if _pass.lighting:
                material["lighting"] = _pass.lighting == "on"

            # Color write?
            if _pass.colour_write:
                material["color_write"] = _pass.colour_write == "on"

            # Depth check
            if _pass.depth_check:
                material["depth_test"] = _pass.depth_check == "on"

            # Depth func
            if _pass.depth_func:
                material["depth_func"] = _pass.depth_func

            # Polygon mode
            if _pass.polygon_mode:
                material["polygon_mode"] = _pass.polygon_mode

            # Iterate over texture units
            for i, texture_unit in enumerate(_pass):
                # Create texture stage
                texture_stage = {}

                # Texture?
                if texture_unit.texture:
                    texture_stage["texture"] = texture_unit.texture

                # Texture address mode?
                if texture_unit.tex_address_mode:
                    texture_stage["wrap"] = texture_unit.tex_address_mode

                # Filtering?
                if texture_unit.filtering:
                    texture_stage["filter"] = texture_unit.filtering

                # Scroll animation?
                if texture_unit.scroll_anim:
                    texture_stage["scroll"] = [float(n) for n in texture_unit.scroll_anim.split(" ")]

                # Rotate animation?
                if texture_unit.rotate_anim:
                    texture_stage["rotate"] = float(texture_unit.rotate_anim)

                # Wave transform?
                if texture_unit.wave_xform:
                    texture_stage["wave"] = texture_unit.wave_xform

                # Scale?
                if texture_unit.scale:
                    texture_stage["scale"] = texture_unit.scale

                # Add texture stage
                material["texture_stages"].append(texture_stage)

    # Add material
    materials[name] = material

# Write material library
with open(args.out_file, "wb") as f:
    tomli_w.dump(materials, f)
