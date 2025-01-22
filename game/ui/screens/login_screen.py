import webbrowser

from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen

import config
import ui.theme  # noqa: F401


# Classes
# =======
class LoginScreen(Screen):
    login_btn = ObjectProperty(None)
    username = StringProperty("")
    password = StringProperty("")

    def validate_credentials(self):
        # Enable/disable login button based on the validity of the given
        # credentials
        self.login_btn.disabled = (len(self.username) < 1 or
                                   len(self.password) < 1)

    def login(self):
        base.game_state.request(  # noqa: F821
            "ConnectingScreen",
            self.username,
            self.password
        )

    def new_account(self):
        webbrowser.open_new_tab(config.REGISTRATION_URL)

    def change_password(self):
        webbrowser.open_new_tab(config.PASSWORD_CHANGE_URL)


Builder.load_file("ui/screens/login_screen.kv")
