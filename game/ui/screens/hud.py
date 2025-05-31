from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

import ui.chat_box  # noqa: F401
import ui.player_hp_panel  # noqa: F401


# Classes
# =======
class HUD(Screen):
    pass


Builder.load_file("ui/screens/hud.kv")
