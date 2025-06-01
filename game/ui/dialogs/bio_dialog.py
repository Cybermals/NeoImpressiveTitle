from kivy.lang import Builder
from kivy.properties import BooleanProperty

from ui.theme import GameFloatingWindow


# Classes
# =======
class BioDialog(GameFloatingWindow):
    is_modified = BooleanProperty(False)

    def set_modified(self, value):
        self.is_modified = value

    def on_parent(self, instance, value):
        if value is None and self.is_modified:
            print("Save Player Bio")
            self.is_modified = False


Builder.load_file("ui/dialogs/bio_dialog.kv")
