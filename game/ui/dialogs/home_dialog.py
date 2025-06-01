from kivy.lang import Builder

from ui.theme import GameFloatingWindow


# Classes
# =======
class HomeDialog(GameFloatingWindow):
    pass


Builder.load_file("ui/dialogs/home_dialog.kv")
