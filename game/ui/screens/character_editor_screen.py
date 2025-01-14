from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen

import ui.theme


# Classes
# =======
class CharacterEditorScreen(Screen):
    character_name = StringProperty("")
    body = ObjectProperty(None)
    head = ObjectProperty(None)
    mane = ObjectProperty(None)
    tail = ObjectProperty(None)
    wings = ObjectProperty(None)
    tuft = ObjectProperty(None)
    save_btn = ObjectProperty(None)

    def validate_character_name(self):
        self.save_btn.disabled = len(self.character_name) == 0


Builder.load_file("ui/screens/character_editor_screen.kv")
