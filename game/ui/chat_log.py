from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.recycleview import RecycleView

from ui.theme import GameLabel


# Classes
# =======
class Post(GameLabel):
    username = StringProperty()
    content = StringProperty()

    def on_ref_press(self, value):
        print(f"Clicked user {value}")


class ChatLog(RecycleView):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Create temporary post widget for calculating size
        self.tmp_post = Post()

    def update_text(self):
        tmp_post = self.tmp_post

        for i, item in enumerate(self.data):
            tmp_post.username = item["username"]
            tmp_post.content = item["content"]
            tmp_post.width = self.width
            tmp_post.texture_update()
            self.data[i]["ks"] = tmp_post.texture_size

        self.refresh_from_data()


Builder.load_file("ui/chat_log.kv")
