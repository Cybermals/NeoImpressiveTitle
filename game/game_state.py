from direct.fsm.FSM import FSM


# Game State Class
# ================
class GameState(FSM):
    def enterSplashScreen(self):
        # Show splash screen and play title screen music
        base.ui.switch_to_screen("SplashScreen")
        base.title_music.play()

    def exitSplashScreen(self):
        pass

    def enterTitleScreen(self):
        # Show title screen
        base.ui.switch_to_screen("TitleScreen")

    def exitTitleScreen(self):
        pass

    def enterCampaignScreen(self):
        # Show campaign screen
        base.ui.switch_to_screen("CampaignScreen")

    def exitCampaignScreen(self):
        pass

    def enterLoginScreen(self):
        # Show the login screen
        base.ui.switch_to_screen("LoginScreen")

    def exitLoginScreen(self):
        pass

    def enterConnectingScreen(self, username, password):
        # Show the connecting screen
        base.ui.switch_to_screen("LoadingScreen")

        # Do login
        print("Connecting...")
        print(f"username = {username}")
        print(f"password = {password}")

    def exitConnectingScreen(self):
        pass

    def enterCharacterSelectScreen(self):
        # Show the character select screen
        base.ui.switch_to_screen("CharacterSelectScreen")

    def exitCharacterSelectScreen(self):
        pass
