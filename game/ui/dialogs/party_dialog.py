from kivy.lang import Builder
from kivy.properties import BooleanProperty, ListProperty

from ui.theme import GameFloatingWindow

import ui.item_list  # noqa: F401


# Classes
# =======
class PartyDialog(GameFloatingWindow):
    party = ListProperty()
    leave_disabled = BooleanProperty()

    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Load test data
        self.party = [{"text": f"Member {i + 1}"} for i in range(20)]


Builder.load_file("ui/dialogs/party_dialog.kv")
