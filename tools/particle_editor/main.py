"""Particle Editor

Author: DylanCheetah
Description:
A simple script to invoke the particle panel built into Panda3D.
"""

from direct.showbase.ShowBase import ShowBase
from direct.tkpanels.ParticlePanel import ParticlePanel
from panda3d.core import load_prc_file


# Classes
# =======
class ParticleEditor(ShowBase):
    def __init__(self):
        # Load config file
        load_prc_file("settings.prc")

        # Call the base constructor
        ShowBase.__init__(self)

        # Initialize particle panel
        self.particle_panel = ParticlePanel()
        self.disable_mouse()
        self.camera.set_y(-10)
        self.set_background_color(0, 0, 0)


# Entry Point
if __name__ == "__main__":
    ParticleEditor().run()
