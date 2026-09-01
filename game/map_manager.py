import random
import tomllib
from typing import List, Union

from direct.directnotify.DirectNotify import DirectNotify
from direct.stdpy.file import *
from direct.task.Task import Task
from panda3d.bullet import (
    BulletBoxShape,
    BulletDebugNode,
    BulletGhostNode,
    BulletHeightfieldShape,
    BulletRigidBodyNode,
    BulletSphereShape,
    BulletTriangleMesh,
    BulletTriangleMeshShape,
    BulletWorld,
    Z_up
)
from panda3d.core import (
    GeoMipTerrain,
    Material,
    NodePath,
    PNMImage,
    PointLight,
    SamplerState,
    Shader,
    Texture,
    TextureStage,
    TransparencyAttrib,
    Vec2,
    Vec3,
    Vec4
)

import config
import particles
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
        self.object_groups = {}
        self.particles = []
        self.ceiling = None
        self.lights = []
        self.billboards = []
        self.sphere_walls = []
        self.box_walls = []
        self.grass_groups = {}
        self.collision_boxes = []
        self.collision_spheres = []

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
        bullet_dbg.show()
        self.physics_world.set_debug_node(bullet_dbg.node())

        # Initialize particles
        base.enable_particles()

        # Schedule update task
        base.task_mgr.add(self.update, "map_manager")

    def is_map_valid(self, map_name: str) -> bool:
        valid = (
            exists(join("maps", map_name, "World.toml")) and
            exists(join("maps", map_name, "Terrain.toml")) and
            exists(join("maps", map_name, "Heightmap.png")) and
            exists(join("maps", map_name, "ColorMask.png"))
        )

        if not valid:
            logger.warning(f"Map '{map_name}' is invalid.")

        return valid

    def get_maps(self) -> List[str]:
        return self.maps
    
    def load_map(self, name: str) -> None:
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
            # Note: Each terrain texture must be sampled as sRGB
            texture = base.loader.load_texture(join("images", "terrain", layer["texture"]))
            texture.minfilter = SamplerState.FT_linear_mipmap_linear
            texture.magfilter = SamplerState.FT_linear_mipmap_linear
            texture.wrap_u = SamplerState.WM_repeat
            texture.wrap_v = SamplerState.WM_repeat

            if texture.get_num_components() == 4:
                texture.set_format(Texture.F_srgb_alpha)

            else:
                texture.set_format(Texture.F_srgb)

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
        # Note: Color masks do not get sampled as sRGB
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
                    (water_plane["is_solid"] 
                     if "is_solid" in water_plane else False)
                )

        # Does the map have objects?
        if "objects" in world_config:
            # Create objects
            for map_object in world_config["objects"]:
                for instance in map_object["instances"]:
                    self.add_object(
                        instance["pos"],
                        instance["rot"],
                        instance["scale"],
                        map_object["mesh"],
                        (map_object["material"]
                         if "material" in map_object else ""),
                        map_object["sound"] if "sound" in map_object else ""
                    )

        # Does the map have particles?
        if "particles" in world_config:
            # Create particles
            for particle_sys in world_config["particles"]:
                self.add_particles(
                    particle_sys["name"],
                    particle_sys["pos"],
                    particle_sys["sound"] if "sound" in particle_sys else "",
                    particle_sys["material"] if "material" in particle_sys else ""
                )

        # Does the map have weather?
        if "weather_cycle" in world_config:
            pass  # TODO: Need to load the weather later.

        # Is the map an interior map?
        if "interior" in world_config:
            interior = world_config["interior"]
            self.set_interior(
                interior["height"],
                interior["material"] if "material" in interior else "",
                interior["sky_color"] if "sky_color" in interior else ""
            )

        # Does the map have any lights?
        if "lights" in world_config:
            for light in world_config["lights"]:
                self.add_light(light["pos"], light["color"])

        # Does the map have any billboards?
        if "billboards" in world_config:
            for billboard in world_config["billboards"]:
                self.add_billboard(
                    billboard["pos"], 
                    billboard["scale"], 
                    billboard["material"]
                )

        # Does the map have any sphere walls?
        if "sphere_walls" in world_config:
            for sphere_wall in world_config["sphere_walls"]:
                self.add_sphere_wall(
                    sphere_wall["pos"], 
                    sphere_wall["range"], 
                    sphere_wall["is_inside"]
                )

        # Does the map have any box walls?
        if "box_walls" in world_config:
            for box_wall in world_config["box_walls"]:
                self.add_box_wall(
                    box_wall["pos"],
                    box_wall["range"],
                    box_wall["is_inside"]
                )

        # Does the map have a map effect?
        if "map_effect" in world_config:
            pass  # TODO: Need to load the map effect later.

        # Does the map have grass?
        if "grass" in world_config:
            grass = world_config["grass"]
            self.add_grass(
                grass["material"],
                join("maps", name, "GrassDensityMap.png"),
                grass["color_map"]
            )

        # Does the map have random trees?
        if "random_trees" in world_config:
            # Randomly place the given number of trees randomly chosen from the
            # list of possible tree meshes
            random_trees = world_config["random_trees"]

            for i in range(random_trees["count"]):
                # Randomly choose a tree mesh and a position for it
                tree = random.choice(random_trees["trees"])
                pos = [
                    random.random() * self.terrain_size.x,
                    random.random() * self.terrain_size.y
                ]
                self.add_object(pos, [0], [.1, .1, .1], tree, "", "")

        # Does the map have random bushes?
        if "random_bushes" in world_config:
            # Randomly place bushes randomly chosen from the list of possible
            # bush meshes. The number of random bushes is equal to the width
            # of the world because Kov did it that way.
            random_bushes = world_config["random_bushes"]

            for i in range(int(self.terrain_size.x / 10)):
                # Randomly choose a bush mesh and a position for it
                bush = random.choice(random_bushes["bushes"])
                pos = [
                    random.random() * self.terrain_size.x,
                    random.random() * self.terrain_size.y
                ]
                self.add_object(pos, [0], [.1, .1, .1], bush, "", "")

        # Does the map have collision boxes?
        if "collision_boxes" in world_config:
            for collision_box in world_config["collision_boxes"]:
                self.add_collision_box(
                    collision_box["pos"],
                    collision_box["range"]
                )

        # Does the map have collision spheres?
        if "collision_spheres" in world_config:
            for collision_sphere in world_config["collision_spheres"]:
                self.add_collision_sphere(
                    collision_sphere["pos"],
                    collision_sphere["range"]
                )

        # Should time be frozen?
        if "freeze_time" in world_config:
            pass

        # Flatten object groups
        for object_group in self.object_groups.values():
            object_group.flatten_strong()

        # Flatten grass groups
        for grass_group in self.grass_groups.values():
            grass_group.flatten_strong()

    def unload_map(self) -> None:
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

        # Destroy existing map objects
        for object_group in self.object_groups.values():
            object_group.remove_node()

        self.object_groups = {}

        # Destroy existing particles
        for particle_sys in self.particles:
            particle_sys.remove_node()

        self.particles = []

        # Destroy existing ceiling
        if self.ceiling is not None:
            self.ceiling.remove_node()

        self.ceiling = None

        # Destroy existing lights
        for light in self.lights:
            base.render.clear_light(light)
            light.remove_node()

        self.lights = []

        # Destroy existing billboards
        for billboard in self.billboards:
            billboard.remove_node()

        self.billboards = []

        # Destroy existing sphere walls
        for sphere_wall in self.sphere_walls:
            self.physics_world.remove(sphere_wall.node())
            sphere_wall.remove_node()

        self.sphere_walls = []

        # Destroy existing box walls
        for box_wall in self.box_walls:
            self.physics_world.remove(box_wall.node())
            box_wall.remove_node()

        self.box_walls = []

        # Destroy grass groups
        for grass_group in self.grass_groups.values():
            grass_group.remove_node()

        self.grass_groups = {}

        # Destroy collision boxes
        for collision_box in self.collision_boxes:
            self.physics_world.remove(collision_box.node())
            collision_box.remove()

        self.collision_boxes = []

        # Destroy collison spheres
        for collision_sphere in self.collision_spheres:
            self.physics_world.remove(collision_sphere.node())
            collision_sphere.remove()

        self.collision_spheres = []

    def add_portal(
            self, 
            pos: Union[list, tuple], 
            range: float, 
            destination: str) -> None:
        # Create portal
        logger.info(f"Adding portal (pos = {pos}, range = {range}, destination = '{destination}')...")
        
        portal_shape = BulletSphereShape(1)
        portal_body = base.render.attach_new_node(BulletGhostNode("Portal"))
        portal_body.node().add_shape(portal_shape)
        portal_body.set_pos(*pos)
        portal_body.set_scale(range, range, range)
        portal_body.set_python_tag("destination", destination)
        self.physics_world.attach(portal_body.node())

        portal = base.loader.load_model("meshes/scenery/Portal.gltf")
        texture = base.loader.load_texture(join("maps", destination, "Portal.jpg"))

        if texture is not None:
            # Standalone diffuse textures must be sampled as sRGB
            if texture.get_num_components() == 4:
                texture.set_format(Texture.F_srgb_alpha)

            else:
                texture.set_format(Texture.F_srgb)

        else:
            logger.warning(f"Failed to load portal texture for map '{destination}'.")

        default_tex = portal.find_texture("portalDefault")
        portal.replace_texture(default_tex, texture)
        
        portal.reparent_to(portal_body)
        self.portals.append(portal_body)

    def add_gate(
            self, 
            pos: Union[list, tuple], 
            destination: str, 
            dest_pos: Union[list, tuple], 
            material: str = "") -> None:
        # Create gate
        logger.info(f"Adding gate (pos = {pos}, destination = '{destination}', dest_pos = {dest_pos}, material = '{material}')...")

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

    def add_water_plane(
            self, 
            pos: Union[list, tuple], 
            scale: Union[list, tuple], 
            sound: str, 
            is_solid: bool) -> None:
        # Create water plane
        logger.info(f"Adding water plane (pos = {pos}, scale = {scale})")
        return  # TODO: Fix water collision performance bug

        water_plane = WaterPlane(pos, scale, sound, is_solid)
        # TODO: Set material here
        self.water_planes.append(water_plane)

    def add_object(
            self, 
            pos: Union[list, tuple], 
            rot: Union[list, tuple],
            scale: Union[list, tuple], 
            mesh: str, 
            material: str,
            sound: str):
        logger.info(f"Adding map object (pos = {pos}, rot = {rot}, scale = {scale}, mesh = '{mesh}', material = '{material}', sound = '{sound}')...")

        # Does the object position lack a Z coordinate?
        if len(pos) < 3:
            # Calculate the object position based on terrain height
            ray_col = self.physics_world.ray_test_closest(
                Vec3(pos[0], pos[1], self.terrain_size.z),
                Vec3(pos[0], pos[1], -self.terrain_size.z),
                0xffffffff
            )
            pos = ray_col.get_hit_pos()

        else:
            pos = Vec3(*pos)

        # Does the object rotation have just a heading?
        if len(rot) < 3:
            rot = Vec3(rot[0], 0, 0)

        else:
            rot = Vec3(*rot)
        
        # Calculate which group the object is in and its position within the group
        group_pos = pos // 64
        object_pos = Vec3(pos.x % 64, pos.y % 64, pos.z % 64)

        # Create the object group if it doesn't exist
        if group_pos not in self.object_groups:
            object_group = NodePath(f"ObjectGroup")
            object_group.set_pos(group_pos * 64)
            object_group.reparent_to(base.render)
            self.object_groups[group_pos] = object_group

        # Get the object group
        object_group = self.object_groups[group_pos]

        # Add the map object to the object group
        try:
            map_object = base.loader.load_model(join("meshes", "scenery", mesh))
            map_object.set_pos(object_pos)
            map_object.set_hpr(*rot)
            map_object.set_scale(*scale)
            # TODO: Set material and sound effect here.
            map_object.reparent_to(object_group)

            # Enable transparency if any of the textures have an alpha channel
            if (Texture.F_srgb_alpha in 
                    [tex.get_format() for tex in map_object.find_all_textures()]):
                map_object.set_attrib(
                    TransparencyAttrib.make(TransparencyAttrib.M_alpha))

        except IOError:
            logger.warning(f"Failed to load mesh '{mesh}'.")

    def add_particles(
            self, 
            name: str, 
            pos: Union[list, tuple],
            sound: str,
            material: str) -> None:
        logger.info(f"Adding particles (name = '{name}', pos = {pos}, sound = '{sound}', material = '{material}')...")

        # Create particles
        particle_root = NodePath("Particles")
        particle_root.set_pos(*pos)
        particle_root.set_shader_auto()
        particle_root.set_attrib(TransparencyAttrib.make(TransparencyAttrib.M_alpha))
        particle_root.reparent_to(base.render)
        self.particles.append(particle_root)

        ParticleClass = getattr(particles, name)
        particle_sys = ParticleClass()
        particle_sys.start(parent=particle_root, renderParent=particle_root)

        # TODO: Add sound effect. Not sure if material is applicable.

    def set_weather(self, name: str) -> None:
        pass

    def set_interior(
            self,
            height: float,
            material: str,
            sky_color: Union[list, tuple]) -> None:
        logger.info(f"Set interior (height = {height}, material = '{material}', sky_color = {sky_color})...")

        # Create ceiling
        ceiling = base.loader.load_model("meshes/scenery/Ceiling.gltf")
        x, y, z = self.terrain_size
        ceiling.set_scale(
            x / 2,
            y / 2,
            z
        )
        ceiling.set_y(y)
        ceiling.set_z(height)
        ceiling.reparent_to(base.render)
        self.ceiling = ceiling

    def add_light(
            self,
            pos: Union[list, tuple],
            color: Union[list, tuple]) -> None:
        logger.info(f"Adding light (pos = {pos}, color = {color})...")

        # Add a light source
        light = base.render.attach_new_node(PointLight("Light"))
        light.node().set_color(Vec4(*color, 1))
        light.node().set_attenuation(Vec3(1, .1, .5))
        light.set_pos(*pos)
        base.render.set_light(light)
        self.lights.append(light)

    def add_billboard(
            self,
            pos: Union[list, tuple],
            scale: Union[list, tuple],
            material: str) -> None:
        logger.info(f"Adding billboard (pos = {pos}, scale = {scale}, material = '{material}')...")

        # Add a billboard
        billboard = base.loader.load_model("meshes/scenery/Billboard.gltf")
        billboard.set_pos(*pos)
        billboard.set_scale(scale[0], 1, scale[1])
        billboard.set_billboard_point_world(0)
        # TODO: Set material
        billboard.reparent_to(base.render)
        self.billboards.append(billboard)

    def add_sphere_wall(
            self,
            pos: Union[list, tuple],
            range: float,
            is_inside: bool) -> None:
        logger.info(f"Adding sphere wall (pos = {pos}, range = {range}, is_inside = {is_inside})")

        # Create sphere wall shape
        if not is_inside:
            sphere_shape = BulletSphereShape(1)

        else:
            inv_col_sphere = base.loader.load_model("meshes/scenery/InvColSphere.gltf")
            inv_sphere_mesh = BulletTriangleMesh()
            inv_sphere_mesh.add_geom(inv_col_sphere.find("**/+GeomNode").node().get_geom(0))
            sphere_shape = BulletTriangleMeshShape(inv_sphere_mesh, False)

        # Add a sphere wall
        sphere_wall = base.render.attach_new_node(BulletRigidBodyNode("SphereWall"))
        sphere_wall.node().add_shape(sphere_shape)
        sphere_wall.set_pos(*pos)
        sphere_wall.set_scale(range, range, self.terrain_size.z)
        self.physics_world.attach(sphere_wall.node())
        self.sphere_walls.append(sphere_wall)

    def add_box_wall(
            self,
            pos: Union[list, tuple],
            range: Union[list, tuple],
            is_inside: bool) -> None:
        logger.info(f"Adding box wall (pos = {pos}, range = {range}, is_inside = {is_inside})...")

        # Create box shape
        if not is_inside:
            box_shape = BulletBoxShape(Vec3(1, 1, 1))

        else:
            inv_col_box = base.loader.load_model("meshes/scenery/InvColBox.gltf")
            inv_box_mesh = BulletTriangleMesh()
            inv_box_mesh.add_geom(inv_col_box.find("**/+GeomNode").node().get_geom(0))
            box_shape = BulletTriangleMeshShape(inv_box_mesh, False)

        # Add box wall
        box_wall = base.render.attach_new_node(BulletRigidBodyNode("BoxWall"))
        box_wall.node().add_shape(box_shape)
        box_wall.set_pos(*pos)
        box_wall.set_scale(range[0] / 2, range[1] / 2, self.terrain_size.z)
        self.physics_world.attach(box_wall.node())
        self.box_walls.append(box_wall)

    def add_grass(self, material: str, grass_map: str, color_map: str) -> None:
        logger.info(f"Adding grass (material = '{material}', grass_map = '{grass_map}', color_map = '{color_map}')...")

        # Load grass map
        grass_map_img = PNMImage()

        if not grass_map_img.read(grass_map):
            logger.warning(f"Failed to load grass map '{grass_map}'.")
            return

        grass_map_size = grass_map_img.get_size()
        scale = Vec2(
            self.terrain_size.x / grass_map_size.x,
            self.terrain_size.y / grass_map_size.y
        )

        # Parse grass map
        for y in range(0, grass_map_size.y, 2):
            for x in range(0, grass_map_size.x, 2):
                # Is the density greater than the grass density threshold?
                density = grass_map_img.get_gray(x, y)

                if density > config.GRASS_DENSITY_THRESHOLD:
                    # Calculate grass patch position
                    pos = Vec3(
                        x * scale.x, 
                        self.terrain_size.y - y * scale.y, 
                        0
                    )

                    ray_col = self.physics_world.ray_test_closest(
                        Vec3(pos[0], pos[1], self.terrain_size.z),
                        Vec3(pos[0], pos[1], -self.terrain_size.z),
                        0xffffffff
                    )
                    pos = ray_col.get_hit_pos()

                    # Calculate grass group position and object position within
                    # the group
                    group_pos = pos // 64
                    object_pos = Vec3(pos.x % 64, pos.y % 64, pos.z % 64)

                    # Create the grass group if it doesn't exist
                    if group_pos not in self.grass_groups:
                        grass_group = NodePath("GrassGroup")
                        grass_group.set_pos(group_pos * 64)
                        grass_group.set_attrib(
                            TransparencyAttrib.make(TransparencyAttrib.M_alpha)
                        )
                        grass_group.reparent_to(base.render)
                        self.grass_groups[group_pos] = grass_group

                    # Get grass group
                    grass_group = self.grass_groups[group_pos]

                    # Add the grass patch to the grass group
                    grass_patch = base.loader.load_model("meshes/scenery/Grass.gltf")
                    grass_patch.set_pos(object_pos)
                    grass_patch.reparent_to(grass_group)

    def add_collision_box(
            self, 
            pos: Union[list, tuple], 
            range: Union[list, tuple]) -> None:
        logger.info(f"Adding collision box (pos = {pos}, range = {range})...")

        # Add a collision box
        col_box = base.render.attach_new_node(BulletRigidBodyNode("CollisionBox"))
        col_shape = BulletBoxShape(Vec3(*range) / 2)
        col_box.node().add_shape(col_shape)
        col_box.set_pos(Vec3(*pos) + Vec3(0, 0, range[2] / 2))
        self.physics_world.attach(col_box.node())
        self.collision_boxes.append(col_box)

    def add_collision_sphere(
            self, 
            pos: Union[list, tuple], 
            range: float) -> None:
        logger.info(f"Add collision spheres (pos = {pos}, range = {range})...")

        # Add a collision sphere
        col_sphere = base.render.attach_new_node(BulletRigidBodyNode("CollisionSphere"))
        col_shape = BulletSphereShape(range)
        col_sphere.node().add_shape(col_shape)
        col_sphere.set_pos(*pos)
        self.physics_world.attach(col_sphere.node())
        self.collision_spheres.append(col_sphere)

    def update(self, task: Task) -> None:
        # Update terrain
        if self.terrain is not None:
            self.terrain.update()

        # Update physics
        self.physics_world.do_physics(base.clock.get_dt())

        # TODO: Handle collisions between the player and portals.

        # TODO: Handle collisions between the player and gates.

        # TODO: Determine if each player and NPC is underwater.

        return task.cont
