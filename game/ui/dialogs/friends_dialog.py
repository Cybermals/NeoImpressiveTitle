from kivy.lang import Builder

from ui.theme import GameFloatingWindow

import ui.block_list
import ui.friend_list


# Classes
# =======
class FriendsDialog(GameFloatingWindow):
    pass


Builder.load_file("ui/dialogs/friends_dialog.kv")
