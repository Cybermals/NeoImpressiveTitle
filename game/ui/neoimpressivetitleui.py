from panda3d_kivy.app import App
from kivy.uix.screenmanager import FadeTransition, NoTransition, ScreenManager

import ui.screens.splash_screen
import ui.screens.title_screen
import ui.screens.campaign_screen
import ui.screens.login_screen
import ui.screens.loading_screen
import ui.screens.character_select_screen
import ui.screens.character_editor_screen  # noqa: F401


# Classes
# =======
class MainScreen(ScreenManager):
    pass


class NeoImpressiveTitleUI(App):
    def build(self):
        self.main_screen = MainScreen()
        return self.main_screen

    def switch_to_screen(self, name):
        # Switch screens
        if name in ["TitleScreen"]:
            self.main_screen.transition = FadeTransition()

        else:
            self.main_screen.transition = NoTransition()

        self.main_screen.current = name

        if name == "SplashScreen":
            self.main_screen.current_screen.reset()
