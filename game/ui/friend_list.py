from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView


# Classes
# =======
class FriendListEntry(BoxLayout):
    online = BooleanProperty()
    username = StringProperty()
    command = ObjectProperty()


class FriendList(RecycleView):
    pass


Builder.load_file("ui/friend_list.kv")
