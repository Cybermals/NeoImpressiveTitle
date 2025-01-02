from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

from ui.theme import FloatingWindow, GamePopup


# Classes
# =======
class Window1(FloatingWindow):
    pass


class Window2(FloatingWindow):
    pass


class MainScreen(Widget):
    window1 = ObjectProperty(None)
    window2 = ObjectProperty(None)
    popup = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Create windows
        self.window1 = Window1(pos=(0, 20))
        self.window2 = Window2(pos=(20, 0))

        # Create popup
        self.popup = GamePopup()
        self.popup.text = "Hello World!"

    def show_windows(self):
        if self.window1 not in self.children:
            self.add_widget(self.window1)

        if self.window2 not in self.children:
            self.add_widget(self.window2)

    def show_popup(self):
        if self.popup not in self.children:
            self.popup.size = self.size
            self.add_widget(self.popup)


class TestTheme(App):
    def build(self):
        return MainScreen()


# Entry Point
# ===========
if __name__ == "__main__":
    TestTheme().run()
