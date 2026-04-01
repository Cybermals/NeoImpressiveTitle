import tomllib

from direct.directnotify.DirectNotify import DirectNotify
from direct.stdpy.file import *
from panda3d.core import (
    GeoMipTerrain,
    Material,
    SamplerState,
    Shader,
    TextureStage,
    Vec2,
    Vec4
)

# Configure logging
logger = DirectNotify().newCategory("MapManager")


# Classes
# =======
class MapManager(object):
    def __init__(self):
        self.maps = [
            map_name for map_name in listdir("maps") 
            if self.is_map_valid(map_name)]
        self.terrain = None

        # Create terrain material
        self.terrain_mat = Material()
        self.terrain_mat.set_metallic(0)
        self.terrain_mat.set_emission(Vec4(0, 0, 0, 1))
        self.terrain_mat.set_roughness(.8)
        self.terrain_mat.set_refractive_index(1)

        # Load terrain shader
        self.terrain_shader = Shader.load(
            Shader.SL_GLSL,
            join("shaders", "Terrain.vert.glsl"),
            join("shaders", "Terrain.frag.glsl")
        )

        # Load caution stripes texture
        self.stripes_tex = base.loader.load_texture(join("images", "terrain", "CautionStripes.png"))
        self.stripes_tex.minfilter = SamplerState.FT_linear_mipmap_linear
        self.stripes_tex.magfilter = SamplerState.FT_linear_mipmap_linear
        self.stripes_tex.wrap_u = SamplerState.WM_repeat
        self.stripes_tex.wrap_v = SamplerState.WM_repeat

        # Schedule update task
        base.task_mgr.add(self.update, "map_manager")

    def is_map_valid(self, map_name):
        valid = (
            exists(join("maps", map_name, "World.toml")) and
            exists(join("maps", map_name, "Terrain.toml")) and
            exists(join("maps", map_name, "Heightmap.png")) and
            exists(join("maps", map_name, "ColorMask.png"))
        )

        if not valid:
            logger.warning(f"Map '{map_name}' is invalid.")

        return valid

    def get_maps(self):
        return self.maps
    
    def load_map(self, name):
        # Is the map valid?
        if name not in self.maps:
            logger.error(f"Map '{name}' cannot be loaded.")
            return
        
        # Unload the current map
        self.unload_map()

        # Load terrain
        logger.info(f"Loading map '{name}'...")
        terrain = GeoMipTerrain("Terrain")
        terrain.set_heightfield(join("maps", name, "Heightmap.png"))
        terrain.set_block_size(64)
        terrain.set_focal_point(base.camera)

        # Load terrain config file
        with open(join("maps", name, "Terrain.toml"), "rb") as f:
            terrain_config = tomllib.load(f)

        # Set terrain material and shader
        terrain.get_root().set_material(self.terrain_mat)
        terrain.get_root().set_shader(self.terrain_shader)

        # Load terrain textures
        for i, layer in enumerate(terrain_config["layers"]):
            # Load texture
            texture = base.loader.load_texture(join("images", "terrain", layer["texture"]))
            texture.minfilter = SamplerState.FT_linear_mipmap_linear
            texture.magfilter = SamplerState.FT_linear_mipmap_linear
            texture.wrap_u = SamplerState.WM_repeat
            texture.wrap_v = SamplerState.WM_repeat

            # Set texture and texture scale
            terrain.get_root().set_texture(TextureStage(f"Layer{i}"), texture)
            terrain.get_root().set_shader_input(
                f"texScale{i}",
                Vec2(layer["scale"][0], layer["scale"][1])
            )

        # Fill empty texture slots
        for i in range(i + 1, 4):
            # Set blank texture
            terrain.get_root().set_texture(TextureStage(f"BlankLayer{i}"), self.stripes_tex)
            terrain.get_root().set_shader_input(
                f"texScale{i}",
                Vec2(1, 1)
            )

        # Load color mask
        color_mask = base.loader.load_texture(join("maps", name, "ColorMask.png"))
        color_mask.minfilter = SamplerState.FT_linear_mipmap_linear
        color_mask.magfilter = SamplerState.FT_linear_mipmap_linear
        terrain.get_root().set_texture(TextureStage("ColorMask"), color_mask)

        # Load world file
        with open(join("maps", name, "World.toml"), "rb") as f:
            world_config = tomllib.load(f)

        # Set terrain size
        terrain.get_root().set_scale(
            world_config["width"] / 513,
            world_config["height"] / 513,
            terrain_config["terrain"]["max_height"]
        )

        # Generate and display terrain
        terrain.generate()
        terrain.get_root().reparent_to(base.render)
        self.terrain = terrain

    def unload_map(self):
        # Destroy existing terrain
        self.terrain = None

    def update(self, task):
        # Update terrain
        if self.terrain is not None:
            self.terrain.update()

        return task.cont
