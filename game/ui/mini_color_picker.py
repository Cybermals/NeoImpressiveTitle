from kivy.lang import Builder
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout


# Classes
# =======
class MiniColorPicker(BoxLayout):
    color = ListProperty([1, 1, 1, 1])
    red_slider = ObjectProperty(None)
    green_slider = ObjectProperty(None)
    blue_slider = ObjectProperty(None)

    def on_color(self, instance, value):
        # Return if the color sliders don't exist yet
        if (self.red_slider is None or 
            self.green_slider is None or 
            self.blue_slider is None):
            return
        
        # Update color slider values
        self.red_slider.value = value[0] * 255
        self.green_slider.value = value[1] * 255
        self.blue_slider.value = value[2] * 255

    def update_red(self, value):
        try:
            self.red_slider.value = max(min(int(value), 255), 0)

        except ValueError:
            pass  # the red value is currently invalid

    def update_green(self, value):
        try:
            self.green_slider.value = max(min(int(value), 255), 0)

        except ValueError:
            pass  # the green value is currently invalid

    def update_blue(self, value):
        try:
            self.blue_slider.value = max(min(int(value), 255), 0)

        except ValueError:
            pass  # the blue value is currently invalid


Builder.load_file("ui/mini_color_picker.kv")
