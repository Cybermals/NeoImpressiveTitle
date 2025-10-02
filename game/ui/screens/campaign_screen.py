from pathlib import Path

from direct.stdpy.file import listdir
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen

from ui.theme import GameButton


# Classes
# =======
class CampaignButton(GameButton):
    pass


class CampaignScreen(Screen):
    campaign_list = ListProperty()

    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Load campaign list
        self.campaign_list = [
            {"text": Path(path).stem} for path in listdir("campaigns")
        ]


Builder.load_file("ui/screens/campaign_screen.kv")
