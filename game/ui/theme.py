from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput


# Classes
# =======
class GameButton(Button):
    pass


class GameCheckBox(CheckBox):
    pass


class GameDropDown(DropDown):
    selection = StringProperty("")

    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Create option buttons
        for i in range(10):
            option_btn = GameButton(
                text=f"Option {i}",
                size_hint_y=None,
                height=44
            )
            option_btn.bind(on_release=lambda instance: self.select(instance.text))
            self.add_widget(option_btn)

        # Create main button
        self.main_btn = GameButton(
            text=self.selection,
            size_hint=(None, None)
        )
        self.main_btn.bind(on_release=self.open)
        self.add_widget(self.main_btn)

    def on_select(self, new_selection):
        # Set new selection
        self.selection = new_selection
        self.main_btn.text = new_selection


class GameProgressBar(ProgressBar):
    pass


class GameSlider(Slider):
    pass


class GameSwitch(Switch):
    pass


class GameTextArea(TextInput):
    pass


class GameTextInput(TextInput):
    pass


Builder.load_file("ui/theme.kv")
