from pathlib import Path

from direct.stdpy.file import *  # noqa: F403
from kivy.lang import Builder
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    StringProperty
)
from kivy.uix.screenmanager import Screen


# Classes
# =======
class CharacterEditorScreen(Screen):
    bodies = ListProperty()
    heads = ListProperty()
    manes = ListProperty()
    tails = ListProperty()
    wings = ListProperty()
    tufts = ListProperty()
    body_markings = ListProperty()
    head_markings = ListProperty()
    tail_markings = ListProperty()

    character_name = StringProperty()
    body = StringProperty()
    head = StringProperty()
    mane = StringProperty()
    tail = StringProperty()
    wing = StringProperty()
    tuft = StringProperty()
    body_marking = StringProperty()
    head_marking = StringProperty()
    tail_marking = StringProperty()
    pelt_color = ListProperty()
    underfur_color = ListProperty()
    nose_color = ListProperty()
    above_eyes_color = ListProperty()
    below_eyes_color = ListProperty()
    ear_color = ListProperty()
    tailtip_color = ListProperty()
    eye_color = ListProperty()
    character_size = NumericProperty(1)
    save_disabled = BooleanProperty()

    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Populate available body parts
        self.bodies = [
            Path(path).stem for path in listdir("meshes/player/bodies")  # noqa: F405,E501
        ]
        self.heads = [
            Path(path).stem for path in listdir("meshes/player/heads")  # noqa: F405,E501
        ]
        self.manes = [
            Path(path).stem for path in listdir("meshes/player/manes")  # noqa: F405,E501
        ]
        self.tails = [
            Path(path).stem for path in listdir("meshes/player/tails")  # noqa: F405,E501
        ]
        self.wings = [
            Path(path).stem for path in listdir("meshes/player/wings")  # noqa: F405,E501
        ]
        self.tufts = [
            Path(path).stem for path in listdir("meshes/player/tufts")  # noqa: F405,E501
        ]

        # Populate available markings
        self.body_markings = ["None"]
        self.head_markings = ["None"]
        self.tail_markings = ["None"]

    def on_body(self, instance, value):
        print(f"Body: {value}")

    def on_head(self, instance, value):
        print(f"Head: {value}")

    def on_mane(self, instance, value):
        print(f"Mane: {value}")

    def on_tail(self, instance, value):
        print(f"Tail: {value}")

    def on_wing(self, instance, value):
        print(f"Wing: {value}")

    def on_tuft(self, instance, value):
        print(f"Tuft: {value}")

    def on_body_marking(self, instance, value):
        print(f"Body Marking: {value}")

    def on_head_marking(self, instance, value):
        print(f"Head Marking: {value}")

    def on_tail_marking(self, instance, value):
        print(f"Tail Marking: {value}")

    def on_pelt_color(self, instance, value):
        print(f"Pelt Color: {value}")

    def on_underfur_color(self, instance, value):
        print(f"Underfur Color: {value}")

    def on_nose_color(self, instance, value):
        print(f"Nose Color: {value}")

    def on_above_eyes_color(self, instance, value):
        print(f"Above Eye Color: {value}")

    def on_below_eyes_color(self, instance, value):
        print(f"Below Eye Color: {value}")

    def on_ear_color(self, instance, value):
        print(f"Ear Color: {value}")

    def on_tailtip_color(self, instance, value):
        print(f"Tailtip Color: {value}")

    def on_eye_color(self, instance, value):
        print(f"Eye Color: {value}")

    def on_character_size(self, instance, value):
        print(f"Character Size: {value}")

    def update_size(self, value):
        try:
            self.ids.character_size.value = max(min(float(value), 255), 0)

        except ValueError:
            pass

    def validate_character_name(self):
        self.save_disabled = len(self.character_name) == 0


Builder.load_file("ui/screens/character_editor_screen.kv")
