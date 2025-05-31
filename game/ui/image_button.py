from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image


# Classes
# =======
class ImageButton(ButtonBehavior, Image):
    background_normal = StringProperty()
    background_down = StringProperty()
    background_disabled_normal = StringProperty()
    background_disabled_down = StringProperty()
    current_background = StringProperty()

    def on_disabled(self, instance, value):
        if value:
            self.current_background = self.background_disabled_normal

        else:
            self.current_background = self.background_normal

    def on_state(self, instance, value):
        if not self.disabled:
            if value == "normal":
                self.current_background = self.background_normal

            elif value == "down":
                self.current_background = self.background_down


Builder.load_file("ui/image_button.kv")
