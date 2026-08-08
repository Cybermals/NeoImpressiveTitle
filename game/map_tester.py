# panda3d-kivy monkey patch
# =========================
import panda3d_kivy.core.window as kivy_window

# Store original method
_original_update_size = kivy_window.PandaWindow.update_size

def safe_update_size(self):
    try:
        _original_update_size(self)
    except AssertionError:
        # Ignore uninitialized matrix state during scene loading frames
        pass

# Apply override
kivy_window.PandaWindow.update_size = safe_update_size


# Imports
# =======
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
from panda3d.core import (
    AmbientLight,
    DirectionalLight,
    load_prc_file,
    Vec4
)
from panda3d_kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.relativelayout import RelativeLayout

from map_manager import MapManager


# Classes
# =======
class MapTesterScreen(RelativeLayout):
    map_name = StringProperty()

    def on_map_name(self, instance, value):
        # Return if no map selected
        if value == "Choose a Map":
            return
        
        # Load the selected map
        base.map_mgr.load_map(value)


class MapTesterUI(App):
    def build(self):
        self.main_screen = MapTesterScreen()
        return self.main_screen
    
    def set_available_maps(self, maps):
        self.main_screen.ids.map_name.values = maps


class MapTester(ShowBase):
    def __init__(self):
        # Load config file
        load_prc_file("settings.prc")

        # Call the base constructor
        ShowBase.__init__(self)

        # Initialize UI
        self.ui = MapTesterUI(self)
        self.ui.run()

        # Initialize lighting
        # TODO: Move this to sky manager
        self.ambient = self.render.attach_new_node(AmbientLight("Ambient"))
        self.ambient.node().set_color(Vec4(.8, .8, .8, 1))
        self.render.set_light(self.ambient)

        self.sun = self.render.attach_new_node(DirectionalLight("Sun"))
        self.sun.set_p(-45)
        self.render.set_light(self.sun)

        # Initialize map manager
        self.map_mgr = MapManager()

        # Schedule initialization task
        self.task_mgr.add(self.init_map_tester(), "init_map_tester")

        self.camera.place()

    async def init_map_tester(self):
        # Wait for the UI to be initialized
        await Task.pause(1)

        # Set list of available maps
        self.ui.set_available_maps(self.map_mgr.get_maps())


# Entrypoint
if __name__ == "__main__":
    MapTester().run()
