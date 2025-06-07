from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView


# Classes
# =======
class ItemList(RecycleView):
    pass


Builder.load_file("ui/item_list.kv")
