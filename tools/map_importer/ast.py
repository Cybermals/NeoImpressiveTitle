# Constants
# =========
GLOBAL_SCALE = .1


# Classes
# =======
class MapSettings(object):
    def __init__(self):
        self.terrain = ""
        self.width = 0
        self.height = 0
        self.spawn_point = [0, 0, 0]
        self.bounds = None

    def parse(self, s):
        # Split section into params
        params = s.strip().split("\n")[1:]
        params = [param.strip() for param in params]

        # Parse params
        self.terrain = params[0]
        self.width = int(params[1]) * GLOBAL_SCALE
        self.height = int(params[2]) * GLOBAL_SCALE
        self.spawn_point = [float(n) * GLOBAL_SCALE for n in params[3].split(" ")]

        if len(params) > 4:
            self.bounds = [int(n) * GLOBAL_SCALE for n in params[4].split(" ")]

    def to_dict(self):
        # Convert map settings to a dictionary
        data = {
            "terrain": self.terrain,
            "width": self.width,
            "height": self.height,
            "spawn_point": self.spawn_point
        }
        
        if self.bounds is not None:
            data["bounds"] = self.bounds

        return data
    

class Portal(object):
    def __init__(self):
        self.pos = [0, 0, 0]
        self.range = 0
        self.destination = ""

    def parse(self, s):
        # Split section into params
        params = s.strip().split("\n")[1:]
        params = [param.strip() for param in params]

        # Parse params
        self.pos = [float(n) * GLOBAL_SCALE for n in params[0].split(" ")]
        self.range = float(params[1]) * GLOBAL_SCALE
        self.destination = params[2]

    def to_dict(self):
        # Convert portal data to a dictionary
        return {
            "pos": self.pos,
            "range": self.range,
            "destination": self.destination
        }
    

class Gate(object):
    def __init__(self):
        self.material = ""
        self.pos = [0, 0, 0]
        self.destination = ""
        self.dest_pos = [0, 0, 0]

    def parse(self, s):
        # Split section into params
        params = s.strip().split("\n")[1:]
        params = [param.strip() for param in params]

        # Parse params
        self.material = params[0]
        self.pos = [float(n) * GLOBAL_SCALE for n in params[1].split(" ")]
        self.destination = params[2]
        self.dest_pos = [float(n) * GLOBAL_SCALE for n in params[3].split(" ")]

    def to_dict(self):
        # Convert gate data to a dictionary
        return {
            "material": self.material,
            "pos": self.pos,
            "destination": self.destination,
            "dest_pos": self.dest_pos
        }
    

class WaterPlane(object):
    def __init__(self):
        self.pos = [0, 0, 0]
        self.scale_x = 0
        self.scale_z = 0
        self.material = "Terrain/CalmWater"
        self.sound = ""
        self.is_solid = False

    def parse(self, s):
        # Split section into params
        params = s.strip().split("\n")[1:]
        params = [param.strip() for param in params]

        # Parse params
        self.pos = [float(n) * GLOBAL_SCALE for n in params[0].split(" ")]
        self.scale_x = float(params[1]) * 500 * GLOBAL_SCALE
        self.scale_z = float(params[2]) * 500 * GLOBAL_SCALE
        
        if len(params) > 3:
            self.material = params[3]

        if len(params) > 4:
            self.sound = params[4]

        if len(params) > 5:
            self.is_solid = params[5] == "true"

    def to_dict(self):
        # Convert water plane data to a dictionary
        data = {
            "pos": self.pos,
            "scale_x": self.scale_x,
            "scale_z": self.scale_z
        }

        if self.material != "Terrain/CalmWater":
            data["material"] = self.material

        if self.sound != "":
            data["sound"] = self.sound

        if self.is_solid:
            data["is_solid"] = self.is_solid

        return data
    

class MapObject(object):
    def __init__(self):
        self.mesh = ""
        self.pos = [0, 0, 0]
        self.rot = [0, 0, 0]
        self.scale = [0, 0, 0]
        self.sound = ""
        self.material = ""

    def parse(self, s):
        # Split section into params
        params = s.strip().split("\n")[1:]
        params = [param.strip() for param in params]

        # Parse params
        self.mesh = params[0].replace(".mesh", "")
        self.pos = [float(n) * GLOBAL_SCALE for n in params[1].split(" ")]
        self.rot = [float(n) for n in params[2].split(" ")]
        self.scale = [float(n) * GLOBAL_SCALE for n in params[3].split(" ")]

        if len(params) > 4:
            self.sound = params[4]

        if len(params) > 5:
            self.material = params[5]

    def to_dict(self):
        # Convert object data to a dictionary
        data = {
            "mesh": self.mesh,
            "pos": self.pos,
            "rot": self.rot,
            "scale": self.scale
        }

        if self.sound != "":
            data["sound"] = self.sound

        if self.material != "":
            data["material"] = self.material

        return data
    

class Particle(object):
    def __init__(self):
        self.name = ""
        self.pos = [0, 0, 0]
        self.sound = ""

    def parse(self, s):
        # Split section into params
        params = s.strip().split("\n")[1:]
        params = [param.strip() for param in params]

        # Parse params
        self.name = params[0]
        self.pos = [float(n) * GLOBAL_SCALE for n in params[1].split(" ")]

        if len(params) > 2:
            self.sound = params[2]

    def to_dict(self):
        # Convert particle data to a dictionary
        data = {
            "name": self.name,
            "pos": self.pos
        }

        if self.sound != "":
            data["sound"] = self.sound

        return data
    

class WeatherCycle(object):
    def __init__(self):
        self.name = ""

    def parse(self, s):
        # Split section into params
        params = s.strip().split("\n")[1:]
        params = [param.strip() for param in params]

        # Parse params
        self.name = params[0] if params[0] != "None" else ""

    def to_dict(self):
        # Convert weather cycle data to dictionary
        return {
            "name": self.name
        }
    

class Interior(object):
    def __init__(self):
        self.height = 0
        self.material = ""
        self.sky_color = [0, 0, 0, 0]

    def parse(self, s):
        # Split section into params
        params = s.strip().split("\n")[1:]
        params = [param.strip() for param in params]

        # Parse params
        self.height = float(params[0]) * GLOBAL_SCALE
        self.material = params[1]
        
        if len(params) > 2:
            self.sky_color = [float(n) for n in params[2].split(" ")]

    def to_dict(self):
        # Convert interior data to a dictionary
        return {
            "height": self.height,
            "material": self.material,
            "sky_color": self.sky_color
        }
    

class Light(object):
    def __init__(self):
        self.pos = [0, 0, 0]
        self.color = [0, 0, 0, 0]

    def parse(self, s):
        # Split section into params
        params = s.strip().split("\n")[1:]
        params = [param.strip() for param in params]

        # Parse params
        self.pos = [float(n) * GLOBAL_SCALE for n in params[0].split(" ")]
        self.color = [float(n) for n in params[1].split(" ")]

    def to_dict(self):
        # Convert light data to a dictionary
        return {
            "pos": self.pos,
            "color": self.color
        }
    

class Billboard(object):
    def __init__(self):
        self.pos = [0, 0, 0]
        self.scale = [0, 0, 0]
        self.material = ""

    def parse(self, s):
        # Split section into params
        params = s.strip().split("\n")[1:]
        params = [param.strip() for param in params]

        # Parse params
        self.pos = [float(n) * GLOBAL_SCALE for n in params[0].split(" ")]
        self.scale = [float(n) * GLOBAL_SCALE for n in params[1].split(" ")]
        self.material = params[2]

    def to_dict(self):
        # Convert billboard data to a dictionary
        return {
            "pos": self.pos,
            "scale": self.scale,
            "material": self.material
        }
    

class SphereWall(object):
    def __init__(self):
        self.pos = [0, 0, 0]
        self.range = 0
        self.is_inside = False

    def parse(self, s):
        # Split section into params
        params = s.strip().split("\n")[1:]
        params = [param.strip() for param in params]

        # Parse params
        self.pos = [float(n) * GLOBAL_SCALE for n in params[0].split(" ")]
        self.range = float(params[1]) * GLOBAL_SCALE
        self.is_inside = params[2] == "true"

    def to_dict(self):
        # Convert sphere wall data to a dictionary
        return {
            "pos": self.pos,
            "range": self.range,
            "is_inside": self.is_inside
        }
    

class BoxWall(object):
    def __init__(self):
        self.pos = [0, 0, 0]
        self.range = [0, 0]
        self.is_inside = False

    def parse(self, s):
        # Split section into params
        params = s.strip().split("\n")[1:]
        params = [param.strip() for param in params]

        # Parase params
        self.pos = [float(n) * GLOBAL_SCALE for n in params[0].split(" ")]
        self.range = [float(n) * GLOBAL_SCALE for n in params[1].split(" ")]
        self.is_inside = params[2] == "true"

    def to_dict(self):
        # Convert box wall data to a dictionary
        return {
            "pos": self.pos,
            "range": self.range,
            "is_inside": self.is_inside
        }
    

class MapEffect(object):
    def __init__(self):
        self.name = ""

    def parse(self, s):
        # Split section into params
        params = s.strip().split("\n")[1:]
        params = [param.strip() for param in params]

        # Parse params
        self.name = params[0]

    def to_dict(self):
        # Convert map effect data to a dictionary
        return {
            "name": self.name
        }
    

class Grass(object):
    def __init__(self):
        self.material = ""
        self.map = ""
        self.color_map = ""

    def parse(self, s):
        # Split section into params
        params = s.strip().split("\n")[1:]
        params = [param.strip() for param in params]

        # Parse params
        self.material = params[0]
        self.map = params[1]
        self.color_map = params[2]

    def to_dict(self):
        # Convert grass data to a dictionary
        return {
            "material": self.material,
            "map": self.map,
            "color_map": self.color_map
        }
    

class RandomTrees(object):
    def __init__(self):
        self.trees = []
        self.count = 0

    def parse(self, s):
        # Split section into params
        params = s.strip().split("\n")[1:]
        params = [param.strip() for param in params]

        # Parse params
        self.trees = [tree.replace(".mesh", "") for tree in params[:-1]]
        self.count = int(params[-1])

    def to_dict(self):
        # Convert random tree data to a dictionary
        return {
            "trees": self.trees,
            "count": self.count
        }
    

class RandomBushes(object):
    def __init__(self):
        self.bushes = []

    def parse(self, s):
        # Split section into params
        params = s.strip().split("\n")[1:]
        params = [param.strip() for param in params]

        # Parse params
        self.bushes = [bush.replace(".mesh", "") for bush in params]

    def to_dict(self):
        # Convert random bush data to a dictionary
        return {
            "bushes": self.bushes
        }
    

class FoliageGroup(object):
    def __init__(self):
        self.mesh = ""
        self.material = ""
        self.instances = []

    def parse(self, s):
        # Split section into lines
        lines = s.split("\n")
        lines = [line.strip() for line in lines]
        lines[0] = lines[0][:-1]

        # Parse mesh and material
        params = lines[0].split(";")
        self.mesh = params[0].replace(".mesh", "")

        if len(params) > 1:
            self.material = params[1]

        # Parse instances
        for line in lines[1:]:
            # Skip blank lines and custom EOF character
            if line == "" or line == "#":
                continue

            # Split line into params
            params = line.split(";")
            params = [param.strip() for param in params]

            # Skip corrupt lines
            if len(params) != 3:
                continue

            # Parse params
            pos = [float(n) * GLOBAL_SCALE for n in params[0].split(" ")]
            scale = [float(n) * GLOBAL_SCALE for n in params[1].split(" ")]
            rot = [float(n) * GLOBAL_SCALE for n in params[2].split(" ")]
            self.instances.append({
                "pos": pos,
                "rot": rot,
                "scale": scale
            })

    def to_dict(self):
        # Convert tree group to a dictionary
        data = {
            "mesh": self.mesh,
            "instances": self.instances
        }

        if self.material != "":
            data["material"] = self.material

        return data
    

class FoliageGroups(object):
    def __init__(self):
        self.groups = []

    def parse(self, s, map_folder):
        # Split section into params
        params = s.strip().split("\n")[1:]

        # Parse tree file
        tree_file = map_folder / params[0]
        tree_data = tree_file.read_text()
        sections = tree_data.split("[")[1:]

        for section in sections:
            group = FoliageGroup()
            group.parse(section)
            self.groups.append(group)

    def to_dict(self):
        # Convert tree groups to a dictionary
        return {
            "groups": [group.to_dict() for group in self.groups]
        }


class Map(object):
    def __init__(self):
        self.settings = None
        self.portals = []
        self.gates = []
        self.water_planes = []
        self.map_objects = []
        self.particles = []
        self.weather_cycle = None
        self.interior = None
        self.lights = []
        self.billboards = []
        self.sphere_walls = []
        self.box_walls = []
        self.map_effect = None
        self.grass = None
        self.random_trees = None
        self.random_bushes = None
        self.foliage = []

    def parse(self, world_file):
        # Split map data into sections
        sections = world_file.read_text().split("[")

        # Parse sections
        for section in sections:
            # Skip empty sections
            if section == "":
                continue

            # Parse map settings section
            elif section.startswith("Initialize"):
                self.settings = MapSettings()
                self.settings.parse(section)

            # Parse portal section
            elif section.startswith("Portal"):
                portal = Portal()
                portal.parse(section)
                self.portals.append(portal)

            # Parse gate section
            elif section.startswith("Gate"):
                gate = Gate()
                gate.parse(section)
                self.gates.append(gate)

            # Parse water plane section
            elif section.startswith("WaterPlane"):
                water_plane = WaterPlane()
                water_plane.parse(section)
                self.water_planes.append(water_plane)

            # Parse object section
            elif section.startswith("Object"):
                map_object = MapObject()
                map_object.parse(section)
                self.map_objects.append(map_object)

            # Parse particle section
            elif section.startswith("Particle"):
                particle = Particle()
                particle.parse(section)
                self.particles.append(particle)

            # Parse weather cycle section
            elif section.startswith("WeatherCycle"):
                self.weather_cycle = WeatherCycle()
                self.weather_cycle.parse(section)

            # Parse interior section
            elif section.startswith("Interior"):
                self.interior = Interior()
                self.interior.parse(section)

            # Parse light section
            elif section.startswith("Light"):
                light = Light()
                light.parse(section)
                self.lights.append(light)

            # Parse billboard section
            elif section.startswith("Billboard"):
                billboard = Billboard()
                billboard.parse(section)
                self.billboards.append(billboard)

            # Parse sphere wall section
            elif section.startswith("SphereWall"):
                sphere_wall = SphereWall()
                sphere_wall.parse(section)
                self.sphere_walls.append(sphere_wall)

            # Parse box wall section
            elif section.startswith("BoxWall"):
                box_wall = BoxWall()
                box_wall.parse(section)
                self.box_walls.append(box_wall)

            # Parse map effect section
            elif section.startswith("MapEffect"):
                self.map_effect = MapEffect()
                self.map_effect.parse(section)

            # Parse grass section
            elif section.startswith("Grass"):
                self.grass = Grass()
                self.grass.parse(section)

            # Parse random trees section
            elif section.startswith("RandomTrees"):
                self.random_trees = RandomTrees()
                self.random_trees.parse(section)

            # Parse random bushes section
            elif section.startswith("RandomBushes"):
                self.random_bushes = RandomBushes()
                self.random_bushes.parse(section)

            # Parse foliage section
            elif (section.startswith("Trees") or
                  section.startswith("Bushes") or
                  section.startswith("FloatingBushes") or
                  section.startswith("NewTrees") or
                  section.startswith("NewBushes") or
                  section.startswith("NewFloatingBushes")):
                foliage_group = FoliageGroups()
                foliage_group.parse(section, world_file.parent)
                self.foliage.append(foliage_group)

    def to_dict(self):
        # Convert map data to a dictionary
        data = {}
        data.update(self.settings.to_dict())

        if len(self.portals):
            data["portals"] = [portal.to_dict() for portal in self.portals]

        if len(self.gates):
            data["gates"] = [gate.to_dict() for gate in self.gates]

        if len(self.water_planes):
            data["water_planes"] = [
                water_plane.to_dict() for water_plane in self.water_planes]
            
        if len(self.map_objects):
            # Group map objects by mesh for more efficient rendering
            map_objects = {}

            for map_object in self.map_objects:
                # Preprocess map object data
                map_object_data = map_object.to_dict()
                key = (
                    map_object_data["mesh"], 
                    map_object_data["material"] if "material" in map_object_data else ""
                )
                del map_object_data["mesh"]

                if "material" in map_object_data:
                    del map_object_data["material"]

                # Add object if necessary
                if key not in map_objects:
                    map_objects[key] = {
                        "mesh": key[0],
                        "instances": []
                    }

                    if key[1] != "":
                        map_objects[key]["material"] = key[1]

                # Add object instance
                map_objects[key]["instances"].append(map_object_data)

            # Add map objects
            data["objects"] = list(map_objects.values())

        if len(self.particles):
            data["particles"] = [
                particle.to_dict() for particle in self.particles]
            
        if self.weather_cycle is not None and self.weather_cycle.name != "":
            data["weather_cycle"] = self.weather_cycle.to_dict()["name"]

        if self.interior is not None:
            data["interior"] = self.interior.to_dict()

        if len(self.lights):
            data["lights"] = [light.to_dict() for light in self.lights]

        if len(self.billboards):
            data["billboards"] = [
                billboard.to_dict() for billboard in self.billboards]
            
        if len(self.sphere_walls):
            data["sphere_walls"] = [
                sphere_wall.to_dict() for sphere_wall in self.sphere_walls
            ]

        if len(self.box_walls):
            data["box_walls"] = [
                box_wall.to_dict() for box_wall in self.box_walls
            ]

        if self.map_effect and self.map_effect.name != "":
            data["map_effect"] = self.map_effect.to_dict()["name"]

        if self.grass:
            data["grass"] = self.grass.to_dict()

        if self.random_trees:
            data["random_trees"] = self.random_trees.to_dict()

        if self.random_bushes:
            data["random_bushes"] = self.random_bushes.to_dict()

        if len(self.foliage):
            if "objects" not in data:
                data["objects"] = []

            for foliage_group in self.foliage:
                data["objects"].extend(foliage_group.to_dict()["groups"])

        return data
