from kivy.lang import Builder
from kivy.properties import ObjectProperty

from ui.theme import GameFloatingWindow

import ui.item_list


# Classes
# =======
class StashDialog(GameFloatingWindow):
    items = ObjectProperty()

    def on_items(self, instance, value):
        # Display test data
        self.items.data = [{"text": f"Item {i + 1}"} for i in range(100)]


Builder.load_file("ui/dialogs/stash_dialog.kv")
