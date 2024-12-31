from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

from ui.option_button import OptionButton


# Classes
# =======
class GameButton(Button):
    pass


class GameCheckBox(CheckBox):
    pass


class GameOptionButton(OptionButton):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Set the option class to our themed toggle button
        self.optionclass = GameToggleButton


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


class GameToggleButton(ToggleButton):
    pass


Builder.load_file("ui/theme.kv")
