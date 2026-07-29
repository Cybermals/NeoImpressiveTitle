import tomllib

from direct.directnotify.DirectNotify import DirectNotify
from direct.stdpy.file import *
from panda3d.bullet import (
    BulletDebugNode,
    BulletGhostNode,
    BulletHeightfieldShape,
    BulletSphereShape,
    BulletRigidBodyNode,
    BulletWorld,
    Z_up
)
from panda3d.core import (
    GeoMipTerrain,
    Material,
    SamplerState,
    Shader,
    TextureStage,
    Vec2,
    Vec3,
    Vec4
)

from sky import SkyDome
from water import WaterPlane

# Configure logging
logger = DirectNotify().newCategory("MapManager")
logger.setInfo(True)


# Classes
# =======
class MapManager(object):
    def __init__(self):
        self.maps = [
            map_name for map_name in listdir("maps") 
            if self.is_map_valid(map_name)]
        self.terrain = None
        self.terrain_body = None
        self.terrain_size = None
        self.portals = []
        self.gates = []
        self.water_planes = []

        # Load default shader
        self.default_shader = Shader.load(
            Shader.SL_GLSL,
            "shaders/Simple.vert.glsl",
            "shaders/Simple.frag.glsl"
        )
        base.render.set_shader(self.default_shader)

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

        # Create physics world
        self.physics_world = BulletWorld()
        self.physics_world.set_gravity(0, 0, -9.81)

        # Configure physics debugging
        bullet_dbg = base.render.attach_new_node(BulletDebugNode("BulletDebug"))
        bullet_dbg.node().show_wireframe(True)
        bullet_dbg.node().show_constraints(True)
        bullet_dbg.node().show_bounding_boxes(False)
        bullet_dbg.node().show_normals(False)
        # bullet_dbg.show()
        self.physics_world.set_debug_node(bullet_dbg.node())

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
            world_config["width"] / 512,
            world_config["height"] / 512,
            terrain_config["max_height"]
        )

        # Create terrain rigid body
        terrain_shape = BulletHeightfieldShape(
            terrain.heightfield(),
            1,
            Z_up
        )
        terrain_body = base.render.attach_new_node(BulletRigidBodyNode("TerrainBody"))
        terrain_body.node().add_shape(terrain_shape)
        terrain_body.set_scale(
            world_config["width"] / 512,
            world_config["height"] / 512,
            terrain_config["max_height"]
        )
        terrain_body.set_pos(
            world_config["width"] / 2,
            world_config["height"] / 2,
            terrain_config["max_height"] / 2
        )
        self.physics_world.attach(terrain_body.node())
        self.terrain_body = terrain_body

        # Generate and display terrain
        terrain.generate()
        terrain.get_root().reparent_to(base.render)
        self.terrain = terrain
        self.terrain_size = Vec3(
            world_config["width"],
            world_config["height"],
            terrain_config["max_height"]
        )

        # Set world bounds if present
        # TODO

        # Create sky
        cloud_tex = base.loader.load_texture("images/sky/Clouds.png")
        cloud_tex.minfilter = SamplerState.FT_linear_mipmap_linear
        cloud_tex.magfilter = SamplerState.FT_linear_mipmap_linear
        cloud_tex.wrap_u = SamplerState.WM_repeat
        cloud_tex.wrap_v = SamplerState.WM_repeat

        celestials_tex = base.loader.load_texture("images/sky/Celestials.png")
        celestials_tex.minfilter = SamplerState.FT_linear_mipmap_linear
        celestials_tex.magfilter = SamplerState.FT_linear_mipmap_linear
        celestials_tex.wrap_u = SamplerState.WM_repeat
        celestials_tex.wrap_v = SamplerState.WM_repeat

        self.sky = SkyDome(
            Vec4(0.0, .64, 1.0, 1.0),
            Vec4(0.0, .49, .76, 1.0),
            cloud_tex,
            celestials_tex
        )
        self.sky.set_cloud_scale(Vec2(.5, .5))

        # Does the map have portals?
        if "portals" in world_config:
            # Create portals
            for portal in world_config["portals"]:
                self.add_portal(
                    portal["pos"], 
                    portal["range"], 
                    portal["destination"]
                )

        # Does the map have gates?
        if "gates" in world_config:
            # Create gates
            for gate in world_config["gates"]:
                self.add_gate(
                    gate["pos"],
                    gate["destination"],
                    gate["dest_pos"],
                    gate["material"]
                )

        # Does the map have water planes?
        if "water_planes" in world_config:
            # Create water planes
            for water_plane in world_config["water_planes"]:
                self.add_water_plane(
                    water_plane["pos"],
                    [water_plane["scale_x"], water_plane["scale_z"], 1],
                    water_plane["sound"] if "sound" in water_plane else "",
                    water_plane["is_solid"] if "is_solid" in water_plane else False
                )

    def unload_map(self):
        # Destroy existing terrain
        if self.terrain is not None:
            self.terrain.get_root().remove_node()
            self.terrain = None

        # Destroy existing terrain body
        if self.terrain_body is not None:
            self.physics_world.remove(self.terrain_body.node())
            self.terrain_body.remove_node()
            self.terrain_body = None

        # Destroy existing portals
        for portal in self.portals:
            self.physics_world.remove(portal.node())
            portal.remove_node()

        self.portals = []

        # Destroy existing gates
        for gate in self.gates:
            self.physics_world.remove(gate.node())
            gate.remove_node()

        self.gates = []

        # Destroy existing water planes
        # Note: The water plane destructor handles removing them from the scene graph.
        self.water_planes = []

    def add_portal(self, pos, range, destination):
        # Create portal
        logger.info(f"Adding portal (pos = {pos}, range = {range}, destination = {destination})...")
        
        portal_shape = BulletSphereShape(1)
        portal_body = base.render.attach_new_node(BulletGhostNode("Portal"))
        portal_body.node().add_shape(portal_shape)
        portal_body.set_pos(*pos)
        portal_body.set_scale(range, range, range)
        portal_body.set_python_tag("destination", destination)
        self.physics_world.attach(portal_body.node())

        portal = base.loader.load_model("meshes/scenery/Portal.gltf")
        texture = base.loader.load_texture(join("maps", destination, "Portal.jpg"))

        if texture is None:
            logger.warning(f"Failed to load portal texture for map '{destination}'.")

        default_tex = portal.find_texture("portalDefault")
        portal.replace_texture(default_tex, texture)
        
        portal.reparent_to(portal_body)
        self.portals.append(portal_body)

    def add_gate(self, pos, destination, dest_pos, material=""):
        # Create gate
        logger.info(f"Adding gate (pos = {pos}, destination = {destination}, dest_pos = {dest_pos}, material = {material})...")

        gate_shape = BulletSphereShape(1)
        gate_body = base.render.attach_new_node(BulletGhostNode("Gate"))
        gate_body.node().add_shape(gate_shape)
        gate_body.set_pos(*pos)
        gate_body.set_scale(5, 5, 5)
        gate_body.set_python_tag("destination", destination)
        gate_body.set_python_tag("dest_pos", dest_pos)
        self.physics_world.attach(gate_body.node())

        gate = base.loader.load_model("meshes/scenery/Portal.gltf")
        # TODO: Set material here
        gate.reparent_to(gate_body)
        self.gates.append(gate)

    def add_water_plane(self, pos, scale, sound, is_solid):
        # Create water plane
        logger.info(f"Adding water plane (pos = {pos}, scale = {scale})")

        water_plane = WaterPlane(pos, scale, sound, is_solid)
        # TODO: Set material here
        self.water_planes.append(water_plane)

    def update(self, task):
        # Update terrain
        if self.terrain is not None:
            self.terrain.update()

        # Update physics
        self.physics_world.do_physics(base.clock.get_dt())

        # TODO: Handle collisions between the player and portals.

        # TODO: Handle collisions between the player and gates.

        # TODO: Determine if each player and NPC is underwater.

        return task.cont
