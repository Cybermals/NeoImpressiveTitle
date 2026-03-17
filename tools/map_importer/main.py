"""
Impressive Title Map Importer

Author: DylanCheetah
Description:
A tool that imports Impressive Title maps for use with Neo Impressive Title.
"""

from argparse import ArgumentParser
from pathlib import Path

import tomli_w

from ast import Map


# Parse command-line arguments
parser = ArgumentParser()
parser.add_argument("in_folder", type=Path, help="a folder containing one or more maps to import")
parser.add_argument("out_folder", type=Path, help="the folder to write the converted maps into")
args = parser.parse_args()

# Import each map in the given folder
for map_folder in args.in_folder.iterdir():
    # Build path to .world file
    world_file = map_folder / f"{map_folder.stem}.world"

    # Skip over files
    if map_folder.is_file():
        continue

    # Skip map folders which lack a .world file
    elif not world_file.exists():
        continue

    # Import world map
    print(f"Parsing '{world_file}'...")
    world_map = Map()
    world_map.parse(world_file)

    # Convert world map
    print(f"Converting '{world_file}'...")
    world_data = world_map.to_dict()
    map_name = map_folder.stem.replace(" ", "").replace("'", "")
    toml_file = args.out_folder / map_name / "World.toml"
    
    with toml_file.open("wb") as f:
        tomli_w.dump(world_data, f)
