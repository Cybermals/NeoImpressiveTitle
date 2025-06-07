from kivy.lang import Builder
from kivy.properties import ObjectProperty

from ui.theme import GameFloatingWindow


# Classes
# =======
class ActionsDialog(GameFloatingWindow):
    primary_action = ObjectProperty()
    secondary_action = ObjectProperty()
    emote = ObjectProperty()

    def on_primary_action(self, instance, value):
        # Set available primary actions
        self.primary_action.values = [
            "None",
            "Sit",
            "Lay",
            "Plop Down",
            "Side Lay",
            "Lay Down",
            "Roll Over",
            "Crouch",
            "Point",
            "Stretch",
            "Headswing",
            "Headbang",
            "Buttswing",
            "Wingwave",
            "Moonwalk",
            "Thriller",
            "Rofl",
            "Roar",
            "Curl",
            "Faint"
        ]

    def on_secondary_action(self, instance, value):
        # Set available secondary actions
        self.secondary_action.values = [
            "None",
            "Nod Head",
            "Shake Head",
            "Nod Head (Slow)",
            "Shake Head (Slow)",
            "Head Tilt",
            "Lick",
            "Nuzzle",
            "Sniff",
            "Tail Flick",
            "Laugh",
            "Chuckle"
        ]

    def on_emote(self, instance, value):
        # Set available emotes
        self.emote.values = [
            "None"
        ]
        # TODO: Load emotes from config file.


Builder.load_file("ui/dialogs/actions_dialog.kv")
