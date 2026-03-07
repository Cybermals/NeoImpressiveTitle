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


class Map(object):
    def __init__(self):
        self.settings = None
        self.portals = []
        self.gates = []
        self.water_planes = []

    def parse(self, s):
        # Split map data into sections
        sections = s.split("[")

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

        return data
