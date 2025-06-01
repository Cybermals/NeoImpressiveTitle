from pathlib import Path

from direct.stdpy.file import *  # noqa: F403
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.screenmanager import Screen


# Classes
# =======
class CharacterEditorScreen(Screen):
    character_name_input = ObjectProperty()
    body_spinner = ObjectProperty()
    head_spinner = ObjectProperty()
    mane_spinner = ObjectProperty()
    tail_spinner = ObjectProperty()
    wing_spinner = ObjectProperty()
    tuft_spinner = ObjectProperty()
    body_marking_spinner = ObjectProperty()
    head_marking_spinner = ObjectProperty()
    tail_marking_spinner = ObjectProperty()
    pelt_color_picker = ObjectProperty()
    underfur_color_picker = ObjectProperty()
    nose_color_picker = ObjectProperty()
    above_eyes_color_picker = ObjectProperty()
    below_eyes_color_picker = ObjectProperty()
    ear_color_picker = ObjectProperty()
    tailtip_color_picker = ObjectProperty()
    eye_color_picker = ObjectProperty()
    size_slider = ObjectProperty()
    character_size = NumericProperty(1)
    save_btn = ObjectProperty()

    def on_body_spinner(self, instance, value):
        # Populate body spinner
        self.body_spinner.values = [
            Path(path).stem for path in listdir("meshes/player/bodies")  # noqa: F405,E501
        ]

    def on_head_spinner(self, instance, value):
        # Populate head spinner
        self.head_spinner.values = [
            Path(path).stem for path in listdir("meshes/player/heads")  # noqa: F405,E501
        ]

    def on_mane_spinner(self, instance, value):
        # Populate mane spinner
        self.mane_spinner.values = [
            Path(path).stem for path in listdir("meshes/player/manes")  # noqa: F405,E501
        ]

    def on_tail_spinner(self, instance, value):
        # Populate tail spinner
        self.tail_spinner.values = [
            Path(path).stem for path in listdir("meshes/player/tails")  # noqa: F405,E501
        ]

    def on_wing_spinner(self, instance, value):
        # Populate wing spinner
        self.wing_spinner.values = [
            Path(path).stem for path in listdir("meshes/player/wings")  # noqa: F405,E501
        ]

    def on_tuft_spinner(self, instance, value):
        # Populate tuft spinner
        self.tuft_spinner.values = [
            Path(path).stem for path in listdir("meshes/player/tufts")  # noqa: F405,E501
        ]

    def on_body_marking_spinner(self, instance, value):
        # Populate body marking spinner
        # TODO: populate this with actual markings
        self.body_marking_spinner.values = ["None"]

    def on_head_marking_spinner(self, instance, value):
        # Populate head marking spinner
        # TODO: populate this with actual markings
        self.head_marking_spinner.values = ["None"]

    def on_tail_marking_spinner(self, instance, value):
        # Populate tail marking spinner
        # TODO: populate this with actual markings
        self.tail_marking_spinner.values = ["None"]

    def update_size(self, value):
        try:
            self.size_slider.value = max(min(float(value), 255), 0)

        except ValueError:
            pass

    def validate_character_name(self):
        self.save_btn.disabled = len(self.character_name) == 0


Builder.load_file("ui/screens/character_editor_screen.kv")
