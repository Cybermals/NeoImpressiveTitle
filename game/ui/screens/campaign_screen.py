from pathlib import Path

from direct.stdpy.file import *
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from ui.theme import GameButton


# Classes
# =======
class CampaignButton(GameButton):
    pass


class CampaignScreen(Screen):
    campaign_list = ObjectProperty(None)

    def on_campaign_list(self, instance, value):
        # Load campaign list
        self.campaign_list.data = [{"text": Path(path).stem} for path in listdir("campaigns")]


Builder.load_file("ui/screens/campaign_screen.kv")
