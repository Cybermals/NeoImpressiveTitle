from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView

from ui.theme import GameLabel


# Classes
# =======
class ChangeLogEntry(GameLabel):
    pass


class ChangeLog(RecycleView):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Create temporary post widget for calculating size
        self.tmp_entry = ChangeLogEntry()

    def update_text(self):
        tmp_entry = self.tmp_entry

        for i, item in enumerate(self.data):
            tmp_entry.text = item["text"]
            tmp_entry.width = self.width
            tmp_entry.texture_update()
            self.data[i]["ks"] = tmp_entry.texture_size

        self.refresh_from_data()


Builder.load_file("ui/changelog.kv")
