from argparse import ArgumentParser
from pathlib import Path

from ast import MaterialLibrary


# Parse command-line arguments
parser = ArgumentParser()
parser.add_argument("in_folder", type=Path, help="a folder of Ogre material scripts to import")
parser.add_argument("out_file", type=str, help="the material library file to output")
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
