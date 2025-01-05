from panda3d_kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import FadeTransition, NoTransition, ScreenManager

import ui.screens.splash_screen


# Classes
# =======
class MainScreen(ScreenManager):
    splash_screen = ObjectProperty(None)


class NeoImpressiveTitleUI(App):
    def __init__(self, *args, **kwargs):
        # Call base constructor
        super().__init__(*args, **kwargs)

        self.main_screen = None

    def build(self):
        self.main_screen = MainScreen()
        return self.main_screen
    
    def switch_to_screen(self, name):
        # Return if the main screen has not yet been created
        if self.main_screen is None:
            return
        
        # Switch screens
        if name in ["TitleScreen"]:
            self.main_screen.transition = FadeTransition()

        else:
            self.main_screen.transition = NoTransition()

        self.main_screen.current = name

        if name == "SplashScreen":
            self.main_screen.current_screen.reset()
