from kivy.lang import Builder
from kivy.properties import StringProperty

from ui.theme import GameFloatingWindow


# Classes
# =======
class ActionsDialog(GameFloatingWindow):
    PRIMARY_ACTIONS = [
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
    SECONDARY_ACTIONS = [
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
    EMOTES = [
        "None"
    ]

    primary_action = StringProperty()
    secondary_action = StringProperty()
    emote = StringProperty()

    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # TODO: Load emotes from config file

    def on_primary_action(self, instance, value):
        print(f"Primary Action: {value}")

    def on_secondary_action(self, instance, value):
        print(f"Secondary Action: {value}")

    def on_emote(self, instance, value):
        print(f"Emotes: {value}")


Builder.load_file("ui/dialogs/actions_dialog.kv")
