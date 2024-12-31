from kivy.lang import Builder
from kivy.properties import DictProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.togglebutton import ToggleButton


# Classes
# =======
class OptionButton(Button):
    optionclass = ObjectProperty(ToggleButton)
    options = DictProperty({})
    value = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Create dropdown
        self.dropdown = DropDown(size_hint=(None, None))
        self.dropdown.bind(on_select=lambda instance, selection: self.on_select(selection))

    def on_release(self):
        # Open dropdown
        self.dropdown.open(self)

    def on_options(self, instance, value):
        # Clear existing widgets
        self.dropdown.clear_widgets()

        # Populate dropdown with options
        for i, option in enumerate(value.keys()):
            # Create a button for this option
            btn = self.optionclass(
                group="options",
                text=option,
                size_hint_y=None,
                height=44,
                state="down" if i == 0 else "normal"
            )
            btn.bind(on_release=lambda instance: self.dropdown.select(instance.text))
            self.dropdown.add_widget(btn)

        # Set initial selection
        self.text = list(value.keys())[0]
        self.value = value[self.text]

    def on_select(self, selection):
        # Set new selection
        self.text = selection
        self.value = self.options[selection]


Builder.load_file("ui/option_button.kv")
