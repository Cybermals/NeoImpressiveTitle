from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen

import ui.theme


# Classes
# =======
class LoginScreen(Screen):
    login_btn = ObjectProperty(None)
    username = StringProperty("")
    password = StringProperty("")

    def validate_credentials(self):
        # Enable/disable login button based on the validity of the given credentials
        self.login_btn.disabled = (len(self.username) < 1 or len(self.password) < 1)


Builder.load_file("ui/screens/login_screen.kv")
