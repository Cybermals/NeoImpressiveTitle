from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

import ui.chat_box  # noqa: F401
import ui.player_hp_panel  # noqa: F401
import ui.target_hp_panel  # noqa: F401


# Classes
# =======
class HUD(Screen):
    chat_box = ObjectProperty()
    player_hp_panel = ObjectProperty()
    target_hp_panel = ObjectProperty()


Builder.load_file("ui/screens/hud.kv")
