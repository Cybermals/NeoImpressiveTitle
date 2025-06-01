from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView

from ui.theme import GameButton


# Classes
# =======
class BlockListEntry(GameButton):
    def on_release(self):
        print(f"Clicked blocked user {self.text}")


class BlockList(RecycleView):
    def __init__(self, *args, **kwargs):
        # Call base constructor
        super().__init__(*args, **kwargs)

        # Load sample block list
        self.data = [{"text": f"Troublemaker {i + 1}"} for i in range(100)]


Builder.load_file("ui/block_list.kv")
