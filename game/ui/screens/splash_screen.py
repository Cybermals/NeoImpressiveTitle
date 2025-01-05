from direct.directnotify.DirectNotify import DirectNotify
from kivy.clock import Clock
from kivy.core.image import Image
from kivy.graphics import RenderContext
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget


# Configure logging
log = DirectNotify().newCategory("UI")


# Constants
# =========
FRAG_SHADER = """
#ifdef GL_ES
    precision highp float;
#endif

/* Outputs from the vertex shader */
varying vec4 frag_color;
varying vec2 tex_coord0;

/* uniform texture samplers */
uniform sampler2D texture0;
uniform mat4 frag_modelview_mat;
uniform float time;

void main(void) {
    gl_FragColor = texture2D(texture0, tex_coord0 + vec2(time, -time) * .1);
}
"""


# Classes
# =======
class WavesOverlay(Widget):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Create render context
        self.canvas = RenderContext(self, use_parent_projection=True)
        self.canvas.shader.fs = FRAG_SHADER

        if not self.canvas.shader.success:
            log.error("Failed to compile fragment shader!")

        # Load wave texture
        texture = Image("images/ui/LogoWaves.png").texture
        texture.wrap = "repeat"

        # Schedule time uniform update
        Clock.schedule_interval(self.update, 1 / 60)

    def update(self, dt):
        # Update time uniform
        self.canvas["time"] = Clock.get_boottime()


class SplashScreen(Screen):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Reset this screen
        self.reset()

    def reset(self):
        # Start transition timer
        self.timer = Clock.schedule_once(self.finish, 10)
        
    def finish(self, dt):
        # Switch to the title screen
        base.game_state.request("TitleScreen")


Builder.load_file("ui/screens/splash_screen.kv")
