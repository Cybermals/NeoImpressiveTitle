from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView


# Classes
# =======
class FriendListEntry(BoxLayout):
    pass


class FriendList(RecycleView):
    def __init__(self, *args, **kwargs):
        # Call base constructor
        super().__init__(*args, **kwargs)

        # Load sample friends
        self.data = [{"online": i % 4, "username": f"Friend {i + 1}"} for i in range(100)]


Builder.load_file("ui/friend_list.kv")
