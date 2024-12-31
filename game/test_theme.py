from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

import ui.theme


# Classes
# =======
class MainScreen(BoxLayout):
    pass


class TestTheme(App):
    def build(self):
        return MainScreen()


# Entry Point
# ===========
if __name__ == "__main__":
    TestTheme().run()
