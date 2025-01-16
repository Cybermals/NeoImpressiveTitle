from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

from ui.floating_window import FloatingWindow
from ui.textured_progress import TexturedProgress

# Initialize fonts
LabelBase.register(
    "ConsolaMono",
    fn_regular="fonts/ConsolaMono.ttf",
    fn_bold="fonts/ConsolaMono-Bold.ttf"
)


# Classes
# =======
class GameButton(Button):
    def on_press(self):
        try:
            base.click_sfx.play()

        except NameError:
            # The sound effect is only available ingame. Theme testing doesn't
            # need it.
            pass


class GameCheckBox(CheckBox):
    pass


class GameFloatingWindow(FloatingWindow):
    pass


class GameLabel(Label):
    pass


class GamePanel(BoxLayout):
    pass


class GamePopup(Label):
    def dismiss(self):
        # Hide the popup
        self.parent.remove_widget(self)

    def on_touch_down(self, touch):
        # Dismiss the popup and stop processing the event
        self.dismiss()
        return True


class GameSlider(Slider):
    pass


class GameSpinner(Spinner):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Set dropdown and option classes
        self.dropdown_cls = GameSpinnerDropDown
        self.option_cls = GameSpinnerOption


class GameSpinnerDropDown(DropDown):
    pass


class GameSpinnerOption(ToggleButton):
    pass


class GameSwitch(Switch):
    pass


class GameTabbedPanel(TabbedPanel):
    pass


class GameTabbedPanelItem(TabbedPanelItem):
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
