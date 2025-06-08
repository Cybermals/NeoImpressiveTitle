from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.recycleview import RecycleView

from ui.theme import GameButton


# Classes
# =======
class BlockListEntry(GameButton):
    command = ObjectProperty()


class BlockList(RecycleView):
    pass


Builder.load_file("ui/block_list.kv")
