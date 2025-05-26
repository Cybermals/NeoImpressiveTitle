from kivy.lang import Builder
from kivy.properties import ListProperty, ObjectProperty, StringProperty
from kivy.uix.screenmanager import (
    NoTransition,
    ScreenManager,
    ScreenManagerException,
    SlideTransition
)

import ui.chat_log  # noqa: F401


# Classes
# =======
class ChatBox(ScreenManager):
    chat_log = ObjectProperty()
    dm_recipient = ObjectProperty()
    chat_mode = StringProperty()
    chat_input = ObjectProperty()
    general_chat = ListProperty()
    local_chat = ListProperty()
    party_chat = ListProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.general_chat = [{"username": "DylanCheetah", "content": f"General post {i + 1}. The quick brown fox jumped over the lazy brown dog. The cat sat on the mat with the rat and the bat and the hat."} for i in range(100)]  # noqa: E501
        self.local_chat = [{"username": "DylanCheetah", "content": f"Local post {i + 1}."} for i in range(100)]  # noqa: E501
        self.party_chat = [{"username": "DylanCheetah", "content": f"Party post {i + 1}."} for i in range(100)]  # noqa: E501

    def hide_chat(self):
        self.transition = SlideTransition(direction="left")
        self.current = "HiddenChat"

    def show_chat(self):
        self.transition = SlideTransition(direction="right")
        self.current = "VisibleChat"

    def on_chat_mode(self, source, value):
        try:
            self.chat_log.transition = NoTransition()
            self.chat_log.current = value

        except ScreenManagerException:
            pass  # ignore this


Builder.load_file("ui/chat_box.kv")
