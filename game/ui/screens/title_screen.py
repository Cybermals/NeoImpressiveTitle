from direct.stdpy.file import *
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

from ui.theme import GameLabel


# Classes
# =======
class Logo(Image):
    pass


class ChangelogEntry(GameLabel):
    pass


class TitleScreen(Screen):
    changelog = ObjectProperty(None)

    def on_changelog(self, instance, value):
        # Load the changelog
        with open("changelog.txt") as f:
            self.changelog.data = [{"text": line.strip()} for line in f]


Builder.load_file("ui/screens/title_screen.kv")
