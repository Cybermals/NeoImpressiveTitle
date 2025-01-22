from pathlib import Path

from direct.stdpy.file import *
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.screenmanager import Screen

import ui.theme


# Classes
# =======
class CharacterEditorScreen(Screen):
    character_name_input = ObjectProperty(None)
    body_spinner = ObjectProperty(None)
    head_spinner = ObjectProperty(None)
    mane_spinner = ObjectProperty(None)
    tail_spinner = ObjectProperty(None)
    wing_spinner = ObjectProperty(None)
    tuft_spinner = ObjectProperty(None)
    body_marking_spinner = ObjectProperty(None)
    head_marking_spinner = ObjectProperty(None)
    tail_marking_spinner = ObjectProperty(None)
    pelt_color_picker = ObjectProperty(None)
    underfur_color_picker = ObjectProperty(None)
    nose_color_picker = ObjectProperty(None)
    above_eyes_color_picker = ObjectProperty(None)
    below_eyes_color_picker = ObjectProperty(None)
    ear_color_picker = ObjectProperty(None)
    tailtip_color_picker = ObjectProperty(None)
    eye_color_picker = ObjectProperty(None)
    size_slider = ObjectProperty(None)
    character_size = NumericProperty(1)
    save_btn = ObjectProperty(None)

    def on_body_spinner(self, instance, value):
        # Populate body spinner
        self.body_spinner.values = [Path(path).stem for path in listdir("meshes/player/bodies")]

    def on_head_spinner(self, instance, value):
        # Populate head spinner
        self.head_spinner.values = [Path(path).stem for path in listdir("meshes/player/heads")]

    def on_mane_spinner(self, instance, value):
        # Populate mane spinner
        self.mane_spinner.values = [Path(path).stem for path in listdir("meshes/player/manes")]

    def on_tail_spinner(self, instance, value):
        # Populate tail spinner
        self.tail_spinner.values = [Path(path).stem for path in listdir("meshes/player/tails")]

    def on_wing_spinner(self, instance, value):
        # Populate wing spinner
        self.wing_spinner.values = [Path(path).stem for path in listdir("meshes/player/wings")]

    def on_tuft_spinner(self, instance, value):
        # Populate tuft spinner
        self.tuft_spinner.values = [Path(path).stem for path in listdir("meshes/player/tufts")]

    def on_body_marking_spinner(self, instance, value):
        # Populate body marking spinner
        self.body_marking_spinner.values = ["None"]  # TODO: populate this with actual markings

    def on_head_marking_spinner(self, instance, value):
        # Populate head marking spinner
        self.head_marking_spinner.values = ["None"]  # TODO: populate this with actual markings

    def on_tail_marking_spinner(self, instance, value):
        # Populate tail marking spinner
        self.tail_marking_spinner.values = ["None"]  # TODO: populate this with actual markings

    def update_size(self, value):
        try:
            self.size_slider.value = max(min(float(value), 255), 0)

        except ValueError:
            pass

    def validate_character_name(self):
        self.save_btn.disabled = len(self.character_name) == 0


Builder.load_file("ui/screens/character_editor_screen.kv")
