from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.recycleview import RecycleView

from ui.theme import GameButton


# Classes
# =======
class ItemListEntry(GameButton):
    command = ObjectProperty()


class ItemList(RecycleView):
    pass


Builder.load_file("ui/item_list.kv")
