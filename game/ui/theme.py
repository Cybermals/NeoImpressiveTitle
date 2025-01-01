from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

from ui.floating_window import FloatingWindow
from ui.option_button import OptionButton
from ui.textured_progress import TexturedProgress


# Classes
# =======
class GameButton(Button):
    pass


class GameCheckBox(CheckBox):
    pass


class GameFloatingWindow(FloatingWindow):
    pass


class GameLabel(Label):
    pass


class GameOptionButton(OptionButton):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Set the option class to our themed toggle button
        self.optionclass = GameToggleButton


class GamePanel(BoxLayout):
    pass


class GameSlider(Slider):
    pass


class GameSwitch(Switch):
    pass


class GameTabbedPanel(TabbedPanel):
    pass


class GameTextArea(TextInput):
    pass


class GameTextInput(TextInput):
    pass


class GameTexturedProgress(TexturedProgress):
    pass


class GameToggleButton(ToggleButton):
    pass


Builder.load_file("ui/theme.kv")
