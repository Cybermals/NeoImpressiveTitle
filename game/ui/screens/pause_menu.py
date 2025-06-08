from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

import ui.theme  # noqa: F401


# Classes
# =======
class PauseMenu(Screen):
    pass


Builder.load_file("ui/screens/pause_menu.kv")
