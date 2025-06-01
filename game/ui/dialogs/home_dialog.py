from kivy.lang import Builder

from ui.floating_window import FloatingWindow


# Classes
# =======
class HomeDialog(FloatingWindow):
    pass


Builder.load_file("ui/dialogs/home_dialog.kv")
