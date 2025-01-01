from kivy.app import App

from ui.theme import GameTabbedPanel


# Classes
# =======
class MainScreen(GameTabbedPanel):
    pass


class TestTheme(App):
    def build(self):
        return MainScreen()


# Entry Point
# ===========
if __name__ == "__main__":
    TestTheme().run()
