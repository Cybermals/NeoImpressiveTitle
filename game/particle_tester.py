import inspect

from direct.particles.ParticleEffect import ParticleEffect
from direct.showbase.ShowBase import ShowBase

from panda3d.core import Vec4
from panda3d_kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.relativelayout import RelativeLayout

import particles


# Classes
# =======
class MainScreen(RelativeLayout):
    particle = StringProperty()

    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Populate particle spinner
        self.ids.particle.values = [
            particle for particle in dir(particles) if (
                inspect.isclass(getattr(particles, particle)) and 
                issubclass(getattr(particles, particle), ParticleEffect))
        ]

    def on_particle(self, instance, value):
        # Ignore "Select Particle"
        if value == "Select Particle":
            return
        
        # Load selected particle
        base.load_particle(value)


class ParticleTesterUI(App):
    def build(self):
        return MainScreen()


class ParticleTester(ShowBase):
    def __init__(self):
        # Call the base constructor
        ShowBase.__init__(self)

        # Set background color
        self.win.set_clear_color(Vec4(0, 0, 0, 1))

        # Initialize UI
        self.ui = ParticleTesterUI(self)
        self.ui.run()

        # Initialize camera
        self.disable_mouse()
        self.camera.set_y(-10)

        # Initialize particles
        self.enable_particles()
        self.particle = None

    def load_particle(self, name):
        # Unload previous particle effect
        if self.particle:
            self.particle.cleanup()

        # Load new particle effect
        self.particle = getattr(particles, name)()
        self.particle.start(parent=self.render, renderParent=self.render)


# Entry Point
if __name__ == "__main__":
    ParticleTester().run()
