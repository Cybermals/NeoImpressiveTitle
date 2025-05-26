from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

import ui.chat_box


# Classes
# =======
class HUD(Screen):
    pass


Builder.load_file("ui/screens/hud.kv")
