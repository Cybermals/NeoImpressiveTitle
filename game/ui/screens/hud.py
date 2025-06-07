from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

import ui.chat_box  # noqa: F401
import ui.minimap  # noqa: F401
import ui.player_hp_panel  # noqa: F401
import ui.target_hp_panel  # noqa: F401

from ui.dialogs.actions_dialog import ActionsDialog
from ui.dialogs.bio_dialog import BioDialog
from ui.dialogs.friends_dialog import FriendsDialog
from ui.dialogs.home_dialog import HomeDialog
from ui.dialogs.inventory_dialog import InventoryDialog
from ui.dialogs.party_dialog import PartyDialog
from ui.dialogs.stash_dialog import StashDialog


# Classes
# =======
class HUD(Screen):
    chat_box = ObjectProperty()
    player_hp_panel = ObjectProperty()
    target_hp_panel = ObjectProperty()

    def __init__(self, *args, **kwargs):
        # Call base constructor
        super().__init__(*args, **kwargs)

        # Create dialogs
        self.home_dlg = HomeDialog()
        self.bio_dlg = BioDialog()
        self.friends_dlg = FriendsDialog()
        self.inventory_dlg = InventoryDialog()
        self.stash_dlg = StashDialog()
        self.actions_dlg = ActionsDialog()
        self.party_dlg = PartyDialog()

    def toggle_home_dialog(self):
        if self.home_dlg.parent is None:
            self.add_widget(self.home_dlg)

        else:
            self.remove_widget(self.home_dlg)

    def toggle_bio_dialog(self):
        if self.bio_dlg.parent is None:
            self.add_widget(self.bio_dlg)

        else:
            self.remove_widget(self.bio_dlg)

    def toggle_friend_dialog(self):
        if self.friends_dlg.parent is None:
            self.add_widget(self.friends_dlg)

        else:
            self.remove_widget(self.friends_dlg)

    def toggle_inventory_dialog(self):
        if self.inventory_dlg.parent is None:
            self.add_widget(self.inventory_dlg)

        else:
            self.remove_widget(self.inventory_dlg)

    def toggle_stash_dialog(self):
        if self.stash_dlg.parent is None:
            self.add_widget(self.stash_dlg)

        else:
            self.remove_widget(self.stash_dlg)

    def toggle_actions_dialog(self):
        if self.actions_dlg.parent is None:
            self.add_widget(self.actions_dlg)

        else:
            self.remove_widget(self.actions_dlg)

    def toggle_party_dialog(self):
        if self.party_dlg.parent is None:
            self.add_widget(self.party_dlg)

        else:
            self.remove_widget(self.party_dlg)


Builder.load_file("ui/screens/hud.kv")
