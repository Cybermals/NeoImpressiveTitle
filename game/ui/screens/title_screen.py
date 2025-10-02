from direct.stdpy.file import open
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen

import ui.changelog  # noqa: F401


# Classes
# =======
class TitleScreen(Screen):
    changelog = ListProperty()

    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Load the changelog
        with open("changelog.txt") as f:
            self.changelog = [
                {"text": " " if line == "\n" else line.rstrip()} for line in f
            ]


Builder.load_file("ui/screens/title_screen.kv")
