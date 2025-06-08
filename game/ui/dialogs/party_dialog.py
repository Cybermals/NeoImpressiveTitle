from kivy.lang import Builder
from kivy.properties import ObjectProperty

from ui.theme import GameFloatingWindow

import ui.item_list  # noqa: F401


# Classes
# =======
class PartyDialog(GameFloatingWindow):
    party = ObjectProperty()
    leave_party_btn = ObjectProperty()

    def on_party(self, instance, value):
        # Load test data
        self.party.data = [{"text": f"Member {i + 1}"} for i in range(20)]


Builder.load_file("ui/dialogs/party_dialog.kv")
