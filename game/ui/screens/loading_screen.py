from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

import ui.theme  # noqa: F401


# Classes
# =======
class LoadingScreen(Screen):
    message = StringProperty("")
    ellipsis = StringProperty("")

    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Start progress indicator
        Clock.schedule_interval(self.update, 1 / 4)

    def update(self, dt):
        self.ellipsis += "."

        if len(self.ellipsis) == 4:
            self.ellipsis = ""


Builder.load_file("ui/screens/loading_screen.kv")
