# Classes
# =======
class MaterialSyntaxError(Exception):
    pass


class TextureUnit(object):
    def __init__(self):
        self.texture = None
        self.tex_address_mode = None
        self.filtering = None
        self.scroll_anim = None
        self.rotate_anim = None
        self.wave_xform = None
        self.colour_op = None
        self.scale = None

    def parse(self, f, startline):
        # Iterate over the lines of the material script
        lineno = startline
        block_started = False

        for line in f:
            # Increment line number
            lineno += 1

            # Strip whitespace
            line = line.strip()

            # Skip blank lines and comments
            if line == "" or line.startswith("//"):
                continue

            # Start block
            elif line == "{":
                # Can't start the block twice
                if block_started:
                   raise MaterialSyntaxError(f"Line {lineno}: Unexpected token.")
                
                block_started = True

            # End block
            elif line == "}":
                return lineno
            
            # Property?
            elif (line.startswith("texture") or
                  line.startswith("tex_address_mode") or
                  line.startswith("filtering") or
                  line.startswith("scroll_anim") or
                  line.startswith("rotate_anim") or
                  line.startswith("wave_xform") or
                  line.startswith("colour_op") or
                  line.startswith("scale")):
                # Store property value
                key, value = line.split(" ", maxsplit=1)
                setattr(self, key, value)

            # Unknown?
            else:
                raise MaterialSyntaxError(f"Line {lineno} cannot be recognized.")


class Pass(object):
    def __init__(self):
        self.texture_units = []
        self.cull_hardware = None
        self.cull_software = None
        self.alpha_rejection = None
        self.ambient = None
        self.diffuse = None
        self.specular = None
        self.emissive = None
        self.depth_write = None
        self.scene_blend = None
        self.lighting = None
        self.alpha_to_coverage = None
        self.colour_write = None
        self.depth_check = None
        self.depth_func = None
        self.illumination_stage = None
        self.light_clip_planes = None
        self.light_scissor = None
        self.normalise_normals = None
        self.polygon_mode = None
        self.shading = None
        self.transparent_sorting = None
        self.fog_override = None

    def __iter__(self):
        return iter(self.texture_units)

    def parse(self, f, startline):
        # Iterate over the lines of the material script
        lineno = startline
        block_started = False

        for line in f:
            # Increment line number
            lineno += 1

            # Strip whitespace
            line = line.strip()

            # Skip blank lines and comments
            if line == "" or line.startswith("//"):
                continue

            # Start block
            elif line == "{":
                # Can't start the block twice
                if block_started:
                   raise MaterialSyntaxError(f"Line {lineno}: Unexpected token.")
                
                block_started = True

            # End block
            elif line == "}":
                return lineno
            
            # Property?
            elif (line.startswith("cull_hardware") or
                  line.startswith("cull_software") or
                  line.startswith("alpha_rejection") or
                  line.startswith("ambient") or
                  line.startswith("diffuse") or
                  line.startswith("specular") or
                  line.startswith("emissive") or
                  line.startswith("depth_write") or
                  line.startswith("scene_blend") or
                  line.startswith("lighting") or
                  line.startswith("alpha_to_coverage") or
                  line.startswith("colour_write") or
                  line.startswith("depth_check") or
                  line.startswith("depth_func") or
                  line.startswith("light_clip_planes") or
                  line.startswith("light_scissor") or
                  line.startswith("normalise_normals") or
                  line.startswith("polygon_mode") or
                  line.startswith("shading") or
                  line.startswith("transparent_sorting") or
                  line.startswith("fog_override")):
                # Store property value
                key, value = line.split(" ", maxsplit=1)
                setattr(self, key, value)

            # Property?
            elif line.startswith("illumination_stage"):
                # Store property value
                key = line
                setattr(self, key, True)
            
            # Texture unit?
            elif line.startswith("texture_unit"):
                # Parse texture unit
                texture_unit = TextureUnit()
                lineno = texture_unit.parse(f, lineno)
                self.texture_units.append(texture_unit)

            # Unknown?
            else:
                raise MaterialSyntaxError(f"Line {lineno} cannot be recognized.")


class Technique(object):
    def __init__(self):
        self.passes = []

    def __iter__(self):
        return iter(self.passes)

    def parse(self, f, startline):
        # Iterate over the lines of the material script
        lineno = startline
        block_started = False

        for line in f:
            # Increment line number
            lineno += 1

            # Strip whitespace
            line = line.strip()

            # Skip blank lines and comments
            if line == "" or line.startswith("//"):
                continue

            # Start block
            elif line == "{":
                # Can't start the block twice
                if block_started:
                   raise MaterialSyntaxError(f"Line {lineno}: Unexpected token.")
                
                block_started = True

            # End block
            elif line == "}":
                return lineno

            # Pass?
            elif line.startswith("pass"):
                # Parse pass
                _pass = Pass()
                lineno = _pass.parse(f, lineno)
                self.passes.append(_pass)

            # Unknown?
            else:
                raise MaterialSyntaxError(f"Line {lineno} cannot be recognized.")


class Material(object):
    def __init__(self):
        self.techniques = []
        self.transparency_casts_shadows = None
        self.receive_shadows = None

    def __iter__(self):
        return iter(self.techniques)

    def parse(self, f, startline):
        # Iterate over the lines of the material script
        lineno = startline
        block_started = False

        for line in f:
            # Increment line number
            lineno += 1

            # Strip whitespace
            line = line.strip()

            # Skip blank lines and comments
            if line == "" or line.startswith("//"):
                continue

            # Start block
            elif line == "{":
                # Can't start the block twice
                if block_started:
                   raise MaterialSyntaxError(f"Line {lineno}: Unexpected token.")
                
                block_started = True

            # End block?
            elif line == "}":
                return lineno
            
            # Property?
            elif (line.startswith("transparency_casts_shadows") or
                  line.startswith("receive_shadows")):
                # Store property value
                key, value = line.split(" ", maxsplit=1)
                setattr(self, key, value)

            # Technique?
            elif line.startswith("technique"):
                # Parse technique
                technique = Technique()
                lineno = technique.parse(f, lineno)
                self.techniques.append(technique)

            # Unknown?
            else:
                raise MaterialSyntaxError(f"Line {lineno} cannot be recognized.")


class MaterialLibrary(object):
    def __init__(self):
        self.materials = {}

    def __iter__(self):
        return iter(self.materials.items())

    def parse(self, f):
        # Iterate over the lines of the material script
        lineno = 0

        for line in f:
            # Increment line number
            lineno += 1

            # Strip whitespace
            line = line.strip()

            # Skip blank lines and comments
            if line == "" or line.startswith("//"):
                continue

            # Material?
            elif line.startswith("material"):
                # Parse material
                mat = Material()
                lineno = mat.parse(f, lineno)
                self.materials[line.split(" ")[1]] = mat

            # Unknown line
            else:
                raise MaterialSyntaxError(f"Line {lineno} cannot be recognized.")
